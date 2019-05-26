import os
from core.zhihu import Zhihu, ZhihuQuestion, ZhihuZhuanlan


def fetch_kw(keyword: str, save_to: str, search_page_num: int, qa_page_num: int, show_browser: bool):
    zhihu = Zhihu(search_page_num, qa_page_num, not show_browser)

    zhuanlan_count = 0
    qa_count = 0

    for url in zhihu.get_search_results(keyword):
        try:
            print('处理中:', url, '...')
            id, result = zhihu.fetch_content(url)
            print('已完成:', url)
        except Exception as e:
            print('解析失败:', url, '（很可能是因为没有答案）')
            print(e)
            continue

        print('保存中...')

        if isinstance(result, ZhihuZhuanlan):
            zhuanlan_count += 1
            print('第', zhuanlan_count, '个专栏:', result.title)
            with open(os.path.join(save_to, f'专栏 {id}.txt'), 'w', encoding='utf-8') as f:
                f.write(f'{result.title}\n\n{result.body}')
        elif isinstance(result, ZhihuQuestion):
            qa_count += 1
            print('第', qa_count, '个问题:', result.title)
            with open(os.path.join(save_to, f'问答 {id}.txt'), 'w', encoding='utf-8') as f:
                f.write(
                    f'{result.title}\n\n{result.body}\n=============================\n\n')
                answer_count = 0
                for answer in result.answers:
                    answer_count += 1
                    f.write(
                        f'答案 {answer_count}\n----------------------------\n\n')
                    f.write(f'{answer.body}\n\n')

        print('已保存\n')
