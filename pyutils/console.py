from pyutils import texts


class Console:
    indent_width = 2

    def __init__(self):
        self.indent_level = 0
        self.last_text_width = 0

    def log(self, text: str, newline: bool = False) -> None:
        text_width = texts.width(" " * self.indent_level * Console.indent_width + text)
        if text_width < self.last_text_width:
            text = text + " " * (self.last_text_width - text_width)
        print(
            " " * self.indent_level * Console.indent_width + text,
            end="\n" if newline else "\r",
        )
        self.last_text_width = text_width

    def log_ln(self, text: str = "") -> None:
        self.log(text, newline=True)

    def indent(self, level: int = 1):
        self.indent_level += level

    def unindent(self, level: int = 1):
        self.indent_level -= level

    def init_indent(self):
        self.indent_level = 0
