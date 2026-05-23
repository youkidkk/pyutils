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


def utc_time_from_local(target_datetime: datetime) -> datetime:
    """ローカル時間（JSTなど）のdatetimeをUTCのdatetimeに変換する"""
    target_with_utc_tz = (
        # タイムゾーンを持たない(naive)場合、ローカルタイムゾーンを付与してから、UTCに変換
        target_datetime.astimezone(None).astimezone(timezone.utc)
        if not target_datetime.tzinfo
        # タイムゾーン情報を持っている（awareな）場合、UTCに変換
        else target_datetime.astimezone(timezone.utc)
    )
    return target_with_utc_tz.replace(tzinfo=None)
