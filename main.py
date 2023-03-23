import requests
from pprint import pprint
from collections import namedtuple
from bs4 import BeautifulSoup

Column = namedtuple("Column", ["name", "uuid", "updated"])
Story = namedtuple("Story", ['author', 'title', 'updated', 'editor', 'id', 'url'])


header = {
    "user-agent": "okhttp/4.2.0 Build/1.0 (xiaomi; Redmi Note 7 Pro; Android 10) Emulator/2.0 (false) Mozilla/5.0 ("
                  "Linux; Android 10; Redmi Note 7 Pro Build/QKQ1.190915.002; wv) AppleWebKit/537.36 (KHTML, "
                  "like Gecko) Version/4.0 Chrome/81.0.4044.138 Mobile Safari/537.36 CDAndroid/7.6.17 (xiaomi; "
                  "6000052) "
}


def get_columns():
    url = "https://enapp.chinadaily.com.cn/channels/enapp/custom-columns.json"
    res_json = requests.get(url, headers=header).json()
    columns_list = []
    for col in res_json:
        column = Column(
            name=col["name"],
            uuid=col["uuid"],
            updated=col["updated"]
        )
        columns_list.append(column)
    # return {item["name"]: item["uuid"] for item in res.json()}
    return columns_list


def get_stories(column_uuid):
    url = f"https://enapp.chinadaily.com.cn/channels/enapp/columns/{column_uuid}/stories.json"
    res_json = requests.get(url, headers=header).json()
    res_story = []

    for st in res_json['stories']:
        story = Story(author=st["author"],
                      title=st["title"],
                      updated=st["updated"],
                      editor=st["editor"],
                      id=st["id"],
                      url=st["url"])
        res_story.append(story)

    return res_story


def get_content(story: Story):
    url = story.url.replace(".html", ".json")
    res_json = requests.get(url, headers=header).json()
    content_html = BeautifulSoup(res_json['content'], features="lxml")

    article_content = "\n\n".join(item.text for item in content_html.find_all("p"))
    article_content = f"{story.title}\n\n" + article_content

    return article_content


if __name__ == '__main__':
    import os

    columns = get_columns()
    for i, col in enumerate(columns):
        print(f"{i}. {col.name}")

    print("请输入你需要的栏目")
    need = input()
    col_id = columns[int(need)].uuid

    os.system("cls")

    articles = get_stories(col_id)

    for i, art in enumerate(articles):
        print(f"{i}. {art.title}  最近更新:{art.updated[:10]}")

    print("请输入你需要的文章")
    need = input()
    art = articles[int(need)]

    os.system("cls")

    print(get_content(art))
