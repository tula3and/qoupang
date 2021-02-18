# -*- coding: utf-8 -*-
import flask
from flask import *
from flask import Flask
from flask import request
from flask import jsonify
import sys
import json

from urllib import parse
import urllib.request
import pandas as pd

from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required, current_identity

#jwt 인증
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies
)

import pymysql

#email
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email import encoders
import os
import requests

#qrcode
import qrcode

from urllib.parse import unquote_plus

#qrng 로딩
from qrng import hash8 


hoststr = "localhost"
usrstr = "root"
passwordstr = "co2bot2020!"
dbstr = "Chatbot"

application = Flask("Quantum")
application.config['JWT_TOKEN_LOCATION'] = ['cookies']
application.config['JWT_ACCESS_COOKIE_PATH'] = '/api'
application.config['JWT_REFRESH_COOKIE_PATH'] = '/'
application.config['JWT_COOKIE_CSRF_PROTECT'] = False
application.config['JWT_SECRET_KEY'] = 'co2bot' 
application.config['SESSION_COOKIE_HTTPONLY'] = False 
application.config['CSFR_COOKIE_HTTPONLY'] = False

#application.config['JWT_COOKIE_SECURE'] = False
#application.config['PERMANENT_SESSION_LIFETIME'] = 2678400
#application.config.update(SESSION_COOKIE_SECURE=False,SESSION_COOKIE_HTTPONLY=False,)

api = Api(application)

jwt = JWTManager(application)

@application.route('/')
def index():
	return render_template('index.html')

@application.route('/cert')
def cert():
	return render_template('cert.html')

@application.route('/admin')
def admin():
	return render_template('manage/index.html')


@application.route("/api/v1/hash8" , methods=['GET'])
def getQrng():
    qrng_data = hash8()
    resp = jsonify({'send': True, 'qrng_data' : qrng_data})
    return resp, 200
    
#블록체인 qr코드 인증
@application.route("/api/v1/swag/<email_and_qrng>" , methods=['GET'])
def swagcerti(email_and_qrng):
    
    #url 디코딩
    email_and_qrng = unquote_plus(email_and_qrng)
    print(email_and_qrng)
    #블록체인 전송
    res = sendblockchain(email_and_qrng,1)
    
    #결과값 리턴
    if res.status_code == 200 :
        res2 = getblockchain(email_and_qrng)  
        status = str(res2.json()['status'])
        
        #블록체인 상태까지 포함한 결과값을 리턴
        txHash = str(res.json()['txHash'])
        print(txHash)
        resp = jsonify({'send': True, 'txHash' : txHash, 'status' : status})
        return resp, 200

@application.route("/api/v1/mail/<email>" , methods=['GET'])
def sendemail(email):
    
    #QRNG 생성 난수값 추출
    qrng = hash8()
    print(qrng)
    #이메일 주소 와 구분값 와 qrng <--- 이값을 qrcode 에 인자로 넘겨줘야함
    email_and_qrng = email+"|"+qrng
    
    #메일포함 QRCODE 생성
    #qrcode_url = "https://swagblockchain.run.goorm.io/swag/"+email_and_qrng
    qrcode_url = "https://swagqrng.run.goorm.io/cert?cert="+email_and_qrng
    
    qr_img = qrcode.make(qrcode_url)
    qr_img_src = r'./static/assets/img/qrcode/'+email_and_qrng+'.png'
    qr_img.save(qr_img_src)
    
    #이메일 세팅
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()
    smtp.starttls() # TLS 사용시 필요
    smtp.login('qiskitswag@gmail.com', 'qi!#%sw!!')
    
    msg = MIMEMultipart('alternative')
    
    path = r'./static/assets/img/qbird_hat.png' #보낼 이미지의 경로
    html = """\
        <html>
          <head></head>
          <body>
            <div>
                <center>
                    <b>Scan QRCODE!</b>
                    <br/>
                    <img src="cid:qrcode" style="width:10%">
                    <br/>
               
                    The swag application is finally completed only when the corresponding qrcode is certified. 
                    <br/>
                    Please authenticate immediately
                    <br/>
                    <img src="cid:qbird" style="width:50%">
                </center>
            </div>
          </body>
        </html>
    """
    
    html_body = MIMEText(html, 'html')
    msg.attach(html_body)
    
    #이미지 세팅
    fp = open(path, 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()
    msgImage.add_header('Content-ID', '<qbird>') #이미지 src 값 넣기 
    msg.attach(msgImage)
    
    fp = open(qr_img_src, 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()
    msgImage.add_header('Content-ID', '<qrcode>') #이미지 src 값 넣기 
    msg.attach(msgImage)

    msg['Subject'] = '[Qoupang] QRCODE Verification'
    msg['To'] = email
    
    smtp.sendmail('qiskitswag@gmail.com', email, msg.as_string())
    smtp.quit()
    
    #블록체인 전송
    
    res = sendblockchain(email_and_qrng,0)
    
    #결과값 리턴
    if res.status_code == 200 :
        txHash = str(res.json()['txHash'])
        print(txHash)
        resp = jsonify({'send': True, 'txHash' : txHash})
        return resp, 200

def getblockchain(email_and_qrng):
    url = "https://swagblockchain.run.goorm.io/swag/"+email_and_qrng
    res = requests.get(url)    
    return res;

def sendblockchain(email, status):
    url = "https://swagblockchain.run.goorm.io/swag"

    data = {'email': email, 'status': status}
    res = requests.post(url, data=data)    
    return res;


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=80, debug=True, threaded=True)

