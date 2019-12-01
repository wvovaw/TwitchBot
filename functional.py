# -*- coding: utf-8 -*-
import config
import re
import json
import socket
import urllib.request as ur
import datetime as dt
from random import randint
from time import sleep
from threading import Lock

chat_message = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
# Compile and send a message
def mess(s, message):
    s.send("PRIVMSG #{} :{}\r\n".format(config.CHAN, message).encode("utf-8"))

# Log in to twitch irc
def irc_login():
    s = socket.socket()
    s.connect((config.HOST, config.PORT))
    s.send("PASS {}\r\n".format(config.PASS).encode("utf-8"))
    s.send("NICK {}\r\n".format(config.NICK).encode("utf-8"))
    s.send("JOIN #{}\r\n".format(config.CHAN).encode("utf-8"))
    return s

# Fetching JSON with viewers list and choose a random one
def winner(s):
    try:
        req = ur.Request(config.URL, headers={"accept": "*/*"})
        res = ur.urlopen(req).read()
        if res.find("502 bad gateway".encode("utf-8")) == - 1:
            data = json.loads(res)
            config.CHATTERS = data['chatters']['viewers']
    except:
        return "Error 228"
    mess(s, config.CHATTERS[randint(0, len(config.CHATTERS))])
    
#Role play kill
def kill(s, message, username):
    oponent = message[5:]
    if oponent == "\r\n":
         return None
    else:
        if "@" in oponent:
            oponent =  oponent[1:]
        destiny = randint(0,1)
        danet = ['', ' don\'t']    
        des = ['[Succsess] ', '[Fail] ' ]
        mess(s, (des[destiny] + username + danet[destiny] + " kill " + oponent))
    
# User roll random number 1 - 100
def roll(s, username):
    mess(s, str(username + " rolls " + str(randint(1, 100)) + " points"))

# Links and contacts
def links(s, message, username):
    mess(s, str(username + ", look there " + config.LINKS[message[0:-2]]))

# Reminder. write timings and message between " ". It will be sent on the specified times
# Split reminds with comma
# Example: !remind 6:00 "Morning!", 04:20 5:00 "Tea time :)", 0:00 "Midnight!"
# Remember, when you add new remind to a time that is already has a remind, it will be overwriten with a new message!
# Example:
# !remind 6:00 "Morning!"
# !remind 6:00 "Good morning!"
# REMINDS['6:00'] = "Good morning!"
# ---
# Parsing an initial string to split it on [(times) "message"]
def start_reminds(s):
    a = 0
    while(True):
        print(a)
        a += 1
        now = (dt.datetime.strptime(dt.datetime.strftime(dt.datetime.today(), '%H:%M'), '%H:%M')).time()
        for key in config.REMINDS:
            if(now == dt.datetime.strptime(key, '%H:%M').time()):
                mess(s, str('@' + config.CHAN + ', It\'s ' + str(key) + '. ' + config.REMINDS[key]))
                del config.REMINDS[key]
                break
        sleep(1)

# Adding new remind
def add_remind(message):
    message = message[7:]
    print('Init message: ' + message)
    remindList = message.split(",")
    print('RemindList')
    for item in remindList:
        print(item)
        set_reminds(item)
    print('REMINDS:')
    for key in config.REMINDS:
        print('Timing: ' + key + ' message: ' + config.REMINDS[key])
    
# Assembling reminds list
def set_reminds(message):
    matchTimes = re.findall(r'(([01]?[0-9]|2[0-3]):([0-5][0-9]))', message)
    if(matchTimes):
        try: 
            mes = (message.split("\"")[1])
        except:
            return None
        for hm in range(0, len(matchTimes)):
            config.REMINDS[str(matchTimes[hm][0])] = mes