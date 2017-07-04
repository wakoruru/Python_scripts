#!/usr/bin/env python
#coding: utf-8

import serial
import time

print u"port? (Default is /dev/ttyUSB0)"
port = raw_input()

if not port:
    port = '/dev/ttyUSB0'

print u"baudrate? (Defalut is 115200)"
rate = raw_input()

if not rate:
    rate = 115200

myserial = serial.Serial(port,rate,timeout=0)

print u"serial state:"+str(myserial.isOpen())
print u"serial port:"+str(myserial.port)
print u"serial baudrate:"+str(myserial.baudrate)


while True:
    try:
        time.sleep(0.02)
        data = myserial.readline()
        if data:#dataは存在するか
            datalist=list(data)#dataをlistに

            listnum = len(datalist)#listのサイズを取得
            datalist.reverse()#反転 
            shapelist = []
            
            while True:

                try:
                    index_1 = datalist.index('#') #'#'の要素番号を取得
                except ValueError: #'#'がないとき
                    break

                tmp = datalist[:index_1+1] #インデックス+1までスライス
                tmp.reverse() #反転
                shapelist.append(tmp)
                datalist = datalist[index_1+1:] #スライスした分を削除

            shapelist.reverse()
            print shapelist

    except KeyboardInterrupt:
        break

myserial.close()

if not myserial.isOpen():
    print u"serial closed"
