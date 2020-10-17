# @Time    : 2020/6/24 14:24
# @Author  : Hugh
# @Email   : 609799548@qq.com

import os
import sys
import shutil

WIN = sys.platform.startswith('win')

mirrors = {
    '阿里云源': ['[global]', 'index-url = https://mirrors.aliyun.com/pypi/simple',
             '[install]', 'trusted-host=mirrors.aliyun.com'],
    "清华源": ['[global]', 'index-url = https://pypi.tuna.tsinghua.edu.cn/simple',
            '[install]', 'trusted-host=pypi.tuna.tsinghua.edu.cn'],
    '豆瓣源': ['[global]', 'index-url = https://pypi.doubanio.com/simple',
            '[install]', 'trusted-host=pypi.doubanio.com']
}

user_home = os.path.expanduser('~')
pip_dir_name, pip_file_name = ('pip', 'pip.ini') if WIN else ('.pip', 'pip.conf')
pip_dir_path = os.path.join(user_home, pip_dir_name)
pip_file_path = os.path.join(user_home, pip_dir_name, pip_file_name)


def create_pip_file(mirror: str):
    if not os.path.exists(pip_dir_path):
        os.mkdir(pip_dir_path)
    with open(pip_file_path, 'w') as f:
        content = [item + '\n' for item in mirrors[mirror]]
        f.writelines(content)
    print('设置 %s 成功' % mirror)


def run():
    print('使用此工具可快速切换pip镜像源')
    print('0、官方源\n1、阿里源\n2、清华源\n3、豆瓣源\n4、退出')
    dic = {
        '1': '阿里云源', '2': '清华源', '3': '豆瓣源'
    }
    while True:
        opt = input('请输入序号: ')
        if opt in ['0', '1', '2', '3', '4']:
            if opt in '123':
                create_pip_file(dic[opt])
            elif opt == '0':
                if os.path.exists(pip_dir_path):
                    shutil.rmtree(pip_dir_path)
            break
        else:
            print('不支持操作选项!!! 请输入0-4')
    print('感谢您的使用~')


