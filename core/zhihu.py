import time
import typing
from selenium import webdriver


class ZhihuZhuanlan:
    def __init__(self, title: str, body: str):
        self.title = title
        self.body = body

    def __repr__(self):
        return f'Title = {self.title}, Body = {self.body}\n'


class ZhihuAnswer:
    def __init__(self, body: str):
        self.body = body

    def __repr__(self):
        return f'{self.body}\n'


class ZhihuQuestion:
    def __init__(self, title: str, body: str, answers: [ZhihuAnswer]):
        self.title = title
        self.body = body
        self.answers = answers

    def __repr__(self):
        result = f'Title = {self.title}, Body = {self.body}\n'
        for answer in self.answers:
            result += f' - {answer}'
        result += '\n'
        return result


class NewWindow:
    def __init__(self, driver, url):
        self.driver = driver
        self.url = url
        self.prev_window = None

    def __enter__(self):
        self.prev_window = self.driver.current_window_handle

        self.driver.execute_script(f"window.open('{self.url}', 'new');")
        self.driver.switch_to.window(f'new')

    def __exit__(self, type, value, traceback):
        self.driver.close()
        self.driver.switch_to.window(self.prev_window)


class Zhihu:
    URL_PREFIX_ZHUANLAN = 'https://zhuanlan.zhihu.com/p/'
    URL_PREFIX_QUESTION = 'https://www.zhihu.com/question/'

    def __init__(self, search_page_num=1, qa_page_num=1, headless=True):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
            options.add_argument('--log-level=3')

        self._driver = webdriver.Chrome(chrome_options=options)

        self.search_page_num = search_page_num
        self.qa_page_num = qa_page_num

    @staticmethod
    def get_search_url(keyword: str) -> str:
        return f'https://www.zhihu.com/search?type=content&q={keyword}'

    def _search(self, keyword: str):
        url = Zhihu.get_search_url(keyword)
        self._driver.get(url)

    def _scroll_to_bottom(self):
        self._driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")

    def load_more_by_scroll_down(self, additional_page_num=1):
        for _ in range(additional_page_num):
            self._scroll_to_bottom()
            while len(self._driver.find_elements_by_class_name('PlaceHolder')) > 0:
                time.sleep(1)

    def get_search_results(self, keyword: str) -> typing.Iterator[str]:
        self._search(keyword)
        self.load_more_by_scroll_down(self.search_page_num - 1)

        items = self._driver.find_elements_by_class_name('ContentItem-title')
        for item in items:
            a = item.find_element_by_tag_name('a')
            href = a.get_attribute('href')
            yield href

    def fetch_content(self, url):
        if url.startswith(Zhihu.URL_PREFIX_ZHUANLAN):
            return self.fetch_zhuanlan_by_url(url)
        elif url.startswith(Zhihu.URL_PREFIX_QUESTION):
            return self.fetch_qa_by_url(url)
        else:
            return f'Not supported URL: {url}'

    def fetch_qa_by_url(self, url: str):
        id = url[len(Zhihu.URL_PREFIX_QUESTION):]
        if '/' in id:
            id = id[:id.find('/')]
        return self.fetch_qa_by_id(id)

    def fetch_zhuanlan_by_url(self, url: str):
        id = url[len(Zhihu.URL_PREFIX_ZHUANLAN):]
        return self.fetch_zhuanlan_by_id(id)

    def fetch_qa_by_id(self, id: str):
        url = Zhihu.URL_PREFIX_QUESTION + id
        with NewWindow(self._driver, url):
            self.load_more_by_scroll_down(self.qa_page_num - 1)

            title = self._driver.find_element_by_class_name('QuestionHeader-title').get_attribute('textContent')
            body = self._driver.find_element_by_class_name('QuestionHeader-detail').get_attribute('textContent')

            answers = []
            answer_root_el = self._driver.find_element_by_id(
                'QuestionAnswers-answers')

            for item in answer_root_el.find_elements_by_class_name('List-item'):
                try:
                    answer_body = item.find_element_by_class_name(
                        'RichContent-inner').get_attribute('textContent')
                    answers.append(ZhihuAnswer(answer_body))
                except:
                    pass

            return (id, ZhihuQuestion(title, body, answers))

    def fetch_zhuanlan_by_id(self, id: str):
        url = Zhihu.URL_PREFIX_ZHUANLAN + id
        with NewWindow(self._driver, url):
            title = self._driver.find_element_by_class_name('Post-Title').get_attribute('textContent')
            body = self._driver.find_element_by_class_name(
                'Post-RichTextContainer').get_attribute('textContent')

            return (id, ZhihuZhuanlan(title, body))
