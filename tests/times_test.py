import os
import time
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

import pytest

from pyutils import times

# テスト対象の関数をインポート（環境に合わせてパスは書き換えてください）
# from my_module import local_time_from_utc


@pytest.fixture(scope="module", autouse=True)
def set_local_timezone_to_tokyo():
    """テストを実行するマシンのローカルタイムゾーンを強制的に東京(JST)に設定するフィクスチャ。

    ※ Windows環境とLinux/Mac環境の両方に対応しています。
    """
    if os.name == "nt":  # Windows の場合
        # Windowsのtzsetは限定的なため、環境変数で制御できない場合は
        # テスト実行環境がJSTであることを前提とするか、サードパーティ製ライブラリが必要です。
        # ここでは一般的なJST環境を想定します。
        yield
    else:  # Linux / Mac の場合
        old_tz = os.environ.get("TZ")
        os.environ["TZ"] = "Asia/Tokyo"
        time.tzset()
        yield
        if old_tz is not None:
            os.environ["TZ"] = old_tz
        else:
            del os.environ["TZ"]
        time.tzset()


def test_local_time_from_utc_with_naive_datetime():
    """1. タイムゾーン情報のない(naive) UTC日時を渡した場合のテスト"""
    # 入力: 2026-05-23 00:00:00 (UTC想定のプレーンな日時)
    input_dt = datetime(2026, 5, 23, 0, 0, 0)

    result = times.local_time_from_utc(input_dt)

    # 検証: 日本時間(JST)の朝 09:00:00 に変換され、tzinfo が None であること
    assert result == datetime(2026, 5, 23, 9, 0, 0)
    assert result.tzinfo is None


def test_local_time_from_utc_with_aware_utc_datetime():
    """2. すでに UTC タイムゾーンが設定されている(aware)日時を渡した場合のテスト"""
    # 入力: 2026-05-23 00:00:00+00:00
    input_dt = datetime(2026, 5, 23, 0, 0, 0, tzinfo=timezone.utc)

    result = times.local_time_from_utc(input_dt)

    # 検証: 正しく9時間プラスされ、tzinfo が None であること
    assert result == datetime(2026, 5, 23, 9, 0, 0)
    assert result.tzinfo is None


def test_local_time_from_utc_with_aware_jst_datetime():
    """3. 別のタイムゾーン(JST)が設定されている日時を渡した場合のテスト"""
    # 入力: 日本時間の 2026-05-23 15:00:00+09:00 (UTCに直すと 06:00:00)
    input_dt = datetime(2026, 5, 23, 15, 0, 0, tzinfo=ZoneInfo("Asia/Tokyo"))

    result = times.local_time_from_utc(input_dt)

    # 検証:
    # 入力自体がすでにJSTの15時（＝OSのローカル時間と同じ）なので、
    # 関数の内部で一度UTC(6時)に変換されたあと、再びJSTに戻るため、結果は「15:00:00」のままになる。
    assert result == datetime(2026, 5, 23, 15, 0, 0)
    assert result.tzinfo is None


def test_local_time_from_utc_with_aware_ny_datetime():
    """4. ニューヨーク時間など、全く異なるタイムゾーンが設定されている日時を渡した場合のテスト"""
    # 入力: ニューヨーク時間の 2026-05-23 00:00:00-04:00 (夏時間)
    # ニューヨークの0時は、UTCだと「朝04:00」。それを日本時間(JST)に直すと「13:00」になる。
    ny_zone = ZoneInfo("America/New_York")
    input_dt = datetime(2026, 5, 23, 0, 0, 0, tzinfo=ny_zone)

    result = times.local_time_from_utc(input_dt)

    # 検証: ニューヨークの0時 ＝ 日本時間の13時
    assert result == datetime(2026, 5, 23, 13, 0, 0)
    assert result.tzinfo is None
