from pyutils import classes


@classes.singleton
class TestSingleton:
    pass


def test_classes():
    s1 = TestSingleton()
    s2 = TestSingleton()
    assert s1 == s2
    assert s1 is s2

    classes._instances = {}
    s3 = TestSingleton()
    assert s1 != s3
    assert s1 is not s3
