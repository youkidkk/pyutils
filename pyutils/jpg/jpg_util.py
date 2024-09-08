import os
from pathlib import Path

import win32_setctime
from PIL import Image

from pyutils.jpg import exif_util

quality = int(os.environ.get("QUALITY_JPG") or "50")


def compress(src_path: Path, dst_dir: Path) -> Path:
    shoot_dt = exif_util.get_shoot_dt(str(src_path))
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
        win32_setctime.setctime(dst_path, shoot_dt.timestamp())
        os.utime(dst_path, (shoot_dt.timestamp(), shoot_dt.timestamp()))
        return dst_path
