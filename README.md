# Zhihu Crawler

Use `selenium` with ChromeDriver.

Please install [ChromeDriver](http://chromedriver.chromium.org/) first and add its path to `PATH` environment variable.

## Usage

1. Edit parameters in `main.py`:

    ```py
    关键词列表 = ['知乎脑残', '知乎变态']

    搜索页面数 = 1      # 即：下拉次数 = 1
    问答页面数 = 1      # 即：下拉次数 = 1

    保存到目录 = 'D:/zhihu' # 目录要用/而不是\

    显示浏览器 = False  # 相信我，你不会想显示的，虽然很炫。设置True显示，设置False不显示。
    ```

2. Run `python main.py` and wait