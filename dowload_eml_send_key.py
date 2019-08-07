# coding=gbk
# import json
import sys
from datetime import datetime as dtlong
import poplib
# 解析邮件
import base64
import datetime
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
import time
# 解析消息头中的字符串
# 没有这个函数，print出来的会使乱码的头部信息。如'=?gb18030?B?yrXWpL3hufsueGxz?='这种
# 通过decode，将其变为中文
import requests
from flask import json


class Analysis():
    def decode_str(self,s):
        value, charset = decode_header(s)[0]
        if charset:
            value = value.decode(charset)
        return value
    # 解码邮件信息分为两个步骤，第一个是取出头部信息
    # 首先取头部信息
    # 主要取出['From','To','Subject']
    '''
    From: "=?gb18030?B?anVzdHpjYw==?=" <justonezcc@sina.com>
    To: "=?gb18030?B?ztLX1Ly6tcTTys/k?=" <392361639@qq.com>
    Subject: =?gb18030?B?dGV4dMTjusM=?=
    '''

    # 如上述样式，均需要解码
    def get_header(self,msg):
        subset={}
        for header in ['From', 'To', 'Subject']:
            value = msg.get(header, '')
            if value:
                # 文章的标题有专门的处理方法
                if header == 'Subject':
                    value = self.decode_str(value)
                    subset[header]=value
                    # print('主题：'+value)
                elif header in ['From', 'To']:
                    # 地址也有专门的处理方法
                    hdr, addr = parseaddr(value)
                    name = self.decode_str(addr)
                    # value = name + ' < ' + addr + ' > '
                    value = name
                    subset[header]=value
                    # print(value+'---------------')
            # print(header + ':' + value)
        # print(subset)
        return subset


    # 头部信息已取出


    # 获取邮件的字符编码，首先在message中寻找编码，如果没有，就在header的Content-Type中寻找
    def guess_charset(self,msg):
        charset = msg.get_charset()
        if charset is None:
            content_type = msg.get('Content-Type', '').lower()
            pos = content_type.find('charset=')
            if pos >= 0:
                charset = content_type[pos + 8:].strip()
        return charset


    # 邮件正文部分
    # 取附件
    # 邮件的正文部分在生成器中，msg.walk()
    # 如果存在附件，则可以通过.get_filename()的方式获取文件名称

    def get_file(self,msg):
        for part in msg.walk():
            filename = part.get_filename()
            if filename != None:  # 如果存在附件
                filename = self.decode_str(filename)  # 获取的文件是乱码名称，通过一开始定义的函数解码
                data = part.get_payload(decode=True)  # 取出文件正文内容
                # 此处可以自己定义文件保存位置
                path = filename
                f = open('F:'+path, 'wb')
                f.write(data)
                f.close()
                print(filename, 'download')


    def get_content(self,msg):
        for part in msg.walk():
            content_type = part.get_content_type()
            charset = self.guess_charset(part)
            # 如果有附件，则直接跳过
            if part.get_filename() != None:
                continue
            email_content_type = ''
            self.content = ''
            if content_type == 'text/plain':
                email_content_type = 'text'
            elif content_type == 'text/html':
                # print('html 格式 跳过')
                # continue  # 不要html格式的邮件
                email_content_type = 'html'
            if charset:
                try:
                    self.content = part.get_payload(decode=True).decode(charset)
                except AttributeError:
                    print('type error')
                except LookupError:
                    print("unknown encoding: utf-8")
            if email_content_type == '':
                continue
                # 如果内容为空，也跳过
            # print('---------------------')
            self.datatime=msg.get("Date")[0:24]
            # print('邮件发送时间：%s'%(self.datatime))
            date1 = time.strptime(msg.get("Date")[0:24], '%a, %d %b %Y %H:%M:%S')  # 格式化收件时间
            date2 = time.strftime("%Y-%m-%d %H:%M:%S", date1)  # 邮件时间格式转换
            print('邮件发送时间：%s' % date2)
            now_t = dtlong.now()
            li_time = dtlong.strftime(now_t,"%Y-%m-%d %H:%M:%S")
            tim_x=''.join(x for x in li_time)
            now_time=dtlong.strptime(tim_x, "%Y-%m-%d %H:%M:%S")
            print(now_time)
            a = dtlong.strptime(date2, "%Y-%m-%d %H:%M:%S")
            pass_one_time=(datetime.datetime.now() - datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
            # pass_one_time=tim_x[12]
            pass_time=''.join(y for y  in pass_one_time)
            pass_time = dtlong.strptime(pass_time, "%Y-%m-%d %H:%M:%S")
            # print(type(pass_one_time))
            if a >pass_time and a<now_time:
                eml_sine=1
                # print('邮件在范围内')
            else:
                eml_sine=0
                # print('邮件不在范围内')
            # print(now_time-a)
            # print(li_time-a)
            # print(date2)
            # print(email_content_type + ' -----  ' + self.content)
            # print('----------------------')
            return self.datatime,self.content,eml_sine


# get_file(msg)
if __name__ == '__main__':
    a=Analysis()
    email = sys.argv[1]
    password = sys.argv[2]
    serv=sys.argv[3]
    server = poplib.POP3_SSL(serv)
    server.user(email)
    server.pass_(password)
    # 登录的过程
    resp, mails, octets = server.list()
    index = len(mails)  # 邮件的总数
    print('邮件总数：%s'%index)
    # 此处的循环是取最近的几封邮件
    for i in range(index, 0, -1):#获取所有邮件
    # for i in range(1,index+1):#最近的3封邮件
        resp, lines, octets = server.retr(i)  # 取邮件
        msg_content = b'\r\n'.join(lines).decode('utf-8', 'ignore')
        msg = Parser().parsestr(msg_content)

        # server.dele(index) 删除邮件
        subset=a.get_header(msg)
        a.get_file(msg)
        tim,cont,sine=a.get_content(msg)
        subset['time']=tim
        subset['content']=cont
        for key, value in subset.items():
            if isinstance(value, bytes):
                subset[key] = str(value, encoding='utf-8')
        # subject=subset['Subject']
        # from_=subset['From']
        # a = base64.b64encode(subject.encode())
        # print(a)
        # print(subset['Subject'])
        # with open('a.txt','w',encoding='utf8')as p:
        #     p.write(subset['Subject'])
        # datas={
        #     'subject ':a,
        #     # 'from':subset['From'],
        #     # 'subject':'哈哈',
        #     # 'time':time,
        #     # 'content':cont
        # }
        if sine==1:
            print('发送邮件')
            da=json.dumps(subset)
            print(da)
            urls='http://vip1.amazonreviews.top/api/zgc_receive_mail.php'
            response=requests.post(urls,data=da)
            print(response.status_code)

            print(response.text.encode('utf8'))
            print('发送成功')
        else:
            print('邮件超出时间范围，不发送')
            break

    server.quit()





