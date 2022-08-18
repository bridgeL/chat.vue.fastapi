from pathlib import Path
from datetime import datetime
from colorama import Fore
import colorama
colorama.init(autoreset=True)


def get_time_s(time_i=-1, format="%Y/%m/%d %H:%M:%S"):
    if time_i < 0:
        return datetime.now().strftime(format)
    return datetime.fromtimestamp(time_i).strftime(format)


class Logger:
    color_dict = {
        "_DEBUG_": Fore.CYAN,
        "SUCCESS": Fore.GREEN,
        "WARNING": Fore.YELLOW,
        "ERROR": Fore.LIGHTRED_EX,
    }

    def __init__(self, path=None) -> None:
        self.path = Path(path) if path else None

    def base_print(self, rank: str, *args):
        time_s = get_time_s()

        if self.path:
            with self.path.open("a+", encoding="utf8") as f:
                args_s = " ".join(str(arg) for arg in args)
                text = f"{time_s} [{rank}] {args_s}\n"
                f.write(text)

        # time
        print(Fore.GREEN + time_s + Fore.RESET, end=" ")

        # rank
        color = self.color_dict.get(rank, Fore.RESET)
        print("[" + color + rank + Fore.RESET + "]", end=" ")

        # args
        for arg in args:
            print(str(arg), end=" ")
        print()

    def info(self, *args):
        self.base_print("INFO", *args)

    def success(self, *args):
        self.base_print("SUCCESS", *args)

    def warning(self, *args):
        self.base_print("WARNING", *args)

    def error(self, *args):
        self.base_print("ERROR", *args)

    def debug(self, *args):
        self.base_print("_DEBUG_", *args)


log = Logger()
