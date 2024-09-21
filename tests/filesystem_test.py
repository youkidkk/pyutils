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


class TestWalk:
    @pytest.fixture
    def init_test_walk(self):
        with TemporaryDirectory(dir=".") as temp:
            # temp:
            self.temp = Path(temp)
            #   test1
            #   test2
            #   test3
            self.temp.joinpath("test1").touch()
            self.temp.joinpath("test2").touch()
            self.temp.joinpath("test3").touch()
            #   dir1:
            #     dir1_test1
            #     dir1_test2
            (dir1 := self.temp.joinpath("dir1")).mkdir(parents=True)
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
            (dir2 := self.temp.joinpath("dir2")).mkdir(parents=True)
            dir2.joinpath("dir2_test1").touch()
            # dir3: empty
            self.temp.joinpath("dir3").mkdir(parents=True)
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

    def test_walk_default_param(self, init_test_walk):
        # デフォルト
        # result_type: WalkResultType.FileNameOnly
        # empty_dir: False
        assert fs.walk(self.temp) == self.default_result

    def test_walk_absolute(self, init_test_walk):
        # result_type: WalkResultType.Absolute
        assert fs.walk(
            self.temp,
            fs.WalkResultType.Absolute,
        ) == {
            dir.absolute(): [dir.joinpath(file).absolute() for file in files]
            for dir, files in self.default_result.items()
        }

    def test_walk_filenameonly(self, init_test_walk):
        # result_type: WalkResultType.FileNameOnly
        assert (
            fs.walk(
                self.temp,
                fs.WalkResultType.FileNameOnly,
            )
            == self.default_result
        )

    def test_walk_relative(self, init_test_walk):
        # result_type: WalkResultType.Relative
        assert fs.walk(
            self.temp,
            fs.WalkResultType.Relative,
        ) == {
            dir: [dir.joinpath(file) for file in files]
            for dir, files in self.default_result.items()
        }

    def test_walk_emptydir_true(self, init_test_walk):
        # result_type: WalkResultType.FileNameOnly ※デフォルト
        # empty_dir: True
        assert fs.walk(
            self.temp,
            empty_dir=True,
        ) == {
            **self.default_result,
            self.temp.joinpath("dir3"): [],
        }

    def test_walk_absolute_emptydir_true(self, init_test_walk):
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

    def test_walk_filenameonly_emptydir_true(self, init_test_walk):
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

    def test_walk_relative_emptydir_true(self, init_test_walk):
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
