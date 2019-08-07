import os
import random
import re
import urllib.request
from urllib.parse import quote

from lxml import etree
import requests


# f_url='https://www.louisvuitton.cn/zhs-cn/women/handbags/all-handbags/_/N-1ouyuai?campaign=sem_BaiduPCPPC_EC-GENE-BAGN_%E5%93%81%E7%89%8C%E5%8C%85%E6%8E%92%E8%A1%8C%E6%A6%9C_category_wbags-all'
#包包
leimu='古驰女包'
f_url='https://www.gucci.cn/zh/ca/women/handbags/chain-shoulder-bags?pn=1'#后缀数字页数改动
#高跟鞋
# f_url='https://www.louisvuitton.cn/zhs-cn/women/shoes/pumps/_/N-n9bpy4/to-2'
#连衣裙
# f_url='https://www.louisvuitton.cn/zhs-cn/women/ready-to-wear/dresses/_/N-1v2fzo4/to-2'
if os.path.exists('F:\\%s' % (leimu)):
    print('文件夹已存在')
    # os.mkdir('F:\\%s--2' % di)
else:
    os.mkdir('F:\\%s' % leimu)
    # resp2=s.get(url=d_url,headers=headers)
headers_list = [
                        {
                            'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0",

                        },
                        {
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36',

                        },
                        {
                            'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",

                        },
                        {
                            'User-Agent': "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko",

                        },
                        {
                            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:63.0) Gecko/20100101 Firefox/63.0',

                        },
                        {
                            'User-Agent': "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",

                        },
                    ]
headers = random.choice(headers_list)
s=requests
resp=s.get(url=f_url)
# with open('dior.html','w',encoding='utf8')as p:
#     p.write(resp.text)

tree=etree.HTML(resp.text)
det_goods_url=tree.xpath('//*[@id="pdlist"]/div/div/a[2]/@href')
# print(det_goods_url)
x=1   #文件夹第几个开始
for det_url in det_goods_url:
    d_url='https://www.gucci.cn'+det_url
    print(d_url)
    if os.path.exists('F:\\%s\\%s' % (leimu,x)):
        print('文件夹已存在')
        # os.mkdir('F:\\%s--2' % di)
    else:
        os.mkdir('F:\\%s\\%s' % (leimu,x))
    resp2=s.get(url=d_url,headers=headers)
    # with open('detail.html','w',encoding='utf8') as p:
    #     p.write(resp2.text)
    treex=etree.HTML(resp2.text)
    title=treex.xpath('//h1/text()')[0]#抓title
    print(title)
    descript='款号：'+treex.xpath('//section[1]//span/text()')[1]
    descript222=treex.xpath('string(//section[1]/article[2]/div[2]/div/div/ul/li[1])').replace('\r','').replace('\n','').replace('\t','')
    descript2=descript222
    # try
    # print(descript2)
    yi=1
    for im_num in range(5):
        im_urls=treex.xpath('//*[@id="product_main_image_%s"]//img/@srcset'%im_num)[0]
        # print(im_list)

        # for j in im_list:
        im_url=im_urls.split(' ')[0]
        print(im_url)
        try:
            urllib.request.urlretrieve(url=im_url, filename='F:\\%s\\%s/%s.jpg' %(leimu,x,yi))
        except:
            pass

        yi+=1
        print('第%s件第%s个图片下载完成' % (x, yi))
    with open('F:\\%s\\%s/listing.txt' % (leimu, x), 'w', encoding='utf8')as f:
        f.write('GUCCI'+'\n'+title + '\n' + descript + descript2)

    x += 1

print('成功')











