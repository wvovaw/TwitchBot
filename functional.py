# -*- coding: utf-8 -*-
import config
import re
import json
import socket
import urllib.request as ur
from random import randint

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
