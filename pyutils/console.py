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
        return f"{indent}{text}".ljust(texts.width(self._last_text))

    def log(self, text: str, newline: bool = False) -> None:
        """カレント行にログを出力"""
        text = self._filled_text(text)
        print(
            text,
            end="\n" if newline else "\r",
        )
        self._last_text = text if not newline else ""

    def log_ln(self, text: str = "") -> None:
        """カレント行にログを出力した後に改行"""
        self.log(text, newline=True)

    def indent(self, level: int = 1):
        """インデントを追加"""
        self._indent_level += level

    def unindent(self, level: int = 1):
        """インデントを削除"""
        self._indent_level -= level
        if self._indent_level < 0:
            self._indent_level = 0

    def init_indent(self):
        """インデントを初期化"""
        self._indent_level = 0
