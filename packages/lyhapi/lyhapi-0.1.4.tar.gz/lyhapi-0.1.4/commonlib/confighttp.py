# coding=utf-8
"""
Author：Vissy Zhu
"""
import requests
import urllib3
import ssl
import logging
import datetime

ssl._create_default_https_context = ssl._create_unverified_context
logging.basicConfig(filename='log.txt', level=logging.DEBUG)


class ConfigHttp():

    def __init__(self, scheme, api_url, www_url, web_url, port):
        self.scheme = scheme
        self.api_url = api_url
        self.www_url = www_url
        self.web_url = web_url
        self.port = port
        self.headers = {}
        self.params = {}
        self.data = {}
        self.url = {}
        # self.files = {}
        self.state = 0

    def set_url(self, url):
        """
        set url
        :param: interface url
        :return:
        """
        self.__url = self.scheme + '://' + self.api_url + url

    def set_www_url(self, url):
        """
        set url
        :param: interface url
        :return:
        """
        self.__url = self.scheme + '://' + self.www_url + url

    def set_web_url(self, url):
        """
        set url
        :param: interface url
        :return:
        """
        self.__url = self.scheme + '://' + self.web_url + url

    def set_headers(self, header):
        """
        set headers
        :param header:
        :return:
        """
        self.headers = header

    def set_params(self, param):
        """
        set params
        :param param:
        :return:
        """
        self.params = param

    def set_data(self, data):
        """
        set data
        :param data:
        :return:
        """
        self.__data = data

    # defined http_data.py get method
    def get(self):
        """
        defined get method
        :return:
        """
        try:
            # urllib3.disable_warnings()
            start_time = datetime.datetime.now()
            response = requests.get(self.__url, headers=self.headers, params=self.params, verify=False)
            logging.info(f"执行时间: {start_time}")
            logging.info(f"Request URL: {self.__url}")
            logging.info(f"Request Parameters: {self.params}")
            logging.info(f"Request Headers: {self.headers}")
            logging.info(f"Response Content: {response.text}")
            return response
        except TimeoutError:
            return None

    # defined http_data.py post method
    # include get params and post data
    # uninclude upload file
    def post(self):
        """
        defined post method
        :return:
        """
        try:
            urllib3.disable_warnings()
            start_time = datetime.datetime.now()
            response = requests.post(self.__url, params=self.params, headers=self.headers, json=self.__data,
                                     verify=False)
            logging.info(f"执行时间: {start_time}")
            logging.info(f"Request URL: {self.__url}")
            logging.info(f"Request Parameters: {self.params}")
            logging.info(f"Request Headers: {self.headers}")
            logging.info(f"Request Body: {self.__data}")
            logging.info(f"Response Content: {response.text}")
            return response
        except TimeoutError:
            return None

    def delete(self):
        """
        defined delete method
        :return:
        """
        try:
            urllib3.disable_warnings()
            start_time = datetime.datetime.now()
            response = requests.delete(self.__url, params=self.params, headers=self.headers, json=self.__data,
                                       verify=False)
            logging.info(f"执行时间: {start_time}")
            logging.info(f"Request URL: {self.__url}")
            logging.info(f"Request Parameters: {self.params}")
            logging.info(f"Request Headers: {self.headers}")
            logging.info(f"Request Body: {self.__data}")
            logging.info(f"Response Content: {response.text}")
            return response
        except TimeoutError:
            return None

    def put(self):
        """
        defined post method
        :return:
        """
        try:
            urllib3.disable_warnings()
            start_time = datetime.datetime.now()
            response = requests.put(self.__url, headers=self.headers, params=self.params, json=self.__data,
                                    verify=False)
            logging.info(f"执行时间: {start_time}")
            logging.info(f"Request URL: {self.__url}")
            logging.info(f"Request Parameters: {self.params}")
            logging.info(f"Request Headers: {self.headers}")
            logging.info(f"Request Body: {self.__data}")
            logging.info(f"Response Content: {response.text}")
            return response
        except TimeoutError:
            return None
