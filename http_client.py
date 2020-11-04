# -*- coding: utf-8 -*-


#Author: Myles Wright
#Date: 09/10/2020
#Filename: http_client.py
#HTTP client that sends a request to https://httpbin.org 

import json
import socket
import re
import sys
import threading
from request import request
from response import response

class client(threading.Thread):

    def __init__(self):
        '''empty initializer'''


    def send_socket(self, message, ipaddress, port_num):
        ''' This function sends a string message over TCP'''
        #Most of this function I took from the slides on canvas. There are other ways to do this that I found but I like this one the most.

        server = ipaddress
        port = port_num
        try:
            print("Connecting...")
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((server, port))
        except ConnectionError:
            print("Error connecting... ")
            sys.exit(1)
        except socket.gaierror:
            print("Error connecting... ")
            sys.exit(1)
        try:
            print("Sending...")
            sock.sendall(message)
            print("Sent!" + "\n")
        except socket.error:
            print("Failed")
            sys.exit(1)
        try:
            print("Recieving response...")
            response = sock.recv(1024)
        except socket.RDS_RECVERR:
            print("Error recieving data...")
            sys.exit(1)
        return response
   





'''def main():
    #set up the request
    user_input = input("Request: ")
    a = re.split(' +', user_input)
    
    r = request(a[0], a[1])
    
    #send the request, assign it to response
    req = send_socket(r.toString())
    resp = response(req.decode('UTF-8'))
    print(resp.toString())
    #print(resp.decode('UTF-8'))




if __name__== '__main__':
    main()

'''