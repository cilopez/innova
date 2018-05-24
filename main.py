# -*- coding: utf-8 -*-
"""
Created on Thu May 24 09:08:16 2018

@author: camil
"""
from bot import CerianBot
from ENV import TOKEN

if __name__ == "__main__":
    bot = CerianBot(TOKEN)
    bot.run()
    