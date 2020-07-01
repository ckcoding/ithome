import requests
import json
import re
import datetime
import smtplib
import Crypto.Cipher.DES
# 更新时间 2020年6月30日14:48:58
# 使用说明：IT之家签到程序 安装python3，在cmd里输入pip install requests和pip install Crypto 然后改动代码里用户名和密码就可以了
# 原作者：https://github.com/daimiaopeng/IthomeQianDao

#优化者：https://github.com/ckjiexi
#优化新增，支持多账号签到
#优化新增：支持辣品签到，最会买签到！
#优化新增邮件通知

#需要注意的坑：
#pip install Crypto安装完如果提示，ModuleNotFoundError: No module named 'Crypto'
#那就去python3的安装目录Lib—-site-package中查看是否有Crypto文件夹，这时你应该看到有crypto文件夹，将其重命名为Crypto即可

def auto_fill(x):
    if len(x) > 24:
        raise "密钥长度不能大于等于24位"
    else:
        while len(x) < 32:
            x += "\0"
        return x.encode()

def getHash(text):
    key = "(#i@x*l%"
    x = Crypto.Cipher.DES.new(key.encode(), Crypto.Cipher.DES.MODE_ECB)
    a = x.encrypt(auto_fill(str(text))).hex()
    return str(a)

def sendEmail(mail_msg):
    from email.mime.text import MIMEText
    # email 用于构建邮件内容
    from email.header import Header
    # 用于构建邮件头
    # 发信方的信息：发信邮箱，QQ 邮箱授权码
    from_addr = 'kzddck@qq.com'
    password = 'bnleagufjxxebefa'
    # 收信方邮箱
    to_addr = '1209739382@qq.com'
    # 发信服务器
    smtp_server = 'smtp.qq.com'
    # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
    msg = MIMEText(mail_msg , 'plain', 'utf-8')
    # 邮件头信息
    msg['From'] = Header(from_addr)
    msg['To'] = Header(to_addr)
    msg['Subject'] = Header('it之家签到状态')
    # 开启发信服务，这里使用的是加密传输
    server = smtplib.SMTP_SSL(smtp_server)
    server.connect(smtp_server, 465)
    # 登录发信邮箱
    server.login(from_addr, password)
    # 发送邮件
    server.sendmail(from_addr, to_addr, msg.as_string())
    # 关闭服务器
    server.quit()

def run(username, password):
    session = requests.session()
    url_login = 'https://my.ruanmei.com/Default.aspx/LoginUser'
    data = {'mail': username, 'psw': password, 'rememberme': 'true'}
    header = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Length': '60',
        'Content-Type': 'application/json; charset=UTF-8',
        'Host': 'my.ruanmei.com',
        'Origin': 'http://my.ruanmei.com',
        'Pragma': 'no-cache',
        'Referer': 'http://my.ruanmei.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    try:
        response = session.post(url=url_login, data=json.dumps(data), headers=header).headers['Set-Cookie']
        user_hash = re.search(r'user=hash=[a-zA-Z0-9]{160,160}', response).group()[10:]
        md5 = getHash(str(datetime.date.today()))
        #it之家签到
        itapp_qiandao = 'https://my.ruanmei.com/api/UserSign/Sign?userHash=%s&type=0&endt=%s' % (user_hash, md5)
        itapp_qiandao = session.get(url=itapp_qiandao).json()
        print(itapp_qiandao)
        # 辣品签到
        lp_qiandao = 'https://my.ruanmei.com/api/UserSign/Sign?userHash=%s&type=1&endt=%s' % (user_hash, md5)
        lp_qiandao = session.get(url=lp_qiandao).json()
        print(lp_qiandao)
        # 最会买签到
        zhm_qiandao = 'https://my.ruanmei.com/api/UserSign/Sign?userHash=%s&type=3&endt=%s' % (user_hash, md5)
        zhm_qiandao = session.get(url=zhm_qiandao).json()
        print(zhm_qiandao)

    except:
        qiandao = "签到失败"
        sendEmail(qiandao)


my_list = [
    {
        'username': '账号1',
        'password': '密码',
    },
    {
        'username': '账号2',
        'password': '密码',
    },
    {
        'username': '账号3',
        'password': '密码',
    }
]
for i in my_list:
    run(i['username'], i['password'])