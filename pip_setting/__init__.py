# @Author  : Hugh
# @Email   : 609799548@qq.com

import sys
import json
import shutil
import argparse
from pathlib import Path

WIN = sys.platform.startswith('win')
with (Path(__file__).parent / 'mirrors.json').open(encoding='utf') as f:
    mirrors = json.load(f)

pip = Path(f"~/{'pip/pip.ini' if WIN else '.pip/pip.conf'}").expanduser()
pip_dir = pip.parent


def new_file(mirror):
    if not pip_dir.exists():
        pip_dir.mkdir()
    with pip.open('w') as file:
        file.write('\n'.join([f'[{k}]\n{v}' for k, v in mirrors[mirror].items()]))
    print('设置成功')


def remove_pip():
    if pip_dir.exists():
        shutil.rmtree(pip_dir)
    print('设置成功')


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--source')
    arg = parser.parse_args().source
    if arg in mirrors:
        new_file(arg)
    elif arg == 'pypi':
        remove_pip()
    else:
        options = ['官方', *mirrors, '退出']
        print('使用此工具可切换pip镜像源\n' + '\n'.join([f'{index}、{item}' for index, item in enumerate(options)]))
        while True:
            opt = input('请输入序号: ')
            if opt in tuple(map(str, range(len(options)))):
                if opt == '0':
                    remove_pip()
                elif opt != str(len(options) - 1):
                    new_file(options[int(opt)])
                break
            else:
                print('不支持操作选项! 请输入正确序号')
