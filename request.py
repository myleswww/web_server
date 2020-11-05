# -*- coding: utf-8 -*-


#Author: Myles Wright
#Date: 09/10/2020
#Filename: request.py
#HTTP client that sends a request to https://httpbin.org 

import json
import socket
import re
import sys
import threading

                                                #request class
class request(object):
    method = " "
    path = " "
    version = "HTTP/1.1"
    headers = {
               }    
    data = " " 
    Data = bytearray()
    
    
    def set_method(self, type_input):  
        """set the method to GET or POST"""
        self.method = type_input
        return type_input


    def get_method(self):
        '''returns the method'''
        return self.method    


    def set_path(self, input):
        """set the path to the target resource"""
        self.path = input
        return input
        

    def get_path(self):
        '''return path'''
        return self.path


    def set_data(self, input):
        """add the data for POST requests"""
        self.data = input
        return input


    def add_header(self, header, value):
        """add a header to the request"""
        self.headers[header] = value
    

    def get_header(self,header):
        return self.headers[header]


    def get_headers(self):
        """returns a string of correctly formatted dictionary items"""
        formatted_headers = "\n"
        for key, value in self.headers.items():
            formatted_headers = formatted_headers + f"{key}: {value}\n"
        return formatted_headers


    def to_string(self):
        """prints the request formatted like we saw in class(use json)"""
        sp = " "
        self.set_data(str(self.version + sp + self.method + sp + self.path + sp + self.get_headers() + "\n"))
        print(self.data)
        
    
    def __init__(self, type_input, path):
        """Does everything to return a string of the data"""
        self.method =  self.set_method(type_input)
        self.path = self.set_path(path)