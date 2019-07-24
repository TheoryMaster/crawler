#-*-coding: utf-8-*-

#import paho.mqtt.client as mqtt
#import paho.mqtt.publish as publish
import crawler
import json
import time
import datetime


#크롤러 객체 저장
crawlerList = []

#센서 key값과 port 번호
port = {"temp": 2, "hum" : 3, "wind" : 4, "wind_dir" : 7, "rain" : 9, "sun" : 1, "solar" : 11, "soil10" : 6}



#크롤러 객체 생성 함수
def makeCrl():
    for code in states:
        crawlerList.append(crawler.Crawler(code))


#uid 매개변수 추가해야됨
#센서값을 MQTT 메시지로 변환, MQTT 브로커로 전송

def changeMessagePublish(sensor, data):
    msg = {"Uid" : None, "time" : time, "data" : data, "Snode" : 1, "Port" : port[sensor], "nGPS" : gps}
    #메시지 발행한는 부분 추가할 것
    print(msg)
    


states = crawler.getStates()
makeCrl()


#changeMessagePublish 함수에 사용되는 전역변수
gps = None
time = ""

for crl in crawlerList:    
    
    msg = crl.pubMessage()
    #메시지가 없을 때
    if (msg == None or msg == ""):
        print(".")
        continue

    #풍향이 정온인 경우 0.0으로 수정
    msg = msg.replace(":'정온'", ":'0.0'") 
    msg = msg.replace("'", '''"''')


    dict = json.loads(msg)


    #전역변수 gps값 설정
    gps = (dict["lat"], dict["lon"])

    #전역변수 time값 설정
    timeStr = dict["x"]
    t = datetime.datetime.strptime(timeStr, "%Y/%m/%d %H:%M")
    ###############만약 연도값이 2자리라면 %Y를 %y로 교체해주세요################
    dict["x"] = t.strftime("%Y-%m-%dT%H:%M:%S")
    time = dict["x"]


    
    for sensor in dict:
        #key 값이 x, lat, lon, region일 경우 메시지 발행 X -> port에 존재하지 않는 key
        #값이 "X", "-", "*"일 경우 메시지 발행 X
        try:
            print(sensor + " " + dict[sensor])
            if(sensor == "sun"):
                dict[sensor] = float(dict[sensor].replace(",", ""))
            else:
                dict[sensor] = float(dict[sensor])
            changeMessagePublish(sensor, dict[sensor])
        except:
            continue


    
    #print(dict)
    #msg = json.dumps(dict, ensure_ascii=False)

    #IP 수정
    #publish.single(crl.topic, msg, hostname = "ip", port = 1883, protocol = mqtt.MQTTv311)
    
