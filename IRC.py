import sys
import socket
import string
import pickle
from threading import Thread


def print_analysis(features):
    print movie_classifier.classify(features)
    print twitter_classifier.classify(features)

HOST = "irc.chat.twitch.tv"
PORT = 6667
NICK = "wklock"
IDENT = "wklock"
REALNAME = "wklock"
PASS = "oauth:xp9mrmbwfydp15z3uil2fbxgrvoguq"
CHANNEL = "bacon_donut"
readbuffer = ""
message = ""

s = socket.socket()
s.connect((HOST, PORT))
s.send("PASS %s\r\n" % PASS)
s.send("NICK %s\r\n" % NICK)
s.send("JOIN #%s\r\n" % CHANNEL)
movie_classifier = pickle.load(open("movie_reviews_NaiveBayes.pickle"))
twitter_classifier = pickle.load(open("nbc1000.pickle"))
while 1:
    readbuffer = readbuffer + s.recv(1024)
    temp = string.split(readbuffer, "\n")
    readbuffer = temp.pop()

    for line in temp:
        line = string.rstrip(line)
        split_line = string.split(line)
        split = split_line[2]
        message = line.split(split, 1)
        message = message[1]
        #print message[2:]
        feats = dict([(word, True) for word in message])
        t = Thread(target=print_analysis, args=(feats,))
        t.start()
