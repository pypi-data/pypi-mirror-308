# -*-coding:utf-8-*-
"""
Created on 2024/11/13

@author: 臧韬

@desc: 默认描述
"""

from setuptools import setup, find_packages

VERSION = '1.0.0'
DESCRIPTION = '极态官方授权Api的SDK'
LONG_DESCRIPTION = '极态官方授权Api的SDK，可以方便快捷地接入并使用哪些经过授权的API接口'

# 配置
setup(
    # 名称必须匹配文件名 'verysimplemodule'
    name="wanyun_JitSdk",
    version=VERSION,
    author="zangtao",
    author_email="noguchisyou123456@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[
        "requests"
    ],

    keywords=['python', 'jit', "sdk", "apiAuth"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
    ]
)
