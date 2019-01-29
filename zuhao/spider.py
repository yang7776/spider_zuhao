import requests
import telnetlib
import random
import json
import pymongo
import time
from multiprocessing import Process, Lock
from threading import Thread
from lxml import etree
from copy import deepcopy

user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
follows_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}'
followers_url = 'https://www.zhihu.com/api/v4/members/{user}/followers?include={include}&offset={offset}&limit={limit}'
start_user = 'chen-jun-15-6'
user_query = 'locations,employments,gender,educations,business,voteup_count,thanked_Count,follower_count,following_count,cover_url,following_topic_count,following_question_count,following_favlists_count,following_columns_count,answer_count,articles_count,pins_count,question_count,commercial_question_count,favorite_count,favorited_count,logs_count,marked_answers_count,marked_answers_text,message_thread_token,account_status,is_active,is_force_renamed,is_bind_sina,sina_weibo_url,sina_weibo_name,show_sina_weibo,is_blocking,is_blocked,is_following,is_followed,mutual_followees_count,vote_to_count,vote_from_count,thank_to_count,thank_from_count,thanked_count,description,hosted_live_count,participated_live_count,allow_message,industry_category,org_name,org_homepage,badge[?(type=best_answerer)].topics'
follows_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'
followers_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
}
MONGO_URI = 'localhost'
MONGO_DATABASE = 'zhihu'
collection_name = ['zhihu1', 'zhihu2', 'zhihu3', 'zhihu4', 'zhihu5']
zhihu = []
proxies = None
lock = Lock()
urlSet = set()
n = 0
proxies1 = None
a = []
task = [['103.106.32.245', '35711'], ['103.43.43.52', '23500'], ['103.219.205.80', '47727'], ['101.236.37.164', '8866'], ['103.47.175.215', '58255'], ['222.210.158.54', '8118'], ['103.218.134.17', '40250'], ['59.32.37.246', '61234'], ['221.227.185.250', '8118'], ['101.236.32.8', '8866'], ['61.160.247.63', '808'], ['103.58.249.248', '23500'], ['220.143.106.114', '80'], ['103.206.103.190', '23500'], ['101.236.57.136', '8866'], ['101.236.45.18', '8866'], ['101.236.61.59', '8866'], ['103.209.140.73', '57941'], ['116.7.176.75', '8118'], ['175.6.2.174', '8088'], ['103.106.35.17', '49299'], ['103.103.52.53', '49650'], ['180.118.243.234', '61234'], ['103.87.206.77', '61556'], ['180.118.243.234', '61234'], ['103.87.206.77', '61556'], ['103.196.211.96', '23500'], ['119.254.94.123', '60271'], ['167.250.191.158', '53281'], ['105.235.197.178', '30631'], ['115.46.89.12', '8123'], ['138.97.145.82', '49576'], ['221.210.51.174', '8118'], ['218.86.139.56', '80'], ['218.5.109.35', '8000'], ['103.36.100.23', '8080'], ['103.58.251.175', '39312'], ['124.243.226.18', '8888'], ['103.92.154.202', '46351'], ['80.211.72.103', '3128'], ['103.87.171.231', '58579'], ['219.145.170.23', '8888'], ['101.236.38.145', '8866'], ['180.110.5.18', '3128'], ['180.118.243.252', '61234'], ['180.118.241.192', '61234']]

# 获取免费代理
def getFreeProxy1():
    while True:
        # for i in range(1, 6):
        #     proxy += '?page = {}'.format(i)
        proxy = 'http://ip.jiangxianli.com'
        proxy += '?page={}'.format(str(random.randint(1, 4)))
        print(proxy)
        res = requests.get(proxy)
        response = etree.HTML(res.content)
        urlText = response.xpath('//tbody/tr/td/child::node()[2]/@data-url')
        print(urlText)

        for url in urlText:
            def urlTask(url):
                path = url.split('/')[2].split(':')[0]
                port = url.split('/')[2].split(':')[1]
                print(path, port)
                try:
                    telnetlib.Telnet(path, port, timeout=3)
                except:
                    return False
                else:
                    return True

            # url = urlText[random.randint(0, len(urlText) - 1)]
            if urlTask(url):
                use_proxy = {url.split(':')[0]: url}
                return use_proxy

def getFreeProxy():
    global n
    proxy = 'http://www.ip3366.net/free/?stype=1&page={pages}'
    li = []
    for i in range(1, 8):
        li.append(proxy.format(pages=i))
    for url in li:
        print(url)
        if n > 3 or proxies1 is None:
            proxies = getFreeProxy1()
            n = 0
        else:
            n += 1
        print(proxies)
        res = requests.get(url, proxies=proxies, headers=headers)
        response = etree.HTML(res.content)
        tree = response.xpath('//tbody/tr/td/text()')
        for i in range(15):
            try:
                index = 3 + i*7
                if tree[index] == 'HTTPS':
                    a.append([tree[index-3], tree[index-2]])
            except:
                pass
            finally:
                print(a)

def taskurl():
    for url in task:
        def urlTask(url):
            path = url[0]
            port = url[1]
            print(path, port)
            try:
                telnetlib.Telnet(path, port, timeout=3)
            except:
                return False
            else:
                return True

        # url = urlText[random.randint(0, len(urlText) - 1)]
        if urlTask(url):
            use_proxy = {'https': 'https://{}:{}'.format(url[0], url[1])}
            return use_proxy

def get_resopnse(url, count):
    """
    获取API内容
    :param url:
    :return:
    """
    # global proxies
    try:
        # proxies = getFreeProxy()
        # print(proxies, type(proxies))
        proxies = taskurl()
        res = requests.get(url, proxies=proxies, headers=headers, verify=False)
        return res
    except:
        proxies = taskurl()
        res = requests.get(url, proxies=proxies, headers=headers, verify=False)
        return res


def notUrl(response):
    """
    检查用户信息是否已经获取
    :param response:
    :return:
    """
    result = json.loads(response.text)
    user = result.get('url_token')
    if user not in urlSet:
        urlSet.add(user)
        return True
    else:
        return False


# 程序入口
def start_requests():
    """
    获取用户信息
    :return:
    """
    # 获取用户信息API,并通过get_response获取API内容信息
    res_user = get_resopnse(user_url.format(user=start_user, include=user_query), count=[])
    print(res_user)
    res_follows = get_resopnse(follows_url.format(user=start_user, include=follows_query, limit=20, offset=0), count=[])
    res_followers = get_resopnse(followers_url.format(user=start_user, include=followers_query, limit=20, offset=0), count=[])

    user = Thread(target=parse_user, args=(res_user,))
    follows = Thread(target=parse_follows, args=(res_follows,))
    followers = Thread(target=parse_followers, args=(res_followers,))

    user.start()
    follows.start()
    followers.start()


def parse_user(response):
    """
    获取用户详细信息，获取
    :param response:
    :return:
    """
    item = {
        'id': None,
        'name': None,
        'avatar_url': None,
        'headline': None,
        'description': None,
        'url': None,
        'url_token': None,
        'gender': None,
        'cover_url': None,
        'type': None,
        'badge': None,

        'answer_count': None,  # 回答数量
        'articles_count': None,  # 文章数量
        'commercial_question_count': None,  # 收费文章数量
        'favorite_count': None,  # 收藏数量
        'favorited_count': None,
        'follower_count': None,  # 粉丝数量
        'following_columns_count': None,
        'following_count': None,  # 关注人数
        'pins_count': None,
        'question_count': None,
        'thank_from_count': None,
        'thank_to_count': None,
        'thanked_count': None,
        'vote_from_count': None,
        'vote_to_count': None,
        'voteup_count': None,
        'following_favlists_count': None,
        'following_question_count': None,
        'following_topic_count': None,
        'marked_answers_count': None,
        'mutual_followees_count': None,
        'hosted_live_count': None,  # 主持的live数量
        'participated_live_count': None,  # 分享的live数量

        'locations': None,  # 地区
        'educations': None,  # 教育背景
        'employments': None  # 职业
    }
    try:
        result = json.loads(response.text)
        print(result)
    except json.decoder.JSONDecodeError:
        with open('exp.txt', 'a+') as ex:
            ex.write('json.decoder.JSONDecodeError')
    except:
        pass
    else:
        # 获取相应字段的信息并存入数据库
        item = deepcopy(item)
        for field in item.keys():
            if field in result.keys():
                item[field] = result.get(field)
        lock.acquire()
        client = pymongo.MongoClient(MONGO_URI)
        db = client[MONGO_DATABASE]
        db[collection_name[random.randint(0, 4)]].update({'url_token': item['url_token']}, dict(item), True)
        client.close()
        lock.release()

        res_follows = get_resopnse(follows_url.format(user=result.get('url_token'), include=follows_query, limit=20, offset=0), count=[])
        res_followers = get_resopnse(followers_url.format(user=result.get('url_token'), include=followers_query, limit=20, offset=0), count=[])

        follows = Thread(target=parse_follows, args=(res_follows,))
        followers = Thread(target=parse_followers, args=(res_followers,))
        follows.start()
        followers.start()


def parse_follows(response):
    try:
        results = json.loads(response.text)
    except json.decoder.JSONDecodeError:
        with open('exp.txt', 'a+') as ex:
            ex.write('json.decoder.JSONDecodeError')
    except:
        pass
    else:
        if 'data' in results.keys():
            for result in results.get('data'):
                res_user = get_resopnse(user_url.format(user=result.get('url_token'), include=user_query), count=[])
                if notUrl(res_user):
                    parse_user(res_user)

        if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
            next_page = results.get('paging').get('next')
            res_follows = get_resopnse(next_page, count=[])
            parse_follows(res_follows)


def parse_followers(response):
    try:
        results = json.loads(response.text)
    except json.decoder.JSONDecodeError:
        with open('exp.txt', 'a+') as ex:
            ex.write('json.decoder.JSONDecodeError')
    except:
        pass
    else:
        if 'data' in results.keys():
            for result in results.get('data'):
                # results.get('data')中包含关注该用户的人的url_toke,循环获取进行请求
                res_user = get_resopnse(user_url.format(user=result.get('url_token'), include=user_query), count=[])
                if notUrl(res_user):
                    parse_user(res_user)

        if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
            next_page = results.get('paging').get('next')
            res_followers = get_resopnse(next_page, count=[])
            parse_followers(res_followers)


if __name__ == "__main__":
    start_requests()