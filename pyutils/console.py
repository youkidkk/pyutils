import threading

from pyutils import classes, texts


@classes.singleton
class Console:
    def __init__(
        self,
        indent_width: int = 2,
        top_level: int = 0,
        init_indent_level: int = 0,
    ):
        self._indent_width: int = indent_width
        self._top_level: int = top_level
        self._indent_level: int = init_indent_level
        self._last_text: str = ""  # 型を str に修正

        self._lock = threading.RLock()

    def _indent_space(self) -> str:
        return " " * (self._top_level + self._indent_level) * self._indent_width

    def _filled_text(self, text: str) -> str:
        text = f"{self._indent_space()}{text}"
        if (sp_len := len(self._last_text) - len(text)) > 0:
            text = text + (" " * sp_len * 2)
        return text

    def print(self, text: str, end: str = "") -> str:
        """カレント行にテキストを出力"""
        with self._lock:
            filled_text = self._filled_text(texts.remove_ctrl_chars(text))
            print("\r" + filled_text, end=end, flush=True)
            self._last_text = filled_text.rstrip()
            return filled_text

    def line_break(self) -> str:
        """改行する"""
        with self._lock:
            print()
            self._last_text = ""
            return ""

    def print_line(self, text: str = "") -> str:
        """カレント行にテキストを出力後に改行"""
        with self._lock:
            self.print(text)
            return self.line_break()

    def indent(self, level: int = 1) -> int:
        """インデントを追加"""
        with self._lock:
            if self._last_text:
                self.line_break()
            self._indent_level += level
            return self._indent_level

    def unindent(self, level: int = 1) -> int:
        """インデントを削除"""
        with self._lock:
            if self._last_text:
                self.line_break()
            self._indent_level -= level
            if self._indent_level < 0:
                self._indent_level = 0
            return self._indent_level

    def init_indent(self) -> int:
        """インデントを初期化"""
        with self._lock:
            if self._last_text:
                self.line_break()
            self._indent_level = 0
            return self._indent_level

    def wait_enter(self, text: str = "Press Enter key") -> None:
        """Enterキーの入力待ち"""
        with self._lock:
            self.print(f"{text}: ", end="")
            input()

    def confirm(self, text: str, default: bool = False) -> bool:
        """Y or N の入力"""
        with self._lock:
            self.print(f"""{text} ({"Y/n" if default else "y/N"}): """, end="")
            choice = input()
            if default:
                return choice.lower() != "n"
            else:
                return choice.lower() == "y"

    def input_int(self, text: str) -> int:
        """整数の入力待ち"""
        while True:
            with self._lock:
                self.print(f"{text}: ", end="")
                intext = input()
            try:
                return int(intext)
            except ValueError:
                pass
