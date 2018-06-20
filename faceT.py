# #####
# Function: Face Recognition
# Author: Feng Jiangyan, Shan Chaoqun
# Date: July, 2018
# ####

import sys
import ssl
import json
import cv2
import os
import numpy as np  
from urllib import request, parse
from PIL import Image, ImageDraw, ImageFont
import base64


# cmd = 'ping 127.0.0.1'
# os.system(cmd)

# client_id 为官网获取的AK， client_secret 为官网获取的SK  
# 获取access token
global null
null= ''
# null=''
# python无法处理null这样的字符串,所以把null设为空格（none）
def get_token():  
    client_id = 'qr7F5UZZnTqvHkABqgrOBKcM' 
    client_secret = 'Gnhf6fhFYwyR1969hY0nBxssI0R6Fnjo'  
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s'%(client_id,client_secret)  
    req = request.Request(host)  
    req.add_header('Content-Type', 'application/json; charset=utf-8')  
    response = request.urlopen(req)  
    # 获得请求结果
    content = response.read()  
    # 结果转化为字符
    content = bytes.decode(content)  
    # 转化为字典
    content = eval(content[:-1])  
    return content['access_token']  
  
  
# 转换图片
# 读取文件内容，转换为base64编码
# 二进制方式打开图文件
def imgdata(file1path,file2path):
    f = open(r'%s' % file1path,'rb')
    pic1 = base64.b64encode(f.read())
    f.close()  
    f = open(r'%s' % file2path,'rb')
    pic2 = base64.b64encode(f.read())
    f.close()
    IMAGE_TYPE = "BASE64"
    # 将图片信息格式化为可提交信息，这里需要注意str参数设置
    params = [{"image":str(pic1,'utf-8'),"image_type":IMAGE_TYPE},{"image":str(pic2,'utf-8'),"image_type":IMAGE_TYPE}]
    return params  


def imgdataH(filepath):  
    import base64  
    f = open(r'%s' % filepath,'rb')
    pic = base64.b64encode(f.read())
    f.close()  
    IMAGE_TYPE = "BASE64"
    # 将图片信息格式化为可提交信息，这里需要注意str参数设置
    # params = {"image":str(pic,'utf-8'),"image_type":IMAGE_TYPE,"max_face_num":10}
    params = {"image":str(pic,'utf-8'),"image_type":"BASE64","max_face_num":10,"face_field":"gender,age,beauty"}
    return params


# 提交进行对比获得结果
def img(file1path,file2path):  
    token = get_token()  
    # 人脸识别API
    # url1 = 'https://aip.baidubce.com/rest/2.0/face/v3/detect?access_token='+token
    # 人脸对比API
    url = 'https://aip.baidubce.com/rest/2.0/face/v3/match?access_token='+token  
    params = imgdata(file1path,file2path)
    # urlencode处理需提交的数据
    # data = parse.urlencode(params).encode('utf-8')
    data = json.dumps(params).encode('utf-8')
    req = request.Request(url=url,data=data)  
    # req.add_header('Content-Type', 'application/x-www-form-urlencoded')
    req.add_header('Content-Type', 'application/json')
    response = request.urlopen(req)  
    content = response.read()  
    content = bytes.decode(content)
    print(content)
    content = eval(content)  
    # 获得分数
    score = content["result"]["score"]
    if score>75:
        
        return '照片相似度：' + str(score) + ',同一个人'
    else:  
        return '照片相似度：' + str(score) + ',不是同一个人'

  
# 提交进行对比获得结果
def imgH(filepath):  
    token = get_token()  
    # 人脸识别API
    url = 'https://aip.baidubce.com/rest/2.0/face/v3/detect?access_token='+token  
    # 人脸对比API
    # url = 'https://aip.baidubce.com/rest/2.0/face/v3/match?access_token='+token
    params = imgdataH(filepath)
    # urlencode处理需提交的数据
    # data = parse.urlencode(params).encode('utf-8')
    data = json.dumps(params).encode('utf-8')
    req = request.Request(url=url, data=data)
    # req.add_header('Content-Type', 'application/x-www-form-urlencoded')
    req.add_header('Content-Type', 'application/json')
    response = request.urlopen(req)  
    content = response.read()  
    content = bytes.decode(content)
    content = eval(content)
    print(content)
    return content


# 框出人脸位置
# 图像上标识年龄性别
def drawSquare(filepath, left, top, right, bottom, age, gender):
    img = Image.open(filepath)
    draw = ImageDraw.Draw(img)
    # 框出人脸位置
    draw.rectangle((left, top, right, bottom), fill=None,outline = (0,255,0))  
    # 绘制文本
    font = ImageFont.truetype("consola.ttf", 15)#设置字体
    draw.text((left,top-27), 'age:'+age,fill=(0,0,255), font=font)
    draw.text((left, top-15), 'gender:'+gender,fill=(255,0,0), font=font)
    img.show("Image",img)
    return


if __name__ == '__main__':
    file1path = './pic/jiao_xiao.jpg'
    file2path = './pic/jiao_da.jpg'
    content = imgH(file1path)
    # 由返回参数提取所需信息
    faceNumber = content["result"]["face_num"]
    gender = content["result"]["face_list"][0]["gender"]["type"]
    age = content["result"]["face_list"][0]["age"]
    beauty = content["result"]["face_list"][0]["beauty"]
    left = content["result"]["face_list"][0]["location"]["left"]
    top = content["result"]["face_list"][0]["location"]["top"]
    width = content["result"]["face_list"][0]["location"]["width"]
    height = content["result"]["face_list"][0]["location"]["height"]
    print('人脸数为：'+str(faceNumber)+' 性别为：'+gender+' 年龄为：'+str(age)+' 美丽数值：'+str(beauty))
    drawSquare(file1path,int(left),int(top),int(left+width),int(top+height), str(age), str(gender))
    
    content1 = imgH(file2path)
    # 由返回参数提取所需信息
    faceNumber = content1["result"]["face_num"]
    gender = content1["result"]["face_list"][0]["gender"]["type"]
    age = content1["result"]["face_list"][0]["age"]
    beauty = content1["result"]["face_list"][0]["beauty"]
    left = content1["result"]["face_list"][0]["location"]["left"]
    top = content1["result"]["face_list"][0]["location"]["top"]
    width = content1["result"]["face_list"][0]["location"]["width"]
    height = content1["result"]["face_list"][0]["location"]["height"]
    print('人脸数为：'+str(faceNumber)+' 性别为：'+gender+' 年龄为：'+str(age)+' 美丽数值：'+str(beauty))
    drawSquare(file2path,int(left),int(top),int(left+width),int(top+height), str(age), str(gender))
    # 正脸框出OK，脸有rot的时候会偏差较大（30度-fbb）

    res = img(file1path,file2path)
    print(res)
    
