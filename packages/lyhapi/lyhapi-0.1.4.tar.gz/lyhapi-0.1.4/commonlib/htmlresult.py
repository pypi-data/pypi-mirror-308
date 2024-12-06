# coding=utf-8
"""
Author：Vissy Zhu
 生成HTML测试报告
"""

from HTMLTestRunner import HTMLTestRunner
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

def result(title):
    filename = 'result.html'
    fp = open(filename, 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=title, description=u'用例执行情况：')
    return runner, fp  # 为什么要返回fp呢，因为调用这个方法的时候，还没有执行用例，所以返回fp，执行完用例，在关闭文件。
