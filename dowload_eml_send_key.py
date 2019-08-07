# coding=gbk
# import json
import sys
from datetime import datetime as dtlong
import poplib
# �����ʼ�
import base64
import datetime
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
import time
# ������Ϣͷ�е��ַ���
# û�����������print�����Ļ�ʹ�����ͷ����Ϣ����'=?gb18030?B?yrXWpL3hufsueGxz?='����
# ͨ��decode�������Ϊ����
import requests
from flask import json


class Analysis():
    def decode_str(self,s):
        value, charset = decode_header(s)[0]
        if charset:
            value = value.decode(charset)
        return value
    # �����ʼ���Ϣ��Ϊ�������裬��һ����ȡ��ͷ����Ϣ
    # ����ȡͷ����Ϣ
    # ��Ҫȡ��['From','To','Subject']
    '''
    From: "=?gb18030?B?anVzdHpjYw==?=" <justonezcc@sina.com>
    To: "=?gb18030?B?ztLX1Ly6tcTTys/k?=" <392361639@qq.com>
    Subject: =?gb18030?B?dGV4dMTjusM=?=
    '''

    # ��������ʽ������Ҫ����
    def get_header(self,msg):
        subset={}
        for header in ['From', 'To', 'Subject']:
            value = msg.get(header, '')
            if value:
                # ���µı�����ר�ŵĴ�����
                if header == 'Subject':
                    value = self.decode_str(value)
                    subset[header]=value
                    # print('���⣺'+value)
                elif header in ['From', 'To']:
                    # ��ַҲ��ר�ŵĴ�����
                    hdr, addr = parseaddr(value)
                    name = self.decode_str(addr)
                    # value = name + ' < ' + addr + ' > '
                    value = name
                    subset[header]=value
                    # print(value+'---------------')
            # print(header + ':' + value)
        # print(subset)
        return subset


    # ͷ����Ϣ��ȡ��


    # ��ȡ�ʼ����ַ����룬������message��Ѱ�ұ��룬���û�У�����header��Content-Type��Ѱ��
    def guess_charset(self,msg):
        charset = msg.get_charset()
        if charset is None:
            content_type = msg.get('Content-Type', '').lower()
            pos = content_type.find('charset=')
            if pos >= 0:
                charset = content_type[pos + 8:].strip()
        return charset


    # �ʼ����Ĳ���
    # ȡ����
    # �ʼ������Ĳ������������У�msg.walk()
    # ������ڸ����������ͨ��.get_filename()�ķ�ʽ��ȡ�ļ�����

    def get_file(self,msg):
        for part in msg.walk():
            filename = part.get_filename()
            if filename != None:  # ������ڸ���
                filename = self.decode_str(filename)  # ��ȡ���ļ����������ƣ�ͨ��һ��ʼ����ĺ�������
                data = part.get_payload(decode=True)  # ȡ���ļ���������
                # �˴������Լ������ļ�����λ��
                path = filename
                f = open('F:'+path, 'wb')
                f.write(data)
                f.close()
                print(filename, 'download')


    def get_content(self,msg):
        for part in msg.walk():
            content_type = part.get_content_type()
            charset = self.guess_charset(part)
            # ����и�������ֱ������
            if part.get_filename() != None:
                continue
            email_content_type = ''
            self.content = ''
            if content_type == 'text/plain':
                email_content_type = 'text'
            elif content_type == 'text/html':
                # print('html ��ʽ ����')
                # continue  # ��Ҫhtml��ʽ���ʼ�
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
                # �������Ϊ�գ�Ҳ����
            # print('---------------------')
            self.datatime=msg.get("Date")[0:24]
            # print('�ʼ�����ʱ�䣺%s'%(self.datatime))
            date1 = time.strptime(msg.get("Date")[0:24], '%a, %d %b %Y %H:%M:%S')  # ��ʽ���ռ�ʱ��
            date2 = time.strftime("%Y-%m-%d %H:%M:%S", date1)  # �ʼ�ʱ���ʽת��
            print('�ʼ�����ʱ�䣺%s' % date2)
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
                # print('�ʼ��ڷ�Χ��')
            else:
                eml_sine=0
                # print('�ʼ����ڷ�Χ��')
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
    # ��¼�Ĺ���
    resp, mails, octets = server.list()
    index = len(mails)  # �ʼ�������
    print('�ʼ�������%s'%index)
    # �˴���ѭ����ȡ����ļ����ʼ�
    for i in range(index, 0, -1):#��ȡ�����ʼ�
    # for i in range(1,index+1):#�����3���ʼ�
        resp, lines, octets = server.retr(i)  # ȡ�ʼ�
        msg_content = b'\r\n'.join(lines).decode('utf-8', 'ignore')
        msg = Parser().parsestr(msg_content)

        # server.dele(index) ɾ���ʼ�
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
        #     # 'subject':'����',
        #     # 'time':time,
        #     # 'content':cont
        # }
        if sine==1:
            print('�����ʼ�')
            da=json.dumps(subset)
            print(da)
            urls='http://vip1.amazonreviews.top/api/zgc_receive_mail.php'
            response=requests.post(urls,data=da)
            print(response.status_code)

            print(response.text.encode('utf8'))
            print('���ͳɹ�')
        else:
            print('�ʼ�����ʱ�䷶Χ��������')
            break

    server.quit()





