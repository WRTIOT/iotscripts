# -*- coding: utf-8 -*-
import lewei,time

'''
一个非常简单的demo，定时上传两个传感器数据,并不停的读取TCP反控连接的控制数据
作者：行知
邮件：lasoxygen@gmail.com
'''

def run():

    sensorData = {"BH":0, "pm1":0}
    batValue = 80  # 光照
    tempValue = 200 # 颗粒物

    lw = lewei.LeWeiLib("c99aa8b4c7e64362ac37671d3df5f02c") #传入用户key
    lw.TcpControlInit("01") #初始化TCP反向控制连接,需传入网关号

    lasttime = time.time()
    while 1:
        time.sleep(0.1)
        ret = lw.TcpControlRead()
        if ret:
            print "接收到TCP反向控制数据：",ret

        if time.time() - lasttime > 10:
            lasttime = time.time()

            sensorData["BH"] = batValue
            sensorData["pm1"] = tempValue

            ret = lw.updateSensors("01", sensorData) #传入网关号及传感器数据
            if ret != -1:
                if ret["Successful"] == True:
                    print "上传传感器数据成功！Message：",ret["Message"]
                else:
                    print "上传传感器数据失败！Message：",ret["Message"]
            else:
                print "遇到错误，无法上传数据"


if __name__ == "__main__":
    run()
