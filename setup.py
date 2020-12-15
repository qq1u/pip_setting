import setuptools
from distutils.core import setup

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='pip-setting',
    version='0.0.4',
    author='丘家劲',
    author_email='609799548@qq.com',
    description='快速设置pip镜像源的工具',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT Licence',
    url='https://github.com/13528080556/pip_setting',
    entry_points={
        'console_scripts': [
            'pip-setting=pip_setting:run',
            'pip_setting=pip_setting:run',
            'pip3-setting=pip_setting:run',
            'pip3_setting=pip_setting:run'
        ]
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
