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


class TestWalkFils:
    @pytest.fixture
    def init(self):
        with TemporaryDirectory(dir=".") as temp:
            # temp:
            self.temp = Path(temp)
            _create_test_files(self.temp)
            self.default_result = [
                self.temp.joinpath("test1"),
                self.temp.joinpath("test2"),
                self.temp.joinpath("test3"),
                self.temp.joinpath("dir1", "dir1_test1"),
                self.temp.joinpath("dir1", "dir1_test2"),
                self.temp.joinpath("dir1", "dir11", "dir11_test1"),
                self.temp.joinpath("dir1", "dir11", "dir11_test2"),
                self.temp.joinpath("dir2", "dir2_test1"),
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
