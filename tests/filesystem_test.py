import os
from datetime import datetime, timedelta
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from pyutils import filesystem as fs


class TestNormalizePath:
    @pytest.fixture(
        params=[
            "test1/test2/test3",
            "test1\\test2/test3",
            "test1/test2\\test3",
        ]
    )
    def pattern(self, request):
        return fs._normalize_path(request.param)

    def test__normalize_path(self, pattern):
        assert pattern == Path("test1/test2/test3")


def _create_test_files(temp: Path):
    #   test1
    #   test2
    #   test3
    temp.joinpath("test1").touch()
    temp.joinpath("test2").touch()
    temp.joinpath("test3").touch()
    #   dir1:
    #     dir1_test1
    #     dir1_test2
    (dir1 := temp.joinpath("dir1")).mkdir(parents=True)
    dir1.joinpath("dir1_test1").touch()
    dir1.joinpath("dir1_test2").touch()
    #     dir11:
    #       dir11_test1
    #       dir11_test2
    (dir11 := dir1.joinpath("dir11")).mkdir(parents=True)
    dir11.joinpath("dir11_test1").touch()
    dir11.joinpath("dir11_test2").touch()
    #   dir2:
    #     dir2_test1
    (dir2 := temp.joinpath("dir2")).mkdir(parents=True)
    dir2.joinpath("dir2_test1").touch()
    # dir3: empty
    temp.joinpath("dir3").mkdir(parents=True)


class TestWalk:
    @pytest.fixture
    def init(self):
        with TemporaryDirectory(dir=".") as temp:
            # temp:
            self.temp = Path(temp)
            _create_test_files(self.temp)
            self.default_result = {
                self.temp: [
                    Path("test1"),
                    Path("test2"),
                    Path("test3"),
                ],
                self.temp.joinpath("dir1"): [
                    Path("dir1_test1"),
                    Path("dir1_test2"),
                ],
                self.temp.joinpath("dir1", "dir11"): [
                    Path("dir11_test1"),
                    Path("dir11_test2"),
                ],
                self.temp.joinpath("dir2"): [
                    Path("dir2_test1"),
                ],
            }
            yield
        pass

    def test_default(self, init):
        # デフォルト
        # result_type: WalkResultType.FileNameOnly
        # empty_dir: False
        assert fs.walk(self.temp) == self.default_result

    def test_absolute(self, init):
        # result_type: WalkResultType.Absolute
        assert fs.walk(
            self.temp,
            fs.WalkResultType.Absolute,
        ) == {
            dir.absolute(): [dir.joinpath(file).absolute() for file in files]
            for dir, files in self.default_result.items()
        }

    def test_filenameonly(self, init):
        # result_type: WalkResultType.FileNameOnly
        assert (
            fs.walk(
                self.temp,
                fs.WalkResultType.FileNameOnly,
            )
            == self.default_result
        )

    def test_relative(self, init):
        # result_type: WalkResultType.Relative
        assert fs.walk(
            self.temp,
            fs.WalkResultType.Relative,
        ) == {
            dir: [dir.joinpath(file) for file in files]
            for dir, files in self.default_result.items()
        }

    def test_emptydir_true(self, init):
        # result_type: WalkResultType.FileNameOnly ※デフォルト
        # empty_dir: True
        assert fs.walk(
            self.temp,
            empty_dir=True,
        ) == {
            **self.default_result,
            self.temp.joinpath("dir3"): [],
        }

    def test_absolute_emptydir_true(self, init):
        # result_type: WalkResultType.Absolute
        # empty_dir: True
        assert fs.walk(
            self.temp,
            fs.WalkResultType.Absolute,
            True,
        ) == {
            **{
                dir.absolute(): [dir.joinpath(file).absolute() for file in files]
                for dir, files in self.default_result.items()
            },
            self.temp.joinpath("dir3").absolute(): [],
        }

    def test_filenameonly_emptydir_true(self, init):
        # result_type: WalkResultType.FileNameOnly
        # empty_dir: True
        assert fs.walk(
            self.temp,
            fs.WalkResultType.FileNameOnly,
            True,
        ) == {
            **self.default_result,
            self.temp.joinpath("dir3"): [],
        }

    def test_relative_emptydir_true(self, init):
        # result_type: WalkResultType.Relative
        # empty_dir: True
        assert fs.walk(
            self.temp,
            fs.WalkResultType.Relative,
            True,
        ) == {
            **{
                dir: [dir.joinpath(file) for file in files]
                for dir, files in self.default_result.items()
            },
            self.temp.joinpath("dir3"): [],
        }

    def test_dir_filter(self, init):
        assert fs.walk(self.temp, dir_filter=lambda d: d.name.startswith("dir1")) == {
            dir: files
            for dir, files in self.default_result.items()
            if dir.name.startswith("dir1")
        }

    def test_file_filter(self, init):
        assert fs.walk(self.temp, file_filter=lambda f: f.name.endswith("test2")) == {
            dir: [f for f in files if f.name.endswith("test2")]
            for dir, files in self.default_result.items()
        }


class TestWalkFils:
    @pytest.fixture
    def init(self):
        with TemporaryDirectory(dir=".") as temp:
            # temp:
            self.temp = Path(temp)
            _create_test_files(self.temp)
            self.default_result = [
                self.temp.joinpath("dir1", "dir11", "dir11_test1"),
                self.temp.joinpath("dir1", "dir11", "dir11_test2"),
                self.temp.joinpath("dir1", "dir1_test1"),
                self.temp.joinpath("dir1", "dir1_test2"),
                self.temp.joinpath("dir2", "dir2_test1"),
                self.temp.joinpath("test1"),
                self.temp.joinpath("test2"),
                self.temp.joinpath("test3"),
            ]
            yield
        pass

    def test_default(self, init):
        result = fs.walk_files(self.temp)
        rrr = self.default_result
        assert result == rrr

    def test_absolute_true(self, init):
        assert fs.walk_files(
            self.temp,
            absolute=True,
        ) == [p.absolute() for p in self.default_result]

    def test_absolute_false(self, init):
        assert (
            fs.walk_files(
                self.temp,
                absolute=False,
            )
            == self.default_result
        )

    def test_file_filter(self, init):
        assert fs.walk_files(
            self.temp, file_filter=lambda f: f.name.endswith("_test2")
        ) == [f for f in self.default_result if f.name.endswith("_test2")]


def test_parent_dirs():
    assert fs.parent_dirs("root/test1/test2/test3", "root") == [
        Path("test1/test2/test3"),
        Path("test1/test2"),
        Path("test1"),
    ]
    assert fs.parent_dirs("root/test1/test2/test3", "root", True) == [
        Path.cwd().joinpath("test1/test2/test3"),
        Path.cwd().joinpath("test1/test2"),
        Path.cwd().joinpath("test1"),
    ]


class TestRemoveEmptyParents:
    @pytest.fixture
    def init(self):
        with TemporaryDirectory(dir=".") as temp:
            self.root = Path(temp)
            self.target = self.root.joinpath("test1", "test2", "test3")
            self.target.mkdir(parents=True)
            self.root.joinpath("test1", "file").touch()
            yield
        pass

    def test(self, init):
        fs.remove_empty_parents(self.target, self.root)
        assert self.root.joinpath("test1").exists()
        assert not self.root.joinpath("test1", "test2").exists()


@pytest.fixture
def temp_file(tmp_path: Path) -> Path:
    """テスト用の空ファイルを一時ディレクトリ内に作成するフィクスチャ"""
    file = tmp_path / "test_file.txt"
    file.write_text("dummy content")
    return file


def test_get_older_timestamp_when_ctime_is_older(temp_file: Path):
    """1. 作成日時(ctime)のほうが更新日時(mtime)より古い場合"""
    # 疑似的な日時を設定
    base_time = datetime(2026, 5, 23, 10, 0, 0)
    ctime_target = base_time - timedelta(hours=1)  # 9:00:00 (古い)
    mtime_target = base_time  # 10:00:00

    # タイムスタンプをエポック秒に変換してファイルに適用
    # ※ os.utime は [アクセス日時, 更新日時] を書き換える
    os.utime(temp_file, (mtime_target.timestamp(), mtime_target.timestamp()))

    # 作成日時の書き換え（Windowsのみ対応。Mac/Linuxでは無視されるが、
    # 誕生時より後のmtimeに設定しているためロジックは成立します）
    try:
        import win32_setctime

        win32_setctime.setctime(str(temp_file), ctime_target.timestamp())
    except ImportError:
        pass

    # テスト実行
    result = fs.get_older_file_timestamp(temp_file)

    # 検証：より古いほうの日時（min）が返ってきているか
    stat = temp_file.stat()
    try:
        expected_ctime = datetime.fromtimestamp(stat.st_birthtime)
    except AttributeError:
        expected_ctime = datetime.fromtimestamp(stat.st_ctime)

    expected_mtime = datetime.fromtimestamp(stat.st_mtime)

    assert result == min(expected_ctime, expected_mtime)


def test_get_older_timestamp_when_mtime_is_older(temp_file: Path):
    """2. 更新日時(mtime)のほうが作成日時(ctime)より古い場合（ファイルの書き換えなどをシミュレート）"""
    # 意図的に更新日時（mtime）を過去に設定
    past_mtime = datetime(2026, 5, 23, 1, 0, 0)
    os.utime(temp_file, (past_mtime.timestamp(), past_mtime.timestamp()))

    # テスト実行
    result = fs.get_older_file_timestamp(temp_file)

    # 検証：作成日時よりも過去に設定したmtimeが選ばれていること
    assert result == past_mtime


def test_accepts_both_str_and_path(temp_file: Path):
    """3. 引数として Path オブジェクトと文字列(str)の両方を受け付けるかのテスト"""
    # Pathオブジェクトを渡す
    result_path = fs.get_older_file_timestamp(temp_file)
    assert isinstance(result_path, datetime)

    # 文字列パスを渡す
    result_str = fs.get_older_file_timestamp(str(temp_file))
    assert isinstance(result_str, datetime)

    assert result_path == result_str


def test_raises_file_not_found_error():
    """4. 存在しないファイルや、ディレクトリが渡されたときに正しくエラーになるか"""
    # 存在しないパス
    with pytest.raises(FileNotFoundError):
        fs.get_older_file_timestamp("non_existent_file.xyz")

    # ファイルではなくディレクトリのパス
    current_dir = Path(__file__).parent
    with pytest.raises(FileNotFoundError):
        fs.get_older_file_timestamp(current_dir)
