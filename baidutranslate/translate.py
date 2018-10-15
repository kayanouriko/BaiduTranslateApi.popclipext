import os
import urllib.parse
import urllib.request
import hashlib
import json
import argparse
import _thread

translateDic = {
    '自动检测': 'auto',
	'中文': 'zh',
	'英语': 'en',
	'粤语': 'yue',
	'文言文': 'wyw',
	'日语': 'jp',
	'韩语': 'kor',
	'法语': 'fra',
	'西班牙语': 'spa',
	'泰语': 'th',
	'阿拉伯语': 'ara',
	'俄语': 'ru',
	'葡萄牙语': 'pt',
	'德语': 'de',
	'意大利语': 'it',
	'希腊语': 'el',
	'荷兰语': 'nl',
	'波兰语': 'pl',
	'保加利亚语': 'bul',
	'爱沙尼亚语': 'est',
	'丹麦语': 'dan',
	'芬兰语': 'fin',
	'捷克语': 'cs',
	'罗马尼亚语': 'rom',
	'斯洛文尼亚语': 'slo',
	'瑞典语': 'swe',
	'匈牙利语': 'hu',
	'繁体中文': 'cht',
	'越南语': 'vie',
}

errorCodeDic = {
    '52000': '成功',
    '52001': '请求超时-重试',
    '52002': '系统错误-重试',
    '52003': '未授权用户-检查您的 appid 是否正确，或者服务是否开通',
    '54000': '必填参数为空-检查是否少传参数',
    '54001': '签名错误-请检查您的签名生成方法',
    '54003': '访问频率受限-请降低您的调用频率',
    '54004': '账户余额不足-请前往管理控制平台为账户充值',
    '54005': '长query请求频繁-请降低长query的发送频率，3s后再试',
    '58000': '客户端IP非法-检查个人资料里填写的"IP地址"是否正确，可前往管理控制平台修改，IP限制，IP可留空',
    '58001': '译文语言方向不支持-检查译文语言是否在语言列表里',
}

# 请求api
def requestApiUrl(appid, appkey, fromlang, tolang, query):
    apiUrl = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
    q = query
    froml = translateDic[fromlang]
    tol = translateDic[tolang]
    appid = appid
    key = appkey
    salt = '1234567890' # 随机数
    sign = appid + q + salt + key
    md5 = hashlib.md5()
    md5.update(sign.encode('utf-8'))
    sign = md5.hexdigest()

    data = {'q': q, 'from': froml, 'to': tol, 'appid': appid, 'salt': salt, 'sign': sign}
    data = urllib.parse.urlencode(data).encode('utf-8')
    req = urllib.request.Request(apiUrl, data=data)
    hjson = json.loads(urllib.request.urlopen(req).read())
    return hjson

# 展示通知
def showNotification(title, content):
    os.system('osascript ./translate.scptd \"%s\" \"%s\"' % (title, content))
    

# main函数
def startTranslate(appid, appkey, fromlang, tolang, query):
    hjson = requestApiUrl(appid, appkey, fromlang, tolang, query)
    print('获取到的结果json', hjson)
    if 'trans_result' in hjson.keys():
        showNotification(hjson['trans_result'][0]['src'], hjson['trans_result'][0]['dst'])
    else:
        error_code = hjson['error_code']
        value = errorCodeDic[error_code]
        array = value.split('-')
        title = array[0] + '(错误码:' + error_code + ')'
        content = array[-1]
        showNotification(title, content)
    

# 入口
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--urikoappid', dest='urikoappid', nargs='?', default=None)
    parser.add_argument('--urikokey', dest='urikokey', nargs='?', default=None)
    parser.add_argument('--urikofrom', dest='urikofrom', nargs='?', default=None)
    parser.add_argument('--urikoto', dest='urikoto', nargs='?', default=None)
    parser.add_argument('--urikoquery', dest='urikoquery', nargs='?', default=None)
    args = parser.parse_args()
    appid = args.urikoappid
    appkey = args.urikokey
    fromlang = args.urikofrom
    tolang = args.urikoto
    query = args.urikoquery

    startTranslate(appid, appkey, fromlang, tolang, query)
    
    

