"""查找 Node.js 程序，解决“已安装但旧启动窗口的 PATH 还没刷新”的情况。

ima 官方接口用 JavaScript 实现，需要 Node.js 执行。Python 的 shutil.which
通常只看当前进程的 PATH（可执行程序搜索目录），不会自动刷新系统配置。
因此：先尊重 PATH；找不到时，再检查几个常见的 Windows 安装位置。
本模块只找程序，不下载软件、不联网、不修改系统 PATH。
"""

from pathlib import Path
import os
import shutil


def find_node() -> str | None:
    """返回可执行文件路径；找不到返回 None，让调用者给出中文提示。

    str | None 表示返回值可能是字符串，也可能为空。每次调用都重新检查，
    不使用缓存，因此安装好后即使原页面进程还在，也有机会找到新程序。
    """
    executable = shutil.which("node")
    if executable:
        return executable

    # LOCALAPPDATA 是当前用户的本地应用目录；ProgramFiles 是系统程序目录。
    # 这里只读取系统变量，不更改它们。某个变量不存在时，跳过对应位置。
    locations = [
        ("LOCALAPPDATA", "Programs/nodejs/node.exe"),
        ("ProgramFiles", "nodejs/node.exe"),
        ("ProgramFiles(x86)", "nodejs/node.exe"),
    ]
    for variable, relative_path in locations:
        base = os.environ.get(variable)
        if base:
            candidate = Path(base) / relative_path
            if candidate.is_file():
                # 后续 subprocess 使用这个绝对位置，不需要通过 shell 拼命令。
                return str(candidate)
    return None
