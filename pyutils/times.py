from datetime import datetime, timezone


def local_time_from_utc(target_datetime: datetime) -> datetime:
    """UTCのdatetimeをローカル環境の時刻（ネイティブ形式）に変換する"""
    target_without_tz = (
        target_datetime.replace(tzinfo=timezone.utc)
        if not target_datetime.tzinfo
        # タイムゾーン情報を持っている（awareな）場合、UTCに変換
        else target_datetime.astimezone(timezone.utc)
    )
    return target_without_tz.astimezone().replace(tzinfo=None)
