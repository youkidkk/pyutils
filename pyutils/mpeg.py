import dataclasses
import json
import re
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser


@dataclasses.dataclass
class Size:
    width: int
    height: int


def _size_from_ffmpeg(target_path: Path) -> Size | None:
    command = [
        "ffprobe",
        "-v",
        "error",
        "-show_format",
        "-show_streams",
        "-of",
        "json",
        str(target_path),
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=True,
        )
        data = json.loads(result.stdout)

        # ビデオストリームの特定
        video_stream = None
        for stream in data.get("streams", []):
            if stream.get("codec_type") == "video":
                video_stream = stream
                break

        if not video_stream:
            return None, None

        width = int(video_stream.get("width", 0))
        height = int(video_stream.get("height", 0))

        # --- 回転情報の抽出（4段階で探索） ---
        rotation = 0

        # 1. side_data_list 内の直接の 'rotation' キーを探す
        if "side_data_list" in video_stream:
            for side_data in video_stream["side_data_list"]:
                if "rotation" in side_data:
                    rotation = int(side_data["rotation"])
                    break
                # 近年のFFmpeg対策: displaymatrix の文字列内に
                # "rotation of -90.00 degrees" などが含まれる場合をパース
                elif "displaymatrix" in side_data:
                    dm_text = side_data["displaymatrix"]
                    match = re.search(r"rotation of\s+(-?\d+)", dm_text)
                    if match:
                        rotation = int(match.group(1))
                        break

        # 2. ビデオストリームの tags.rotate を探す
        if rotation == 0 and "tags" in video_stream:
            if "rotate" in video_stream["tags"]:
                rotation = int(video_stream["tags"]["rotate"])

        # 3. ファイル全体の format.tags.rotate を探す (一部のコンテナ用)
        if rotation == 0 and "format" in data and "tags" in data["format"]:
            if "rotate" in data["format"]["tags"]:
                rotation = int(data["format"]["tags"]["rotate"])

        # 4. マイナス回転（-90度など）を正の数に揃える
        rotation = rotation % 360

        # --- 📐 実際のサイズ計算 ---
        actual_width, actual_height = width, height
        if rotation in [90, 270]:
            actual_width, actual_height = height, width

        return Size(actual_width, actual_height)
    except Exception:
        return


def _size_from_hachoir(target_path: Path) -> Size | None:
    parser = createParser(str(target_path))
    if not parser:
        return None, None
    try:
        metadata = extractMetadata(parser)
        if not metadata:
            return None

        # メタデータから幅と高さを取得
        width = metadata.get("width") if metadata.has("width") else None
        height = metadata.get("height") if metadata.has("height") else None

        if not width or not height:
            return
        return Size(int(width), int(height))
    except Exception:
        return None
    finally:
        parser.close()


def size(target_file: Path | str) -> Size | None:
    """動画のサイズを取得"""
    target_path = Path(target_file)

    if result := _size_from_ffmpeg(target_path):
        return result
    if result := _size_from_hachoir(target_path):
        return result

    return


def shoot_datetime(file: Path | str) -> datetime | None:
    path = Path(file)
    parser = createParser(str(path))
    if not parser:
        return
    try:
        if metadata := extractMetadata(parser):
            if not metadata.has("creation_date"):
                return
        return metadata.get("creation_date") + timedelta(hours=9)
    except Exception:
        return
    finally:
        parser.close()


def _output_scale(file: Path, scale=960) -> str | None:
    size_ = size(file)
    if not size_:
        return

    if size_.width > size_.height:
        # 横長
        return f"scale={scale}:-2"
    elif size_.width < size_.height:
        # 縦長
        return f"scale=-2:{scale}"
    else:
        return f"scale={scale}:{scale}"


def compress(
    src_file: Path | str,
    dst_file: Path | str,
    scale: int = 960,
    crf: int = 28,
    preset: str = "slower",
) -> Path | None:
    """
    MP4動画を圧縮する

    :param src_file: 元ファイル
    :param dst_file: 圧縮後の保存先ファイル
    :param crf: 画質と圧縮率のバランス（0〜51）。数値が大きいほど高圧縮。
                H.265の場合、28前後が「画質を維持しつつ激変する」ベストスポットです。
    :param preset: 圧縮にかける時間。'slower' や 'veryslow' にするほど、
                   時間はかかりますが圧縮率は最高になります。
    """
    src_path = Path(src_file)
    dst_path = Path(dst_file)

    if not src_path.exists():
        return
    if dst_path.exists():
        return

    scale = _output_scale(str(src_path))
    if not scale:
        return

    # FFmpegのコマンドを構築
    command = [
        "ffmpeg",
        "-y",  # 同名ファイルがあれば上書き
        "-i",
        str(src_path),  # 入力ファイル
        "-c:v",
        "libx265",  # ビデオコーデックに H.265 (HEVC) を指定
        "-crf",
        str(crf),  # 恒常画質モード（サイズと画質のバランス）
        "-vf",
        scale,
        "-preset",
        preset,  # エンコード速度（遅い＝圧縮効率UP）
        "-c:a",
        "aac",  # 音声を汎用性の高いAACに変換
        "-b:a",
        "128k",  # 音声ビットレートを128kbpsに抑える
        str(dst_path),
    ]

    try:
        # コマンドを実行
        subprocess.run(
            command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        return dst_path
    except subprocess.CalledProcessError:
        return
