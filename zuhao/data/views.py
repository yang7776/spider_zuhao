from django.shortcuts import render
import os, urllib3, json
from django.http.response import HttpResponse
# Create your views here.

# 定义函数完成页面渲染
def show_zuhao(request):
    return render(request, 'zuhao.html')

# 定义函数完成详情页的渲染
def show_zuhao_good(request):
    return render(request, 'zu_good.html')

# 定义函数完成用户详情页渲染
def user_detail(request):
    return render(request, 'detail_info.html')

# 定义函数完成zuhao页面数据的获取
def get_zuhao_data(request):
    if not os.path.exists(os.path.join(os.path.dirname(__file__), 'json_data/zuhao.json')):
        json_data = request_data('https://www.zuhaowan.com/appv3/Game/hotList', 'post')
        with open(os.path.join(os.path.dirname(__file__), 'json_data/zuhao.json'), 'w') as f:
            f.write(json_data)
    else:
        with open(os.path.join(os.path.dirname(__file__), 'json_data/zuhao.json'), 'r') as f:
            json_data = f.read()
    return HttpResponse(json_data)

# 定义通用函数完成指定网站的获取
def request_data(url, method, fields=None):
    headers = {'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    # 构建http请求池对象
    http = urllib3.PoolManager()
    # 发送网络请求
    res = http.request(method, url, fields= fields, headers=headers)
    return res.data.decode()

# 定义函数完成租号页面二级页面数据的获取
def get_zuhao_ifnor_data(request):
    gameId = request.GET.get('gameId')
    page = request.GET.get('page')
    if not os.path.exists(os.path.join(os.path.dirname(__file__), 'json_data/{0}_{1}.json'.format(gameId, page))):
        datas = request_data('https://www.zuhaowan.com/Appv2/Search/searchRent', 'post', fields={'gameId': gameId, 'page': page})
        count = int(json.loads(datas).get('count'))
        pageSize = json.loads(datas).get('pageSize')
        if (count//pageSize+1) >= int(page):
            with open(os.path.join(os.path.dirname(__file__), 'json_data/{0}_{1}.json'.format(gameId, page)), 'w') as f:
                f.write(datas)
            return HttpResponse(datas)
        else:
            return HttpResponse(json.dumps({'code': 400, 'msg': '对不起没有更多数据了'}))
    else:
        with open(os.path.join(os.path.dirname(__file__), 'json_data/{0}_{1}.json'.format(gameId, page)), 'r') as f:
            datas = f.read()
        return HttpResponse(datas)

# 定义函数完成三级页面数据的获取
def infor_three(request):
    userid = request.GET.get('userid')
    if not os.path.exists(os.path.join(os.path.dirname(__file__), 'json_data/{}.json'.format(userid))):
        datas = request_data('https://www.zuhaowan.com/Appv2/Search/actRentDetailNew', 'post',fields={'id':userid})
        with open(os.path.join(os.path.dirname(__file__), 'json_data/{0}.json'.format(userid)), 'w') as f:
            f.write(datas)
        return HttpResponse(datas)
    else:
        with open(os.path.join(os.path.dirname(__file__), 'json_data/{0}.json'.format(userid)), 'r') as f:
            datas = f.read()
        return HttpResponse(datas)


