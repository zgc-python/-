# coding: utf-8
import xlrd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header

class RegisterAmz():
    def __init__(self,text):
        self.text=text
        self.workbook = xlrd.open_workbook('mail.xlsx')
        self.table = self.workbook.sheets()[0]  # 表示第一个sheet,第一张表
        self.nrows = self.table.nrows  # 获取每一行
        self.show(self.nrows)
        self.au = ''
        for self.au in range(1,self.nrows):
            self.show('开始发送第%s行'%self.au)
            self.username=self.table.row_values(self.au)[0]
            self.password=self.table.row_values(self.au)[1]
            self.recei=self.table.row_values(self.au)[2]
            print(self.text)
            self.subject=self.text.split(';')[0]
            self.main_text=self.text.split(';')[1]
            print(self.username,self.password)
            print(self.main_text)
            self.send()

    def show(self,msg):
        print(msg)

    def send(self):
        # 设置smtplib所需的参数
        # 下面的发件人，收件人是用于邮件传输的。
        smtpserver = 'smtp.mail.aliyun.com'
        username = self.username
        password = self.password
        sender = self.username
        # receiver='XXX@126.com'
        # 收件人为多个收件人
        receiver = [self.recei]
        subject = self.subject
        # 通过Header对象编码的文本，包含utf-8编码信息和Base64编码信息。以下中文名测试ok
        # subject = '中文标题'
        # subject=Header(subject, 'utf-8').encode()

        # 构造邮件对象MIMEMultipart对象
        # 下面的主题，发件人，收件人，日期是显示在邮件页面上的。
        msg = MIMEMultipart('mixed')
        msg['Subject'] = subject
        msg['From'] = '%s <%s>'%(self.username,self.username)
        # msg['To'] = 'XXX@126.com'
        # 收件人为多个收件人,通过join将列表转换为以;为间隔的字符串
        msg['To'] = ";".join(receiver)
        # msg['Date']='2012-3-16'

        # 构造文字内容
        text = self.main_text
        text_plain = MIMEText(text, 'plain', 'utf-8')
        msg.attach(text_plain)
        # 构造图片链接
        # sendimagefile = open(r'aa.jpg', 'rb').read()
        # image = MIMEImage(sendimagefile)
        # image.add_header('Content-ID', '<image1>')
        # image["Content-Disposition"] = 'attachment; filename="testimage.png"'
        # msg.attach(image)

        # 构造html
        # 发送正文中的图片:由于包含未被许可的信息，网易邮箱定义为垃圾邮件，报554 DT:SPM ：<p><img src="cid:image1"></p>
        # html = """
        # <html>
        #   <head></head>
        #   <body>
        #     <p>Hi!<br>
        #        How are you?<br>
        #        Here is the <a href="http://www.baidu.com">link</a> you wanted.<br>
        #     </p>
        #   </body>
        # </html>
        # """
        # text_html = MIMEText(html, 'html', 'utf-8')
        # text_html["Content-Disposition"] = 'attachment; filename="texthtml.html"'
        # msg.attach(text_html)
        #
        # # 构造附件
        # sendfile = open(r'cook.txt', 'rb').read()
        # text_att = MIMEText(sendfile, 'base64', 'utf-8')
        # text_att["Content-Type"] = 'application/octet-stream'
        # # 以下附件可以重命名成aaa.txt
        # # text_att["Content-Disposition"] = 'attachment; filename="aaa.txt"'
        # # 另一种实现方式
        # text_att.add_header('Content-Disposition', 'attachment', filename='aaa.txt')
        # # 以下中文测试不ok
        # # text_att["Content-Disposition"] = u'attachment; filename="中文附件.txt"'.decode('utf-8')
        # msg.attach(text_att)

        # 发送邮件
        smtp = smtplib.SMTP()
        # smtp.connect('smtp.163.com')smtp.mxhichina.com  465，SSL
        smtp.connect('smtp.alibaba.com')
        # 我们用set_debuglevel(1)就可以打印出和SMTP服务器交互的所有信息。
        # smtp.set_debuglevel(1)
        smtp.login(username, password)
        smtp.sendmail(sender, receiver, msg.as_string())
        smtp.quit()
        self.show('第%s行发送成功\n-----------------'%self.au)









