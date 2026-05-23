import os
import tempfile
from datetime import datetime
from pathlib import Path

import win32_setctime
from PIL import ExifTags, Image, UnidentifiedImageError

from pyutils import filesystem

# 環境変数の読み込み
quality_default = int(os.environ.get("JPG_COMPRESS_QUALITY", "25"))


def _get_exif_tagid(name: str) -> int:
    """タグ名から安全にIDを取得する（存在しない場合はValueError）"""
    tag_id = next((id for id, val in ExifTags.TAGS.items() if val == name), None)
    if tag_id is None:
        raise ValueError(f"指定されたEXIFタグ名が見つかりません: {name}")
    return tag_id


tag_id_dtorg = _get_exif_tagid("DateTimeOriginal")
tag_id_subsec = _get_exif_tagid("SubsecTimeOriginal")


def _shoot_datetime_from_exif(target: Path) -> datetime | None:
    try:
        with Image.open(target) as img:
            exif = img.getexif()
            if not exif:
                # EXIFが取得できない場合
                return None

            exif_dict = exif.get_ifd(ExifTags.IFD.Exif)
            dtorg = exif_dict.get(tag_id_dtorg)
            if not dtorg:
                # 撮影日時が取得できない場合
                return None

            # サブ秒（ミリ秒）の取得と成形
            subsec = exif_dict.get(tag_id_subsec, "000000")
            # 桁数が可変（2桁や3桁）でも、後ろに0を詰めて6桁（マイクロ秒）に揃える
            subsec = f"{subsec:<06}"[:6]

            return datetime.strptime(f"{dtorg}.{subsec}", "%Y:%m:%d %H:%M:%S.%f")

    except (UnidentifiedImageError, ValueError, KeyError):
        return None


def shoot_datetime(target_file: Path | str) -> datetime:
    """撮影日時を取得"""
    target_path = Path(target_file)
    if not target_path.is_file():
        raise ValueError(
            f"対象ファイルが存在しないか、ファイルではない: {target_file}",
        )
    if result := _shoot_datetime_from_exif(target_path):
        # EXIFから撮影日時が取得できた場合 -> その値を返却
        return result
    # 取得できない場合は作成日時または更新日時を返却
    return filesystem.get_older_file_timestamp(target_path)


def compress(
    src_path: Path | str,
    dst_dir: Path | str,
    quality: int = quality_default,
) -> Path:
    """画像ファイルを指定した圧縮率で圧縮し、タイムスタンプを撮影日時に同期する。"""
    target_path = Path(src_path)
    if not target_path.is_file():
        raise ValueError(
            f"対象ファイルが存在しないか、ファイルではない: {src_path}",
        )

    dst_path = Path(dst_dir).joinpath(target_path.name)
    if dst_path.exists():
        raise ValueError(
            f"出力先ファイルが存在: {dst_path}",
        )

    dt_timestamp = shoot_datetime(target_path).timestamp()
    try:
        with (
            Image.open(target_path) as img,
            tempfile.TemporaryDirectory(dir=dst_dir) as tempdir,
        ):
            tempdst = Path(tempdir).joinpath(target_path.name)
            ext_params = {
                k: v for k, v in {"exif": img.info.get("exif")}.items() if v is not None
            }
            img.save(
                tempdst,
                optimize=True,
                quality=quality,
                **ext_params,
            )
            tempdst.rename(dst_path)

        # タイムスタンプの更新
        win32_setctime.setctime(dst_path, dt_timestamp)
        os.utime(dst_path, (dt_timestamp, dt_timestamp))

        return dst_path
    except Exception:
        raise
