from pyutils.console import Console


def test_console_log():
    console = Console()
    assert console.log("あいうえお123") == "あいうえお123\r"
    assert console.log("あいう12") == "あいう12     \r"
    console.log_ln()
    console.indent()
    assert console._indent_level == 1
    assert console.log("あいうえお123") == "  あいうえお123\r"
    assert console.log("あいう12") == "  あいう12     \r"
    console.log_ln()
    console.indent()
    assert console._indent_level == 2
    assert console.log("あいうえお123") == "    あいうえお123\r"
    assert console.log("あいう12") == "    あいう12     \r"
    console.log_ln()
    console.unindent()
    assert console._indent_level == 1
    assert console.log("あいうえお123") == "  あいうえお123\r"
    assert console.log("あいう12") == "  あいう12     \r"
    console.log_ln()
    console.init_indent()
    assert console._indent_level == 0


def test_console_log_ln():
    console = Console()
    assert console.log_ln("あいうえお123") == "あいうえお123\n"
    console.indent()
    assert console._indent_level == 1
    assert console.log_ln("あいうえお123") == "  あいうえお123\n"
    console.indent()
    assert console._indent_level == 2
    assert console.log_ln("あいうえお123") == "    あいうえお123\n"
    console.unindent()
    assert console._indent_level == 1
    assert console.log_ln("あいうえお123") == "  あいうえお123\n"
    console.init_indent()
    assert console._indent_level == 0
