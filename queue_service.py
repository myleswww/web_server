# -*- coding: utf-8 -*-


#Author: Myles Wright
#Date: 10/02/20
#Filename: queue_service.py
#Queue monitor that sends responses based on requests in a queue

import json
import socket
import re
import sys
import threading
from _thread import start_new_thread
#from http_client import http_client
from request import request
from response import response
''' First, the queue object is sent to the generate response function,
    then the response is ***crafted***
    then the response is sent to the client, and based on the boolean that the client gives back,
    the status[] is set to 1 or 0. if the status is 1, then the request is moved to the back of the queue 
    so it can be tried again later.
    I also wanted to use a service like beanstalkd for this but alas, I just made my own simple queue service'''

class queue_service(threading.Thread):
    status_code = '0'
    queue = []

    def __init__(self, queue):
        self.queue = queue

    def queue_cycle(self):
        #does stuff

    #def send_response(self, response):
        #'''sends the response'''

    

    
