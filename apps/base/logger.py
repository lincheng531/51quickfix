#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
log
~~~

This module customize the logging handler so that we can acheive a colorful output

Usage:

>>> import log
>>> logger = log.getlogger("TestLogger")
>>> logger.info("this is some information")
[time]<TestLogger>INFO:this is some  information

"""
import os
import logging
from settings import HOST_NAME,ENV

# 创建一个logger  
def getlogger(name):
    logger = logging.getLogger(name)  
    logger.setLevel(logging.DEBUG)  
      
    # 创建一个handler，用于写入日志文件  
    fh = logging.FileHandler('tlmq.log')  
    fh.setLevel(logging.DEBUG)  
      
    # 再创建一个handler，用于输出到控制台  
    ch = logging.StreamHandler()  
    ch.setLevel(logging.DEBUG)  
      
    # 定义handler的输出格式  
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  
    fh.setFormatter(formatter)  
    ch.setFormatter(formatter)  
      
    # 给logger添加handler  
    logger.addHandler(fh)  
    logger.addHandler(ch)  
    return logger
