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


def set_mirror(mirror):
    url = mirrors[mirror]
    host = urlparse(url).hostname
    set_ini_keys(pip, {"global": {"index-url": url}, "install": {"trusted-host": host}})
    if shutil.which("uv"):
        set_uv_index(uv, url)
    print("设置成功")


def remove_mirror():
    remove_ini_keys(pip, {"global": {"index-url"}, "install": {"trusted-host"}})
    if shutil.which("uv"):
        remove_uv_index(uv)
    print("设置成功")


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--source")
    arg = parser.parse_args().source
    if arg in mirrors:
        set_mirror(arg)
    elif arg == "pypi":
        remove_mirror()
    else:
        options = ["官方", *mirrors, "退出"]
        print("使用此工具可切换pip镜像源\n" + "\n".join([f"{index}、{item}" for index, item in enumerate(options)]))
        while True:
            opt = input("请输入序号: ")
            if opt in tuple(map(str, range(len(options)))):
                if opt == "0":
                    remove_mirror()
                elif opt != str(len(options) - 1):
                    set_mirror(options[int(opt)])
                break
            else:
                print("不支持操作选项! 请输入正确序号")
