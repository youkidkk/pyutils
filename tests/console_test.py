from pyutils.console import Console


def test_console():
    console = Console()
    assert console.print("あ\tい\rう\nえお123  ") == "あいうえお123  "
    assert console.print("あいう12") == "あいう12     "
    console.indent()
    assert console._last_text == ""
    assert console._indent_level == 1
    assert console.print("あいうえお123") == "  あいうえお123"
    assert console.print("あいう12") == "  あいう12     "
    console.indent()
    assert console._indent_level == 2
    assert console.print("あいうえお123") == "    あいうえお123"
    assert console.print_line("あああ") == ""
    assert console.print("あいう12") == "    あいう12"
    console.unindent()
    assert console._indent_level == 1
    assert console.print("あいうえお123") == "  あいうえお123"
    assert console.print("あいう12") == "  あいう12     "
    console.init_indent()
    assert console._indent_level == 0

    console = Console(indent_width=3, top_level=2, init_indent_level=1)
    assert console.print("test") == "         test"
