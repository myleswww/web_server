# -*- coding: utf-8 -*-


#Author: Myles Wright
#Date: 09/10/2020
#Filename: response.py
#HTTP client that sends a request to https://httpbin.org 

import json
import socket
import re
import sys
import threading

class response(object):
    version = ""
    code = ""
    message = ""
    headers = {}
    data = ""
    Data = bytearray()


    def __init__(self, response):
        """set the response headers in the class dict object"""
        
        self.data = response

    
    def __init__(self):
        '''create an empty response'''

    def set_code(self, code):
        '''sets the response code and the response message'''    
        self.code = code

    def add_header(self, header, value):
        '''adds a header to the response'''
        self.headers[header] = value

    def get_header(self, header):
        """return the value of the specified header"""
        return self.headers[header]

    def get_headers(self):
        """returns a string of correctly formatted dictionary items"""
        formatted_headers = "\n"
        #print("Formatting headers...")
        for key, value in self.headers.items():
            formatted_headers = formatted_headers + f"{key}: {value}\n"
        #print(formatted_headers)
        return formatted_headers

    def set_data(self, data):
        '''may take file contents instead of path if that works'''
        self.data = data.decode('UTF-8', 'ignore')
        self.Data = data


    def set_version(self, version):
        '''sets the version variable'''
        self.version = version

    def get_data(self):
        """return just the data from the response"""
        return self.data

    def get_byte_data(self):
        return self.Data


    def to_string(self):
        """prints the request formatted like we saw in class"""
        message = str(self.version + " " + self.code + self.get_headers() + "\n")
        
        return message

    def to_send(self):
        message = (self.version + " " + self.code + self.get_headers() + "\n").encode('UTF-8') + (self.get_byte_data()) + ("\n").encode('UTF-8')
        return message



