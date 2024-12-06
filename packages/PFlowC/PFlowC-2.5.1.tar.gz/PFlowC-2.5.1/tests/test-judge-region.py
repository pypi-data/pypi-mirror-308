# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2024/8/28
@Software: PyCharm
@disc:
======================================="""
from PFlowC.geo_proxy import LOCAL_REGION_CODE

from PFlowC.utils.net import is_domestic2

if __name__ == '__main__':
    print(is_domestic2("blog.0p.fit", LOCAL_REGION_CODE))
