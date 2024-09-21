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

    def log(self, text: str, newline: bool = False) -> str:
        """カレント行にログを出力"""
        filled_text = self._filled_text(text)
        end = "\n" if newline else "\r"
        print(
            filled_text,
            end=end,
        )
        self._last_text = filled_text.rstrip() if not newline else ""
        return filled_text + end

    def log_ln(self, text: str = "") -> str:
        """カレント行にログを出力した後に改行"""
        return self.log(text, newline=True)

    def indent(self, level: int = 1) -> int:
        """インデントを追加"""
        self._indent_level += level
        return self._indent_level

    def unindent(self, level: int = 1) -> int:
        """インデントを削除"""
        self._indent_level -= level
        if self._indent_level < 0:
            self._indent_level = 0
        return self._indent_level

    def init_indent(self) -> int:
        """インデントを初期化"""
        self._indent_level = 0
        return self._indent_level
