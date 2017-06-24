#!/usr/bin/env python
#coding: utf-8

CR = ' '
LF = ' '
ESC = ''

import serial
import time

#----- com port open -----
com = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=115200,
    bytesize=8,
    parity='N',
    stopbits=1,
    timeout=None,
    xonxoff=0,
    rtscts=0,
    writeTimeout=None,
    dsrdtr=None)
#----- Logging File open -----
print "filename:"

myfile=raw_input()

fp = open(myfile +".csv", 'a')

#----- Main Routine -----
counter = 0   #時々flushして結果を吐き出すためのカウンタ

timcnt = 0

print u"[Ctrl+c]キーでLoggingを終了します."
#temp = com.read(10000)
while True:
	try:
	    #データ送信要求

    	#データ受信
		time.sleep(0.01)  #少し待つ
		line = com.readline()

    	#結果表示とファイル書込み
		results = line  #必要に応じて切り出し等加工する
		print results

		fp.write(results + LF)
    	#10回に1度、バッファflush（異常停止時に少しでもファイルに残す対策）
		counter += 1
		counter %= 10
		if (counter == 0):
			fp.flush()
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	except KeyboardInterrupt:
	#----- 終了処理 -----
		print u"Loggingを終了します."
		#----- com port close -----
		com.close()
		#----- Logging File close -----
		fp.write(LF)
		fp.flush()
		fp.close()
		break
#--EOF--
