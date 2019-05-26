import os
from core.zhihu import Zhihu, ZhihuQuestion, ZhihuZhuanlan
from core.core import fetch_kw

##########################
#                        #
# 下面是一堆可以改的东西 #
#                        #
##########################

关键词列表 = ['知乎脑残', '知乎变态']

搜索页面数 = 1      # 即：下拉次数 = 1
问答页面数 = 1      # 即：下拉次数 = 1

保存到目录 = 'D:/zhihu' # 目录要用/而不是\

显示浏览器 = False  # 相信我，你不会想显示的，虽然很炫。设置True显示，设置False不显示。

##########################
#                        #
# 下面是一堆不能改的东西 #
#                        #
##########################


def main():
    if not os.path.exists(保存到目录):
        os.mkdir(保存到目录)

    for keyword in 关键词列表:
        print('搜索关键词:', keyword)

        root_path = os.path.join(保存到目录, keyword)
        if not os.path.exists(root_path):
            os.mkdir(root_path)

        print('保存到:', root_path)

        fetch_kw(keyword, root_path, 搜索页面数, 问答页面数, 显示浏览器)

    print('全部完成！')


if __name__ == '__main__':
    main()
