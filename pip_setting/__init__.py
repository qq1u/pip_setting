# @Author  : Hugh
# @Email   : 609799548@qq.com

import os
import sys
import shutil
import argparse

WIN = sys.platform.startswith('win')
ali = ('[global]', 'index-url = https://mirrors.aliyun.com/pypi/simple',
       '[install]', 'trusted-host=mirrors.aliyun.com')
qh = ('[global]', 'index-url = https://pypi.tuna.tsinghua.edu.cn/simple',
      '[install]', 'trusted-host=pypi.tuna.tsinghua.edu.cn')
db = ('[global]', 'index-url = https://pypi.doubanio.com/simple',
      '[install]', 'trusted-host=pypi.doubanio.com')
tx = ('[global]', 'index-url = https://mirrors.cloud.tencent.com/pypi/simple',
      '[install]', 'trusted-host=mirrors.cloud.tencent.com')

mirrors = {'aliyun': ali, 'qinghua': qh, 'douban': db, 'tencent': tx, '1': ali, '2': qh, '3': db, '4': tx}

user_home = os.path.expanduser('~')
pip_dir_name, pip_file_name = ('pip', 'pip.ini') if WIN else ('.pip', 'pip.conf')
pip_dir_path = os.path.join(user_home, pip_dir_name)
pip_file_path = os.path.join(user_home, pip_dir_name, pip_file_name)


def create_pip_file(mirror):
    if not os.path.exists(pip_dir_path):
        os.mkdir(pip_dir_path)
    with open(pip_file_path, 'w') as f:
        content = [item + '\n' for item in mirrors[mirror]]
        f.writelines(content)
    print('设置成功')


def remote_pip():
    if os.path.exists(pip_dir_path):
        shutil.rmtree(pip_dir_path)
    print('设置成功')


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--source')
    arg = parser.parse_args().source
    if arg in mirrors:
        create_pip_file(arg)
    elif arg == 'pypi':
        remote_pip()
    else:
        print('使用此工具可切换pip镜像源')
        print('0、官方源\n1、阿里源\n2、清华源\n3、豆瓣源\n4、腾讯源\n5、退出')
        while True:
            opt = input('请输入序号: ')
            if opt in ('0', '1', '2', '3', '4', '5'):
                if opt in '1234':
                    create_pip_file(opt)
                elif opt == '0':
                    remote_pip()
                break
            else:
                print('不支持操作选项! 请输入0-4')