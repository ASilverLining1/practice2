#!-*- coding:utf-8 -*-
import re, os,time #导入正则表达式模块
import requests #python HTTP客户端 编写爬虫和测试服务器经常用到的模块
import random #随机生成一个数，范围[0,1]

#考虑到各个用户名不同，所以提取Users后面的用户名
ls, ls1, ls2 = [], [], []
m = 0
cwd = str(os.getcwd())
for i in "\\":
    cwd = cwd.replace(i, "/")
for i in cwd.strip():
    ls.append(i)
print(ls)
for j in range(len(ls)):
    if ls[j] == "/":
        if m == 1 or m == 2:
            ls1.append(j)
        m += 1
print(ls1)
for j in range(ls1[0]+1, ls1[1]):
    ls2.append(ls[j])
str1 = "".join(ls2)

#在桌面创建文件夹
def mkdir(path):
    folder = os.path.exists(path)
    
    if not folder:
        os.makedirs(path)
        print("在桌面创建一个名为pictures的文件夹")
        time.sleep(5)

#定义函数方法
def spiderPic(html, keyword):
    print('正在查找 ' + keyword +' 对应的图片,下载中，请稍后......')
    m = 0
    for addr in re.findall('"objURL":"(.*?)"',html,re.S):     #查找URL
        #addr为图片的url
        print('正在爬取URL地址：'+addr[0:30]+'...')  #爬取的地址长度超过30时，用'...'代替后面的内容
        #addr是一个字符串
        try:
            #pic为图片的获取图片的url，要获取url必须通过requests.get
            pics = requests.get(addr,timeout=10)  #请求URL时间（最大10秒）
            #print(pics) print返回的结果是response 200
        except requests.exceptions.ConnectionError:
            print('您当前请求的URL地址出现错误')
            continue
        
        #下载图片，并保存和命名，keyword就是用户输入的关键词word
        fq = open(file + '/'+ keyword+'_'+str(m)+'.jpg','wb')  
        #写入url的内容即图片
        print(pics.content)
        fq.write(pics.content)
        fq.close()
        m += 1
#python的主方法
if __name__ == '__main__':
    word = input('请输入你要搜索的图片关键字：')
    result = requests.get('http://image.baidu.com/search/index?tn=baiduimage&ps=1&ct=201326592&lm=-1&cl=2&nc=1&ie=utf-8&word=' + word).text
    file = "C:/Users/" + str1 +'/'+ "desktop/"+"pictures" #创建的图片文件夹名称
    mkdir(file)
    #调用函数
    #这里result.text显示gkb错误的时候在后面加入from_encoding="utf-8" 运行，然后再把这段代码删掉在运行就可以显示内容了
    spiderPic(result,word)

