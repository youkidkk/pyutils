import os
from datetime import datetime
from pathlib import Path
from typing import Union

import win32_setctime
from PIL import ExifTags, Image, UnidentifiedImageError

quality_default = int(os.environ.get("JPG_COMPRESS_QUALITY") or "25")


def _get_exif_tagid(name: str) -> int:
    return [id for id, val in ExifTags.TAGS.items() if val == name][0]


tag_id_dtorg = _get_exif_tagid("DateTimeOriginal")
tag_id_subsec = _get_exif_tagid("SubsecTimeOriginal")


def _shoot_datetime_from_exif(target: Path) -> datetime | None:
    try:
        img = Image.open(target)
        exif = img.getexif()
        if not exif:
            # EXIFが取得できない場合
            return
        exif_dict = exif.get_ifd(ExifTags.IFD.Exif)
        dtorg = exif_dict.get(tag_id_dtorg)
        if not dtorg:
            # 撮影日時が取得できない場合
            return
        subsec = exif_dict.get(tag_id_subsec) or "000000"
        return datetime.strptime(dtorg + subsec, "%Y:%m:%d %H:%M:%S%f")
    except (UnidentifiedImageError, ValueError):
        return


def shoot_datetime(target_file: Path | str) -> datetime | None:
    """撮影日時を取得"""
    target_path = Path(target_file)
    if not target_path.exists() or not target_path.is_file():
        raise ValueError(
            f"対象ファイルが存在しないか、ファイルではない: {target_file}",
        )
    if result := _shoot_datetime_from_exif(target_path):
        return result


def compress(
    target_file: Union[Path, str],
    dst_dir: Union[Path, str],
    quality=quality_default,
) -> Path:
    """画像ファイルを指定した圧縮率で圧縮"""
    target_path = Path(target_file)
    if not target_path.exists() or not target_path.is_file():
        raise AttributeError(
            f"対象ファイルが存在しないか、ファイルではない: {target_file}",
        )

    dst_path = Path(dst_dir).joinpath(target_path.name)
    if dst_path.exists():
        raise AttributeError(
            f"出力先ファイルが存在: {str(dst_path)}",
        )

    with Image.open(target_path) as img:
        exif = img.info.get("exif")
        if not exif:
            raise
        img.save(
            dst_path,
            optimize=True,
            quality=quality,
            exif=img.info.get("exif"),
        )

    if shoot_dt := shoot_datetime(str(target_path)):
        # 撮影日時が存在する場合、作成日時、更新日時を撮影日時で更新
        win32_setctime.setctime(dst_path, shoot_dt.timestamp())
        os.utime(dst_path, (shoot_dt.timestamp(), shoot_dt.timestamp()))

    return dst_path
