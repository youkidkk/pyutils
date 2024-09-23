from pyutils import texts


class Console:
    def __init__(
        self,
        indent_width: int = 2,
    ):
        self._indent_width: int = indent_width
        self._indent_level: int = 0
        self._last_text: int = ""

    def _filled_text(self, text):
        """インデント、末尾のスペースを付与したテキスト"""
        indent = " " * self._indent_level * self._indent_width
        text = f"{indent}{text}"
        if (sp_width := texts.width(self._last_text) - texts.width(text)) > 0:
            text = text + (" " * sp_width)
        return text

    def print(self, text: str) -> str:
        """カレント行にテキストを出力"""
        filled_text = self._filled_text(text)
        print(
            filled_text,
            end="\r",
        )
        self._last_text = filled_text.rstrip()
        return filled_text

    def line_break(self) -> str:
        """改行する"""
        print()
        self._last_text = ""
        return ""

    def print_line(self, text: str = "") -> str:
        """カレント行にテキストを出力後に改行"""
        self.print(text)
        return self.line_break()

    def indent(self, level: int = 1) -> int:
        """インデントを追加"""
        if self._last_text:
            self.line_break()
        self._indent_level += level
        return self._indent_level

    def unindent(self, level: int = 1) -> int:
        """インデントを削除"""
        if self._last_text:
            self.line_break()
        self._indent_level -= level
        if self._indent_level < 0:
            self._indent_level = 0
        return self._indent_level

    def init_indent(self) -> int:
        """インデントを初期化"""
        if self._last_text:
            self.line_break()
        self._indent_level = 0
        return self._indent_level
