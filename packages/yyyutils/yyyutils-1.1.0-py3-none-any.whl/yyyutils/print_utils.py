import inspect
import builtins
import sys
import re
from colorama import Fore, Style, init

# 初始化 colorama
init(autoreset=False)  # 将 autoreset 设置为 False，以便手动控制颜色


class Tee(object):
    """
    将输出同时输出到多个终端
    """

    def __init__(self, *terminals):
        self.terminals = terminals

    def __remove_ansi_escape_sequences(self, text):
        ansi_escape = re.compile(r'\x1B\[[0-?9;]*[mGKF]')  # 正则表达式匹配ANSI序列
        return ansi_escape.sub('', text)

    def write(self, obj):
        self.terminals = list(self.terminals)
        for f in self.terminals:
            if isinstance(obj, str):
                obj = self.__remove_ansi_escape_sequences(obj)
            f.write(obj)
            f.flush()

    def flush(self):
        for f in self.terminals:
            f.flush()


class PrintUtils:
    """
    自定义print函数，可以添加文件名、类名、函数名、行号、时间，以及手动控制文字颜色
    """
    original_print = print

    def __init__(self, add_line=True, add_file=False, add_class=False, add_func=False, add_time=False, flush=False,
                 use_tee=False, terminals=()):
        self.add_line = add_line
        self.add_file = add_file
        self.add_func = add_func
        self.add_time = add_time
        self.add_class = add_class
        self.flush = flush
        self.__enable = True
        self.__current_color = ''
        self.__skip_file_write = False  # 新增标志

        self.tee = None
        if use_tee and terminals:
            self.tee = Tee(*terminals if isinstance(terminals, (list, tuple)) else (terminals,))

        self.__replace_print()

    def __custom_print(self, *args, **kwargs):
        if not self.__enable:
            return PrintUtils.original_print(*args, **kwargs)

        string = ""
        frame = self.__get_frame()
        PrintUtils.original_print(frame)

        if frame:
            if self.add_file:
                file_name = frame.f_code.co_filename
                string += f"F--{file_name}, "
            if self.add_class:
                class_name = frame.f_locals.get('self', None).__class__.__name__
                if class_name:
                    string += f"C--{class_name}, "
            if self.add_func:
                func_name = frame.f_code.co_name
                string += f"Fu--{func_name}, "
            if self.add_line:
                line_number = frame.f_lineno
                string += f"L--{line_number}, "
        if self.add_time:
            import time
            now_time = time.strftime("%H:%M:%S", time.localtime())
            string += f"T--{now_time}, "
        string = string[:-2] + "：" if string else ""

        sep = kwargs.pop('sep', ' ')
        end = kwargs.pop('end', '\n')

        output = self.__current_color + string + sep.join(map(str, args)) + Style.RESET_ALL

        PrintUtils.original_print(output, end=end, flush=self.flush, **kwargs)

        if self.tee and not self.__skip_file_write:
            self.tee.write(output + end)

        self.__skip_file_write = False  # 重置标志

    def __get_frame(self):
        """安全地获取调用栈信息"""
        try:
            frame = inspect.currentframe()
            while frame:
                if frame.f_code.co_filename != __file__:
                    return frame
                frame = frame.f_back
        except Exception:
            pass
        return None

    def set_color(self, color):
        """设置文字颜色"""
        if color.lower() == 'red':
            self.__current_color = Fore.RED
        elif color.lower() == 'green':
            self.__current_color = Fore.GREEN
        elif color.lower() == 'blue':
            self.__current_color = Fore.BLUE
        elif color.lower() == 'yellow':
            self.__current_color = Fore.YELLOW
        else:
            self.__current_color = ''

    def reset_color(self):
        """重置文字颜色"""
        self.__current_color = ''

    def disable(self):
        self.__enable = False
        self.__restore_print()

    def enable(self):
        self.__enable = True
        self.__replace_print()

    def toggle_tee(self, *terminals):
        """切换Tee的启用状态"""
        if self.tee:
            self.tee = None
            self.__skip_file_write = True  # 设置标志
            print("Tee已禁用，当前使用普通打印。")
        elif terminals:
            self.tee = Tee(*terminals)
            self.__skip_file_write = True  # 设置标志
            print("Tee已启用。")
        else:
            print("请提供输出终端以启用Tee。")

    def __replace_print(self):
        builtins.print = self.__custom_print

    def __restore_print(self):
        builtins.print = PrintUtils.original_print

    def __del__(self):
        """析构函数，确保在对象被销毁时恢复原始的print函数"""
        self.__restore_print()


class TestClass:
    def test(self):
        print("红色")


# 示例使用
if __name__ == '__main__':
    file = open('output.txt', 'w', encoding='utf-8')
    pr = PrintUtils(add_line=True, add_class=True, add_func=True, add_time=True, use_tee=True, terminals=(file,))
    op = PrintUtils.original_print
    print(12435344523465432)
    file.close()
