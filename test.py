import requests
import json


def getData(limit=11):
    def fetchData(sentPage):
        return requests.get(f'https://jsonmock.hackerrank.com/api/articles?page={sentPage}')
    page = 1
    res = []
    totalPages = 1
    while page <= totalPages:
        print(page, ': page')
        data = fetchData(page).json()
        totalPages = data["total_pages"]
        articles = data['data']
        for item in articles:
            if (item['title'] == '' or item['title'] == None) and (item['story_title'] == '' or item['story_title']) or item['num_comments'] == None: continue
            elif item['title'] == None:
                res.append((item['story_title'], item['num_comments']))
            else:
                res.append((item['title'], item['num_comments']))
        page += 1
    print(res.sort(key=lambda x: (x[1], x[0]), reverse=True))
    # res.sort(key = lambda x: x[0])
    return [x for x, v in res[:limit]]


print(getData())
