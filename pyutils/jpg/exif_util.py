from datetime import datetime

from PIL import ExifTags, Image, UnidentifiedImageError


def _get_exif_tagid(name: str) -> int:
    return [id for id, val in ExifTags.TAGS.items() if val == name][0]


tag_id_dtorg = _get_exif_tagid("DateTimeOriginal")
tag_id_subsec = _get_exif_tagid("SubsecTimeOriginal")


def get_shoot_dt(path: str) -> datetime:
    try:
        img = Image.open(path)
        exif = img.getexif()
        exif_dict = exif.get_ifd(ExifTags.IFD.Exif)
        dtorg = exif_dict.get(tag_id_dtorg, "")
        subsec = exif_dict.get(tag_id_subsec, "000000")
        return datetime.strptime(dtorg + subsec, "%Y:%m:%d %H:%M:%S%f")
    except (UnidentifiedImageError, ValueError):
        return None
