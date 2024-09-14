import os
from datetime import datetime
from pathlib import Path
from typing import Optional

import win32_setctime
from PIL import ExifTags, Image, UnidentifiedImageError

quality_default = int(os.environ.get("QUALITY_JPG") or "50")


def _get_exif_tagid(name: str) -> int:
    return [id for id, val in ExifTags.TAGS.items() if val == name][0]


tag_id_dtorg = _get_exif_tagid("DateTimeOriginal")
tag_id_subsec = _get_exif_tagid("SubsecTimeOriginal")


def shoot_datetime(path: str) -> Optional[datetime]:
    try:
        img = Image.open(path)
        exif = img.getexif()
        exif_dict = exif.get_ifd(ExifTags.IFD.Exif)
        dtorg = exif_dict.get(tag_id_dtorg, "")
        subsec = exif_dict.get(tag_id_subsec, "000000")
        return datetime.strptime(dtorg + subsec, "%Y:%m:%d %H:%M:%S%f")
    except (UnidentifiedImageError, ValueError):
        return None


def compress(src_path: Path, dst_dir: Path, quality=quality_default) -> Path:
    shoot_dt = shoot_datetime(str(src_path))
    with Image.open(src_path) as img:
        exif = img.info.get("exif")
        dst_path = dst_dir.joinpath(src_path.name)
        if not exif:
            raise
        img.save(
            dst_path,
            optimize=True,
            quality=quality,
            exif=img.info.get("exif"),
        )
    if shoot_dt:
        win32_setctime.setctime(dst_path, shoot_dt.timestamp())
        os.utime(dst_path, (shoot_dt.timestamp(), shoot_dt.timestamp()))
    return dst_path
