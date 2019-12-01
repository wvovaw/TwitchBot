# -*- coding: utf-8 -*-
import functional, config
import socket, threading
import re
from time import sleep

def main():
    s = functional.irc_login() 
    # Doing main job in the separate thread
    threading._start_new_thread(chat_job(s))
    # what im gonna do here?


# Listening socket and answering
def chat_job(s):
    while True:
        # Receiving a message from the chat.
        response = s.recv(1024).decode("utf-8")
        if response == "PING :tmi.twitch.tv\r\n":
            s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
        else:
            username = re.search(r"\w+", response).group(0)
            message = functional.chat_message.sub("", response)
            print(response)
            mes = message.strip()
            # Role play kill
            if u"!kill" in mes:
               functional.kill(s, mes, username)
            # Lottery randomly choosing winner from  viewers
            if u"!winner" in mes:
                functional.winner(s)
            # User roll random number 1 - 100
            if u"!roll" in mes:
                functional.roll(s, username)
            # User get the link to resource that he request  
            if mes in config.LINKS.keys():
                functional.links(s, message, username)
            sleep(1)


if __name__ == "__main__":
    main()