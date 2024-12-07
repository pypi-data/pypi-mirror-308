import sys
import time
import colorama
import getpass
import _io

levels = {
    "INFO": 0,
    "SUCCESS": 1,
    "WARN": 2,
    "ERROR": 3
}


class Logger:
    """日志类"""
    def __init__(self, stdout: _io.TextIOWrapper = sys.stdout,
                 stdin: _io.TextIOWrapper = sys.stdin, level: str = "INFO",
                 time_format: str = "[%Y-%m-%d %H:%M:%S]") -> None:
        """创建日志对象的方法"""
        self.__level = levels[level]
        self.stdout = stdout
        self.stdin = stdin
        self.time_format = time_format

    def set_level(self, level: str):
        """设置日志等级的方法"""
        if level not in levels:
            raise ValueError("unavailable logger level")
        self.__level = levels[level]

    def __output(self, level: str, out: str):
        """输出信息的内部方法"""
        now = time.localtime()
        for i in out.split('\n'):
            self.stdout.write(
                colorama.Fore.RESET + f"{time.strftime(self.time_format, now)}"
                + f"[{level}]" + i + '\n')

    def info(self, out):
        """输出普通信息的方法"""
        if self.__level < levels["INFO"]:
            return
        self.__output(f"{colorama.Fore.BLUE}INFO{colorama.Fore.RESET}", str(out))

    def success(self, out):
        """输出成功信息的方法"""
        if self.__level < levels["SUCCESS"]:
            return
        self.__output(f"{colorama.Fore.GREEN}SUCCESS{colorama.Fore.RESET}", str(out))

    def warn(self, out):
        """输出警告信息的方法"""
        if self.__level < levels["WARN"]:
            return
        self.__output(f"{colorama.Fore.YELLOW}WARN{colorama.Fore.RESET}", str(out))

    def error(self, out):
        """输出错误信息的方法"""
        if self.__level < levels["ERROR"]:
            return
        self.__output(f"{colorama.Fore.RED}ERROR{colorama.Fore.RESET}", str(out))

    def input(self, out):
        """普通输入的方法"""
        out = str(out)
        now = time.localtime()
        for i in out.split('\n')[:-1]:
            self.stdout.write(
                colorama.Fore.RESET + f"{time.strftime(self.time_format, now)}"
                + f"[{colorama.Fore.MAGENTA}INPUT{colorama.Fore.RESET}]" + i + '\n')
        stdin = sys.stdin
        sys.stdin = self.stdin
        result = input(colorama.Fore.RESET + f"{time.strftime(self.time_format, now)}"
                       + f"[{colorama.Fore.MAGENTA}INPUT{colorama.Fore.RESET}]" + out.split('\n')[-1])
        sys.stdin = stdin
        return result

    def password(self, out):
        """无回响输入的方法"""
        out = str(out)
        now = time.localtime()
        stdout, stdin = sys.stdout, sys.stdin
        sys.stdout, sys.stdin = self.stdout, self.stdin
        for i in out.split('\n')[:-1]:
            print(
                colorama.Fore.RESET + f"{time.strftime(self.time_format, now)}"
                + f"[{colorama.Fore.MAGENTA}PASSWD{colorama.Fore.RESET}]" + i)
        result = getpass.getpass(
            colorama.Fore.RESET + f"{time.strftime(self.time_format, now)}"
            + f"[{colorama.Fore.MAGENTA}PASSWD{colorama.Fore.RESET}]"
            + out.split('\n')[-1])
        sys.stdout, sys.stdin = stdout, stdin
        return result
