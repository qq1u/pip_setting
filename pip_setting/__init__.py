import sys
import json
import shutil
import argparse
from pathlib import Path
from urllib.parse import urlparse

from .config import UTF8, set_ini_keys, remove_ini_keys, set_uv_index, remove_uv_index

WIN = sys.platform.startswith("win")
with (Path(__file__).parent / "mirrors.json").open(encoding=UTF8) as f:
    mirrors = json.load(f)
pip = Path(f"~/{'pip/pip.ini' if WIN else '.pip/pip.conf'}").expanduser()
uv = Path(f"~/{'AppData/Roaming/uv/uv.toml' if WIN else '.config/uv/uv.toml'}").expanduser()


def targets(target):
    """实际写入的目标: 显式指定就用指定值; all 时 uv 以检测为准。"""
    if target != "all":
        return [target]
    return ["pip"] + (["uv"] if shutil.which("uv") else [])


def set_mirror(mirror, target="all"):
    url = mirrors[mirror]
    results = []
    if "pip" in targets(target):
        set_ini_keys(pip, {"global": {"index-url": url}, "install": {"trusted-host": urlparse(url).hostname}})
        results.append(f"pip: 已设置 {mirror} 镜像")
    if "uv" in targets(target):
        set_uv_index(uv, url)
        results.append(f"uv : 已设置 {mirror} 镜像")
    print("\n".join(results))


def remove_mirror(target="all"):
    results = []
    if "pip" in targets(target):
        remove_ini_keys(pip, {"global": {"index-url"}, "install": {"trusted-host"}})
        results.append("pip: 已恢复官方源")
    if "uv" in targets(target):
        remove_uv_index(uv)
        results.append("uv : 已恢复官方源")
    print("\n".join(results))


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--source")
    parser.add_argument("-p", "--target", choices=["pip", "uv", "all"], default="all",
                        help="操作目标: pip、uv 或 all (默认 all, 检测到 uv 时同步设置）")
    arg = parser.parse_args()
    if arg.source in mirrors:
        set_mirror(arg.source, arg.target)
    elif arg.source == "pypi":
        remove_mirror(arg.target)
    else:
        options = ["官方", *mirrors, "退出"]
        ts = targets(arg.target)
        print(f"使用此工具可切换 {' 和 '.join(ts)} 的镜像源\n"
              + "\n".join(f"{i}、{item}" for i, item in enumerate(options)))
        while True:
            opt = input("请输入序号: ")
            if opt in tuple(map(str, range(len(options)))):
                if opt == "0":
                    remove_mirror(arg.target)
                elif opt != str(len(options) - 1):
                    set_mirror(options[int(opt)], arg.target)
                break
            else:
                print("不支持操作选项! 请输入正确序号")
