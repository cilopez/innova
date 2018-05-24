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

class CerianBot:
    def __init__(self,token):
        self.telegram_bot = telegram.Bot(token=token)
        self.updates = []
        self.last = None
        self.querys = {"/get":self.get,"/photo":self.photo,"/video":self.video}
        
    def run(self):
        while True:
            time.sleep(0.5)
            try:
                self.history()
                self.listening()
            except TimedOut as err:
                self.history()
                self.listening()

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
                
    def get(self,message):
        self.response(message,"Hola!")
    
    def video(self,message):
        self.response(message,"Video starts")
        video_processing()
        
    def photo(self,message):
        self.response(message,"Prepare for photo")
        for i in range(0,3):
            time.sleep(0.9)
            self.response(message,"Photo in {}".format(3-i))
            
    
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
            

    


