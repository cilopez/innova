# -*- coding: utf-8 -*-
"""
Created on Wed May 23 21:39:46 2018

@author: camil
"""
import os
import telegram
import time
import threading
from cam_detecter import *
import requests
import classificator
import cv2



class CerianBot:
    def __init__(self,token):
        self.telegram_bot = telegram.Bot(token=token)
        self.updates = []
        self.last = None
        self.querys = {"/hi":self.hi,"/photo":self.photo,"/video":self.video,
                       "/africa":self.toto, "/detect":self.detecter,"/help":self.helper}
        
    def run(self):
        while True:
            time.sleep(1)
            try:
                self.history()
                self.listening()
            except Exception as err:
                print (err)

    def listening(self):
        while 1:
            time.sleep(0.5)
            if not self.updates:
                self.updates = [x.message for x in self.telegram_bot.get_updates()]
                [self.execute(x.message) for x in self.telegram_bot.get_updates()]
                self.last = (self.telegram_bot.get_updates()[-1].message)
                self.history_write()
            else:
                message = (self.telegram_bot.get_updates()[-1]).message
                if str(message) != str(self.last) :
                    self.last = message
                    self.execute(self.last)
                    self.history_write
                    
    def history(self):
        if os.path.isfile('querys.csv'):
            with open("querys.csv","r") as db:
                for elems in db:
                    self.updates.append(elems)
            self.last = self.updates[-1].strip()
                
    def helper(self):
        self.response(message,"The valids commands are /photo \n /video " +
                      "\n /detect \n /hi" )
    
    def history_write(self):
        fake_updates = []
        if os.path.isfile('querys.csv'):
            with open("querys.csv","r") as db:
                for elems in db:
                    fake_updates.append(elems)
        else:
            with open("querys.csv","w") as db:
                pass
        if len(fake_updates) != len(self.updates):
            with open("querys.csv","a") as db:
                for elems in self.updates[len(fake_updates):]:
                    db.write("{}\n".format(elems))
                    
    def detecter(self,message):
        response = classificator.running() 
        self.response(message,response)
        chat_id = message.chat_id
        self.telegram_bot.send_photo(chat_id=chat_id, photo=open('res.jpg', 'rb'))
        freegeoip = "http://freegeoip.net/json"
        geo_r = requests.get(freegeoip)
        geo_json = geo_r.json()
        user_position = [geo_json["latitude"], geo_json["longitude"]]
        chat_id = message.chat_id
        self.telegram_bot.send_location(chat_id=chat_id,
                                        latitude=user_position[0],
                                        longitude=user_position[1])
        
        
    def toto(self,message):
        self.response(message,"I bless the rains down in Africa")
        chat_id = message.chat_id
        self.telegram_bot.send_audio(chat_id=chat_id, audio=open('toto.mp3', 'rb'))
        
        
                
    def hi(self,message):
        self.response(message,"Hola!")
        freegeoip = "http://freegeoip.net/json"
        geo_r = requests.get(freegeoip)
        geo_json = geo_r.json()
        user_position = [geo_json["latitude"], geo_json["longitude"]]
        chat_id = message.chat_id
        self.telegram_bot.send_location(chat_id=chat_id,
                                        latitude=user_position[0],
                                        longitude=user_position[1])
    
    def video(self,message):
        self.response(message,"Video starts")
        video_processing()
        self.response(message,"Video ends")
        
    def photo(self,message):
        path = 'dataset/val/data/images.jpg'
        self.response(message,"Prepare for photo")
        for i in range(0,3):
            time.sleep(0.9)
            self.response(message,"Photo in {}".format(3-i))
        camera = cv2.VideoCapture(0)
        return_value, image = camera.read()
        cv2.imwrite(path, image)
        chat_id = message.chat_id
        del(camera)
        self.telegram_bot.send_photo(chat_id=chat_id, photo=open(path, 'rb'))
            
    
    def response(self,message,text):
        chat_id = message.chat_id
        self.telegram_bot.send_message(chat_id=chat_id, text=text)
    
    def execute(self, message):
        try:
            self.querys[message.text.split(" ")[0]](message)
        except KeyError as err:
            self.response(message,"Consulta inválida")
        with open("querys.csv","a") as db:
                db.write("{}\n".format(message))
            

    


