# -*- coding: utf-8 -*-

'''
实现了http://www.lewei50.com物联网平台的所有接口
作者：行知
邮件：lasoxygen@gmail.com
'''

import socket
import json
import urllib2
import urllib
import time
import thread
import select
 
class LeWeiLib(object):

    user_agent = None
    timeout = None
    userkey = None
    TcpSocketClient = None
    TcpControlData = None
    
    def __init__(self, user_key):
        '''
        :user_key: UUID
        '''
        agent = "" "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)\r\n" "userkey: %s" % user_key
        self.user_agent = {"User-Agent" : agent}
        self.timeout = 3
        self.userkey = user_key

    def getSensorsWithGateway(self, sensorType):
        '''
        :sensorType: 查询的传感器类型，可取下列值
                     类型名      名称
                     TEMP    温度监控
                     PRES    气压监控
                     HUMI    湿度监控
                     GPSS    GPS监控
                     DIST    深度监控
                     JDQI    继电器
                     CO22    CO2
                     KLUX    光照度
                     PMUG    颗粒物
                     PMU2    颗粒物-2
                     PMU3    颗粒物-3
                     OTHR    其他类型
        '''
        #print "LeWeiLib_log::getSensorsWithGateway,sensorType:%r" % sensorType
        url = "http://wwww.lewei50.com/api/v1/user/getSensorsWithGateway"

        if sensorType != "":
            url = url + "?sensorType=" + sensorType
            print url
        try:
            req = urllib2.Request(url, "", self.user_agent)
            response = urllib2.urlopen(req, timeout = self.timeout)
            ret = response.read()
            response.close()
            #print ret
            return ret
        except Exception , e:
            print "Exception: %r" % e
            return -1
        
    def gatewayAdd(self, gateway):
        '''
        :gateway: 网关信息，字典类型，格式如下，键必须一致
                 {
                  "idName":"01",
                  "name":"gateway1",
                  "typeName":"arduino",
                  "description":"test",
                  "isPublic":false
                 }
                 其中typeName为网关类型，可取下列值
                   arduino-----Arduino
                   art---------ART
                   lw-board----lw-board
                   other-------其它
        '''
        #print "LeWeiLib_log::gatewayAdd,gateway:%r" % gateway
        url = "http://www.lewei50.com/api/V1/gateway/add"
        
        try:
            post_body =  json.dumps(gateway)
            
            req = urllib2.Request(url, post_body, self.user_agent)
            response = urllib2.urlopen(req, timeout = self.timeout)
            ret = json.loads(response.read())
            '''
            receive msg:
            {
             "Successful": true, 
             "Message": null
            }
            '''
            response.close()
            return ret
            
        except Exception , e:
            #print "Exception: %r" % e
            return -1
        
    def gatewayUpdate(self, gateway_id, gateway):
        '''
        :gateway_id: 数字字符串，网关标识
        :gateway: 网关信息，字典类型，格式如下，键必须一致
                  {
                    "name":"测试网关",
                    "description":"用于测试的网关",
                    "isControlled":false,
                    "internetAvailable":false,
                    "apiAddress":"http://192.168.1.105/api"
                  }
        '''
        #print "LeWeiLib_log::gatewayUpdate, gateway_id:%s, gateway:%r" % (gateway_id, gateway)
        url = "http://www.lewei50.com/api/v1/gateway/update/%s" % gateway_id
       
        try:
            post_body =  json.dumps(gateway)
            
            req = urllib2.Request(url, post_body, self.user_agent)
            response = urllib2.urlopen(req, timeout = self.timeout)
            ret = json.loads(response.read())
            '''
            receive msg:
            {
             "Successful": true, 
             "Message": null
            }
            '''
            response.close()
            return ret
            
        except Exception , e:
            #print "Exception: %r" % e
            return -1
        
    def gatewayUpdatelog(self, gateway_id, log):
        '''
        :gateway_id: 数字字符串，网关标识
        :log: 日志消息
        '''
        #print "LeWeiLib_log::gatewayUpdatelog, gateway_id:%s, log:%s" % (gateway_id, log)
        url = "http://www.lewei50.com/api/v1/gateway/updatelog/%s" % gateway_id
       
        post_msg = '''
        {
          "Message":""
        }'''
        try:
            post_msg = json.loads(post_msg)
            post_msg["Message"] = log
            post_body =  json.dumps(post_msg)
            
            req = urllib2.Request(url, post_body, self.user_agent)
            response = urllib2.urlopen(req, timeout = self.timeout)
            ret = json.loads(response.read())
            '''
            receive msg:
            {
             "Successful": true, 
             "Message": null
            }
            '''
            response.close()
            return ret
            
        except Exception , e:
            #print "Exception: %r" % e
            return -1
        
    def gatewayExcuteCommand(self, gateway_id, command):
        '''
        :gateway_id: 数字字符串，网关标识
        :Command: 命令体，字典类型，格式如下，键必须一致
                          {
                           "f":"",
                           "p1":"",
                           "p2":"",
                           "p3":"",
                           "p4":"",
                           "p5":""
                          }
        '''
        #print "LeWeiLib_log::gatewayUpdatelog, gateway_id:%s, Command:%r" % (gateway_id, command)
        url = "http://www.lewei50.com/api/v1/gateway/excuteCommand/%s" % gateway_id
        
        try:
            if "f" in command.keys():
                url = url + "?f=" + command["f"]
            else:
                return -1
            
            if "p1" in command.keys():
                url = url + "?p1=" + command["p1"]
            if "p2" in command.keys():
                url = url + "?p2=" + command["p2"]
            if "p3" in command.keys():
                url = url + "?p3=" + command["p3"]
            if "p4" in command.keys():
                url = url + "?p4=" + command["p4"]
            if "p5" in command.keys():
                url = url + "?p5=" + command["p5"]

            req = urllib2.Request(url, "", self.user_agent)
            response = urllib2.urlopen(req, timeout = self.timeout)
            ret = json.loads(response.read())
            '''
            receive msg:
            {
             "successful": true, 
             "message": "",
             "data":xxx
            }
            注意，此处json体中键为小写的！！
            '''
            response.close()
            return ret
            
        except Exception , e:
            #print "Exception: %r" % e
            return -1

    def updateSensors(self, gateway_id, sensors):
        '''
        :gateway_id: 数字字符串，网关标识
        :sensors: 传感器及值，字典类，键为传感器名称，键值为数值
                  {
                    "bat":12,
                    "humi":12
                  }
        
        '''
        #print "LeWeiLib_log::updateSensors,gateway_id:%s,sensors:%r" % (gateway_id,sensors)
        url = "http://wwww.lewei50.com/api/v1/gateway/updatesensors/%s" % gateway_id
        '''
        post msg:
        [
          {
           "Name":"T1",
           "Value":"1"
          },
          {
           "Name":"01H1",
           "Value":"96.2"
          }
        ]
        '''
        
        post_body = "["
        try:
            for name in sensors:
                s = "{" + '"Name":"%s"' % name +"," + '"Value":"%s"' % sensors[name] + "},"
                post_body = post_body + s

            post_body = post_body[:-1] + "]"

            req = urllib2.Request(url, post_body, self.user_agent)
            response = urllib2.urlopen(req, timeout = self.timeout)
            ret = json.loads(response.read())
            '''
            receive msg:
            {
             "Successful": true, 
             "Message": null
            }
            '''
            response.close()
            return ret
        except Exception , e:
            #print "Exception: %r" % e
            return -1

    def gatewayAddSensor(self, gateway_id, sensors):
        '''
        :gateway_id: 数字字符串，网关标识
        :sensors: 传感器及值，字典类型，格式如下，键必须一致
                 {
                   "idName":"T1",
                   "typeName":"TEMP",
                   "name":"testt1",
                   "unit":"℃",
                   "isPublic":true
                  }
        '''
        #print "LeWeiLib_log::gatewayAddSensor,gateway_id:%s,sensors:%r" % (gateway_id,sensors)
        url = "http://wwww.lewei50.com/api/v1/gateway/addsensor/%s" % gateway_id
        
        try:
            post_body =  json.dumps(sensors)
            
            req = urllib2.Request(url, post_body, self.user_agent)
            response = urllib2.urlopen(req, timeout = self.timeout)
            ret = json.loads(response.read())
            '''
            receive msg:
            {
             "Successful": true, 
             "Message": null
            }
            '''
            response.close()
            return ret
        except Exception , e:
            #print "Exception: %r" % e
            return -1

    def sensorUpdateSensorInfo(self, sensor_id, sensors):
        '''
        :sensor_id: 数字字符串，设备标识
        :sensors: 传感器及值，字典类型，格式如下，键必须一致
                  {
                    "idName":"GPS",
                    "name":"testt1",
                    "unit":"1",
                    "isPublic":"true",
                    "description":"test"
                  }
        '''
        #print "LeWeiLib_log::sensorUpdateSensorInfo,sensor_id:%s,sensors:%r" % (sensor_id,sensors)
        url = "http://wwww.lewei50.com/api/v1/sensor/UpdateSensorInfo/%s" % sensor_id
        
        try:
            post_body =  json.dumps(sensors)
            
            req = urllib2.Request(url, post_body, self.user_agent)
            response = urllib2.urlopen(req, timeout = self.timeout)
            ret = json.loads(response.read())
            '''
            receive msg:
            {
             "Successful": true, 
             "Message": null
            }
            '''
            response.close()
            return ret
        except Exception , e:
            #print "Exception: %r" % e
            return -1

    def sensorGetHistoryData(self, sensor_id, command):
        '''
        :gateway_id: 数字字符串，网关标识
        :Command: 命令体，字典类型，格式如下，键必须一致
                          {
                           "StartTime":"2014-02-18",
                           "EndTime":"2014-02-19",
                           "Interval":"1",
                           "Start":"0",
                           "Limit":"1000",
                           "Order":"1"
                          }
        '''
        #print "LeWeiLib_log::sensorGetHistoryData, sensor_id:%s, Command:%r" % (sensor_id, command)
        url = "http://www.lewei50.com/api/v1/sensor/GetHistoryData/%s" % sensor_id
        
        try:
            if "StartTime" in command.keys():
                url = url + "?StartTime=" + command["StartTime"]
            if "EndTime" in command.keys():
                url = url + "?EndTime=" + command["EndTime"]
            if "Interval" in command.keys():
                url = url + "?Interval=" + command["Interval"]
            if "Start" in command.keys():
                url = url + "?Start=" + command["Start"]
            if "Limit" in command.keys():
                url = url + "?Limit=" + command["Limit"]
            if "Order" in command.keys():
                url = url + "?Order=" + command["Order"]

            req = urllib2.Request(url, "", self.user_agent)
            response = urllib2.urlopen(req, timeout = self.timeout)
            ret = json.loads(response.read())
            '''
            receive msg:
            {
             "Data": [],
             "Successful": true,
             "Message": null
            }
            '''
            response.close()
            return ret
            
        except Exception , e:
            #print "Exception: %r" % e
            return -1

    def sensorGetPublicGPSInRange(self, command):
        '''
        :Command: 命令体，字典类型，格式如下，键必须一致
                          {
                           "lng":"",
                           "lat":"",
                           "distance":"0.1",
                           "limitSecond":600,
                           "limitCount":10
                          }
        '''
        #print "LeWeiLib_log::sensorGetPublicGPSInRange, Command:%r" % command
        url = "http://www.lewei50.com/api/v1/sensor/getPublicGPSInRange"
        
        try:
            if "lng" in command.keys():
                url = url + "?lng=" + command["lng"]
            if "lat" in command.keys():
                url = url + "?lat=" + command["lat"]
            if "distance" in command.keys():
                url = url + "?distance=" + command["distance"]
            if "limitSecond" in command.keys():
                url = url + "?limitSecond=" + command["limitSecond"]
            if "limitCount" in command.keys():
                url = url + "?limitCount=" + command["limitCount"]

            req = urllib2.Request(url, "", self.user_agent)
            response = urllib2.urlopen(req, timeout = self.timeout)
            ret = json.loads(response.read())
            '''
            receive msg:
            {
             "Data": [],
             "Successful": true,
             "Message": null
            }
            '''
            response.close()
            return ret
            
        except Exception , e:
            #print "Exception: %r" % e
            return -1
        
    def TcpControlInit(self, gateway_id):
        '''
        创建心跳线程维护发向lewei服务器的心跳包
        '''
        #print "LeWeiLib_log::TcpControlInit, gateway_id:%r" % gateway_id
        
        try:
            thread.start_new_thread(self._TcpHeartbeat, (gateway_id, self.userkey))
            #返回成功
            return 0           
        except Exception , e:
            #返回失败
            return -1

    def TcpControlRead(self):
        '''
        读取控制命令
        返回值json形式
        {"method":"send","gatewayNo":"01","userkey":"45a71b454b784e0e829b286ab39f902a","f":"writeSerial","p1":"0"}
        '''
        #print "LeWeiLib_log::TcpControlRead"
        
        if self.TcpControlData is not None:
            ret = json.loads(self.TcpControlData[:-3]) #drop last symbol '&^!'
            self.TcpControlData = None
            return ret
        else:
            return None

    def _TcpHeartbeat(self, gateway_id, userkey):
        '''
        用户不要直接调用这条函数！
        '''
        #print gateway_id, userkey
        lasttime = time.time()
        while True:
            time.sleep(0.1)
            try:
                if self.TcpSocketClient is None:
                    self.TcpSocketClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.TcpSocketClient.settimeout(3) #设置超时时间
                    self.TcpSocketClient.connect(("tcp.lewei50.com", 9960))
                    time.sleep(2)
                    self.TcpSocketClient.send('{"method":"update","gatewayNo":"%s","userkey":"%s"}&^!' % (gateway_id, userkey))
                    self.TcpSocketClient.setblocking(False) #完成连接后设置socket是非阻塞的
                    
                if time.time() - lasttime > 60:  #1分钟发送一次心跳
                    lasttime = time.time()
                    self.TcpSocketClient.send('{"method":"update","gatewayNo":"%s","userkey":"%s"}&^!' % (gateway_id, userkey))

                rlists = [self.TcpSocketClient] #select参数 可读状态集合 
                wlists = [] #select参数 可写状态集合
                xlists = [] #异常？
                rs,ws,es = select.select(rlists, wlists, xlists, 0)
                if rs:
                    ret =self.TcpSocketClient.recv(1024) #读取数据
                    if ret:
                        self.TcpControlData = ret
                        self.TcpSocketClient.send('{"method":"response","result":{"successful":true,"message":"I got it!"}}&^!')

            except Exception, e:
                try:
                    self.TcpSocketClient.close()
                except Exception , e:
                    pass
                    
                self.TcpSocketClient = None
                time.sleep(10) #若连接遇到问题，延时10秒后重连



