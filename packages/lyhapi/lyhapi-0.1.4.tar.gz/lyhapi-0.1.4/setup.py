# coding=utf-8
"""
Author：Vissy Zhu
"""
from setuptools import setup, find_packages
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
setup(
    name="lyhapi",
    version="0.1.4",
    author="Vissy Zhu",
    author_email="1209354095@qq.com",
    description="lyhapi_autoTest",
    url="https://gitee.com/vissy/lyhapi.git",
    license='MIT',
    packages=find_packages(),
    # zip_safe=False
)
