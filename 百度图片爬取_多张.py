#!-*- coding:utf-8 -*-
"""根据搜索词下载百度图片"""
#参考博文：https://blog.csdn.net/hust_bochu_xuchao/article/details/79431145
import re, os, sys, urllib, requests, time, math, glob, winreg
from PIL import  Image

#获取桌面路径
def get_desktop():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')#利用系统的链表
    return winreg.QueryValueEx(key, "Desktop")[0]  #这个返回值已经是字符串形式了

#创建图片储存的桌面文件夹
def mkdir(path):
    folder = os.path.exists(path) #如果path路径下有这个文件，就返回True，反之返回False
    
    if not folder:
        os.makedirs(path)
        time.sleep(2)
#获得动态的网址，最重要的        
def getPage(keyword, page, n):
    page=page*n
    #按照标准， URL 只允许一部分 ASCII 字符（数字字母和部分符号），其他的字符（如汉字）是不符合 URL 标准的。所以 URL 中使用其他字符就需要进行 URL 编码。
    keyword1=urllib.parse.quote(keyword, safe='/') #解码的过程，对keyword解码，解码内容提到参考网址https://www.cnblogs.com/SeekHit/p/6284974.html
    #print(keyword1) 
    url_begin= "http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word="
    url = url_begin+ keyword1 + "&pn=" +str(page) + "&gsm="+str(hex(page))+"&ct=&ic=0&lm=-1&width=0&height=0"
    return url

#获得每个动态的网址里的图片url
def get_onepage_urls(onepageurl):
    try:
        html = requests.get(onepageurl).text
    except Exception as e:
        print(e)
        pic_urls = []
        return pic_urls
    #pic_urls为一个网址内的所有的图片的内容
    pic_urls = re.findall('"objURL":"(.*?)",', html, re.S)
    print(pic_urls)
    return pic_urls
 

def down_pic(file, keyword, pic_urls):
    """给出图片链接列表, 下载所有图片"""
    m = 0
    for i, pic_url in enumerate(pic_urls):
        try:
            pics = requests.get(pic_url, timeout=15) #pics若是返回response[200] 代表响应成功
            #print('正在爬取URL地址：'+pic_url+'...')
            print('正在下载图片，请稍后'.center(30, '*'))
            fq = open(file + '/'+keyword+'_' + str(m)+'.jpg', 'wb')
            #print(pics.content) #返回这些内容b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x01,\x01,\x00\x00\xff\xed\x1b\xaePhotoshop 3.0\x008BIM\x04\x04\x00\x00\x00\x00\x02\x97\x1c\x01Z\x00\x03\x1b%G\x1c\x02\x00\x00\x02\x00\x00\x1c\x02x\x00Hfresh red apples with water drops and slice isolated on white background\x1c\x02\x05\x00@fresh red apples with water drops and slice isolated on white ba\x1c\x027\x00\x08
            fq.write(pics.content) #下载pics.content的内容，并将其写入fq里的路径
            fq.close() #关闭fq，占内存的
            m += 1
        except requests.exceptions.ConnectionError:
            print('您当前请求的URL地址出现错误')
            continue
        
            '''
            string =str(i + 1) + '.jpg'
            with open(string, 'wb') as f:
                f.write(pic.content)
                print('成功下载第%s张图片: %s' % (str(i + 1), str(pic_url)))
        except Exception as e:
            print('下载第%s张图片时失败: %s' % (str(i + 1), str(pic_url)))
            print(e)
            continue
             '''
 
if __name__ == '__main__':
    directory = input("输入你想创建的桌面文件夹名称：")
    keyword = input("输入你想要的图片名称：") # 关键词, 改为你想输入的词即可, 相当于在百度图片里搜索一样
    page_begin=0
    page_number=30
    image_number = eval(input("输入需要的图片的张数："))/30-1
    image_number = math.ceil(image_number) #上浮数字
    print(image_number)
    file = get_desktop() + '/' +directory
    mkdir(file)
    print("等待2s, 在桌面创建一个名为 " + directory + " 的文件夹")
        
    all_pic_urls = []
    
    while 1:
        if page_begin>= image_number:
            break
        print("第{}次请求数据" .format(page_begin))
        url=getPage(keyword, page_begin, page_number)
        onepage_urls= get_onepage_urls(url)
        page_begin += 1
 
        all_pic_urls.extend(onepage_urls)
        
    down_pic(file, keyword, list(set(all_pic_urls)))
    print('图片下载完成！'+"一共保存了{}张图片".format(int((image_number+1)*30)))
    
    #若需要对其尺寸输出要一致，请采用以下方式：
    #图片尺寸处理
    TF_resize = eval(input("是否需要对图片进行尺寸处理(True or False)："))
    if TF_resize == True:
        arr = [[]]
        you_want_size_height, you_want_size_wide= eval(input("输入你想要的图片的高和宽，用逗号分隔:"))
        class_path = file+ '/' #这是我的图片文件夹的存放路径
        #name为class的类别, glob.glob('c:/pic*.txt')获得C盘pic文件夹下的所有txt格式的文件,返回的是列表格式，该列表的元素为txt格式文件的绝对路径
        for infile in glob.glob(class_path + '*.jpg'): # 遍历所有文件夹下的jpg格式的图片
            img = Image.open(infile) #使用Image模块打开文件
            img = img.resize([you_want_size_wide, you_want_size_height], Image.ANTIALIAS) #改变尺寸,并且修改图片有高质量
            img.save(infile)
            
