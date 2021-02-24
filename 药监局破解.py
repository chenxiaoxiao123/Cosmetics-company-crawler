#首页药监局的信息是通过json动态得到的
#http://scxk.nmpa.gov.cn:81/xk/itownet/portalAction.do
#详情页的URL
# http://scxk.nmpa.gov.cn:81/xk/itownet/portal/dzpz.jsp?id=649e85b1c5db4a62a13173d8f65e9efc
# http://scxk.nmpa.gov.cn:81/xk/itownet/portal/dzpz.jsp?id=3185548fc3d545d68b3eb85a1a57c2dd
# 通过对详情页URL进行分析：
# URL的域名是一样的，只是携带的参数不同
# ID值可以从首页中对应的ajax请求到的json串中获取
# 域名和ID值拼接出一个完整的企业对应的详情页的URL
# 详情页的企业详情数据也是动态加载出来的
# http://scxk.nmpa.gov.cn:81/xk/itownet/portalAction.do?method=getXkzsById
# http://scxk.nmpa.gov.cn:81/xk/itownet/portalAction.do?method=getXkzsById
# 观察后发现：
#   所有的post请求的URL都是一样的，只有参数ID值是不同
#   如果我们可以批量获取多家企业的ID后，就可以将ID和URL形成一个完整详情页的URL

#   重点：批量获取ID

import requests
import json
if __name__ == "__main__":
    url = 'http://scxk.nmpa.gov.cn:81/xk/itownet/portalAction.do?method=getXkzsList'
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.74"
    }
    id_list = []  # 存储企业ID
    all_data_list = []

    #参数的封装
    for page in range(1,6):#将所有页数遍历
        page = str(page)
        data = {
            'on': 'true',
            'page': page ,
            'pageSize': '15',
            'productName':'',
            'conditionType': '1',
            'applyname':'',
            'applysn':''
        }
    # 伪装URL
    # headers = {
    #     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.74"
    # }
        json_ids = requests.post(url=url,headers=headers,data=data).json()
        # id_list = [] #存储企业ID
        for dic in json_ids['list']:
            id_list.append(dic['ID'])

    #获取企业详情数据
    # all_data_list = []
    post_url = 'http://scxk.nmpa.gov.cn:81/xk/itownet/portalAction.do?method=getXkzsById'
    for id in id_list:
        data = {
            'id':id
        }
        datail_json = requests.post(url=post_url,headers=headers,data=data).json()
        all_data_list.append(datail_json)
    #持久化存储
    fp = open('./yaojianju.json','w',encoding='utf-8')
    json.dump(all_data_list,fp=fp,ensure_ascii=False)
    print('over!!!')
