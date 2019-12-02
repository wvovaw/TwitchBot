# -*- coding: utf-8 -*-
import functional, config
import socket, threading
import re
from time import sleep

def main():
    functional.s = functional.irc_login() 
    reminderThread = threading.Thread(target = functional.start_reminds)
    mainThread = threading.Thread(target = chat_job)
    reminderThread.setDaemon(True)
    mainThread.setDaemon(True)
    reminderThread.start()
    mainThread.start()
    mainThread.join()
    reminderThread.join()

# Listening socket and answering
def chat_job():
    while(True):
        # Receiving a message from the chat.
        response = functional.s.recv(1024).decode("utf-8")
        if response == "PING :tmi.twitch.tv\r\n":
            functional.s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
        else:
            username = re.search(r"\w+", response).group(0)
            message = functional.chat_message.sub("", response)
            print(response)
            mes = message.strip()
            # Role play kill
            if u"!kill" in mes:
               functional.kill(message, username)
            # Lottery randomly choosing winner from  viewers
            if u"!winner" in mes:
                functional.winner()
            # User roll random number 1 - 100
            if u"!roll" in mes:
                functional.roll(username)
            # User get the link to resource that he request  
            if mes in config.LINKS.keys():
                functional.links(message, username)
            # Reminder that works on seted time. syntax: !remind hh:mm "MESSAGE1", hh:mm hh:mm "MESSAGE2"
            if u"!remind" in mes:
                functional.add_remind(mes)
        sleep(1)


if __name__ == "__main__":
    main()