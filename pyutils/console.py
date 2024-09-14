from pyutils import texts


class Console:
    indent_width = 2

    def __init__(self):
        self.indent_level = 0
        self.last_text_width = 0

    def log(self, text: str, newline: bool = False) -> None:
        """カレント行にログを出力"""
        text_width = texts.width(" " * self.indent_level * Console.indent_width + text)
        if text_width < self.last_text_width:
            text = text + " " * (self.last_text_width - text_width)
        print(
            " " * self.indent_level * Console.indent_width + text,
            end="\n" if newline else "\r",
        )
        self.last_text_width = text_width

    def log_ln(self, text: str = "") -> None:
        """カレント行にログを出力した後に改行"""
        self.log(text, newline=True)

    def indent(self, level: int = 1):
        """インデントを追加"""
        self.indent_level += level

    def unindent(self, level: int = 1):
        """インデントを削除"""
        self.indent_level -= level

    def init_indent(self):
        """インデントを初期化"""
        self.indent_level = 0
