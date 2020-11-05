# -*- coding: utf-8 -*-


#Author: Myles Wright
#Date: 10/02/20
#Filename: web_server.py
#HTTP Web Server that listens to ports, recieves requests, and responds 

import json
import socket
import re
import sys
import os
import threading
import datetime
from _thread import start_new_thread
from request import request
from response import response


class connection(threading.Thread):
    '''class for multithreaded connections'''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = 0
    port = 0
    lock = threading.Lock()                         #saw a really cool tutorial for multithreading that included this
    codes = {
            "200": "OK",
            "404": "NOT FOUND",
            "503": "SERVICE UNAVAILABLE"
        }
    root = ["index.html", "home.html"]
    server_name = "Myles' badass server 2.0"
    mime_types = {                                  #better way to add the header using mime-types that you helped with
            "html": "text/html",
            "css": "text/css",
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "png": "image/png",
            "ico": "image/x-icon"
        }
    def __init__(self, host, port):
        '''initialize the connection'''
        self.host = host
        self.port = port
        try:
            self.sock.settimeout(200)
            self.sock.bind((self.host, self.port))
        except socket.error:
            print("Error creating socket")
            sys.exit(1)
        self.client_requests = []
        self.responses = []
            

    def listen(self):
        '''function that listens to a specific port number. uses threading'''
        try:
            self.sock.listen(200)
                                                    #I saw this .format on stackoverflow
            print("Listening for connections on port {0}".format(self.port)) 
            
            while True:
                connection, address = self.sock.accept()
                message = connection.recv(1024)
                print("Connected to {0}{1}".format(address[0], "\n"))
                if(message == None):
                    continue
                else:
                    start_new_thread(self.parse, (message, address, connection, ))
        except socket.error:
            print("Error listening")
        except socket.timeout:
            print("Connection timed out!")
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()
        

    def parse(self, c, addr, conn):
        '''parses the data and puts it into a request object. Then the request object is added to the array of requests'''
        s = c.decode('UTF-8')                       #split the string into an array
        
        lines = s.split("\r\n")
        a = re.split(" +", lines[0])

                                                    #assign the variables to a request object
    
        req = request(a[0], a[1])                   #since req requires the method and path to be initialized, this has to be done before the loop
        
                                                    #set headers
        for b in lines:
            if lines.index(b) == 0:                 #do not want to repeat what we already did.
                continue
            if(b == ''):                            #last two values are '', if left to be split, they will cause an out of index error
                continue
            else:
                a = b.split(": ")                   #split headers by ':'
                req.add_header(a[0], a[1])          # a is [header, value] in this case
        self.lock.acquire()
        req.to_string()                             #print for logging
        self.lock.release()

        self.client_requests.append(req)           #add to list of requests 
        self.generate_response(req, addr, conn)


    def generate_response(self,request, addr, conn):
        '''assigns values to response class based on request object'''
        resp = response()                           #create response object

        path = request.get_path()                   #doing some cleaning up :)
        if(path == "/"):
            requested_data_type = "html"
        if(path != "/"):
            path_split = path.split(".")
           
            requested_data_type = path_split[1]
            
        else:
            requested_data_type = "html"
        resp.set_version("HTTP/1.1")
        self.set_server(resp)
        self.set_content_type(requested_data_type, resp)
        self.get_data(request, resp)
        self.set_response_code(request, resp)
        self.set_date_time(resp)
                    
        self.lock.acquire()                         #print response for logging
        self.responses.append(resp)
        print("Response to client:\n{0}".format(resp.to_string()))
        self.lock.release()

                                                    
        try:
            conn.sendall(resp.to_send())
            conn.sendall(resp.get_byte_data())      #send the data
            conn.close()
            print("Sent response")
        except socket.error as v:
            print("Socket error: {0}".format(str(v)))
        
        

    def set_content_type(self, requested_data_type, response):
        '''sets the content-type header'''
        response.add_header("content-type", self.mime_types[requested_data_type])
        
        
    def get_data(self, request, response):
        '''gets the data to send'''
        if(request.get_path() == "/"):
            req_file = "index.html"
        else:
            self.lock.acquire()
            request.to_string()                     #print request for logging
            self.lock.release()
            req_file_split = request.get_path().split("/")
            req_file = req_file_split[1]
            

        self.set_content_length(response, req_file)
        
                                                    #loop through root list and get data
        if(response.get_header("content-type") == "text/html"):
            for x in self.root:
                if(x == req_file):
                    total = self.read_file(req_file)
                    response.set_data(total)
            
                                                    #loop through mime types and get correct data
        type_ = response.get_header("content-type")
        for x, y in self.mime_types.items():
            if(type_ == y):
                total = self.read_file(req_file)
                response.set_data(total)

        
    def set_response_code(self, request, response):
        '''sets the response code based on other factors and if they are met'''                                        
        if(response.get_data() != ''):              #at this point the data is set so if there is no data, nothing was found
            response.set_code("200" + " " + self.codes["200"])
            self.set_connection(response, "keep-alive")
        if(response.get_data() == ''):
            response.set_code("404" + " " + self.codes["404"])
            self.set_connection(response, "closed")
        if(request.get_method() != "GET"):          #This server does not allow for posting
            response.set_code("503" + " " + self.codes["503"])
            self.set_connection(response, "closed")
        
        
    def set_content_length(self, response, file_name):
        '''sets the content length header in the response'''
        size = os.path.getsize(file_name)
        response.add_header("content-length", size)


    def set_date_time(self, response):
        '''sets the time header in the response'''
        response.add_header("Date", datetime.datetime.now())


    def set_connection(self, response, connection):
        '''sets the connection header'''
        response.add_header("Connection", connection)


    def read_file(self, file_name):
        '''reads the file and returns the raw data'''
        total = bytes()
        with open(file_name, 'rb') as f:
            bytes_read =  f.read()
            total = total + bytes_read
        return total


    def set_server(self, response):
        '''sets the server name'''
        response.add_header("Server", self.server_name)


def main():
    sock = connection("localhost", 8080)
    
    sock.listen()

    
if __name__ == '__main__':
    main()
