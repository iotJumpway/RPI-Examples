"""
An image server running in a separate thread. Used to display images over HTTPS GET request
and avoiding race conditions.
usage:
# instantiate server thread with default image
server = ImageServerThread("./img/unavailable.jpg")
# run the server in a separate thread
server.start()
# pass a bytearray containing a .jpg's data to be displayed to the server thread
# this is a non-blocking function that will only write the data if thread is unlocked
# returns True on success and False on failure
server.write(data)
note that read and write are non-blocking (i.e. they just pass through when mutex is locked
and read_blocking and write_blocking are their blocking counterparts that will wait for the
mutex to be released and block the thread until done.
Currently ImageServerThread.run() is using read_blocking() to send image over HTTPS, so
the thread providing the image should use write(), not write_blocking(). This should, in theory,
prefer fast performance of the device vs. faster refresh rates on the application. If too "jumpy"
try the other way around!
"""

import copy
import threading
import io
import os
import ssl
import json

from flask import Flask, send_file
from flask_basicauth import BasicAuth

CONTEXT = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
CONTEXT.load_cert_chain(os.getcwd()+"/certs/crt.crt", os.getcwd()+"/certs/key.key")

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

class ImageServerThread(threading.Thread):

    def __init__(self, defaultFilePath = None):
        threading.Thread.__init__(self)
        if defaultFilePath:
            self.__data = open(defaultFilePath, "rb").read()
        else:
            self.__data = None
        self.__prevData = self.__data
        self.lock = threading.Lock()
        self.__active = False

        with open('config.json') as configs:   

            self._configs = json.loads(configs.read())

    def read(self):
        if self.lock.acquire(0):
            self.__prevData = self.__data
            ret = copy.deepcopy(self.__data)
            self.lock.release()
            return ret
        else:
            return None

    def write(self, inputData):
        if self.lock.acquire(0):
            self.__data = inputData
            self.lock.release()
            return True
        else:
            return False

    def read_blocking(self):
        self.lock.acquire()
        self.__prevData = self.__data
        ret = copy.deepcopy(self.__data)
        self.lock.release()
        return ret

    def write_blocking(self, inputData):
        self.lock.acquire()
        self.__prevData = self.__data
        self.__data = inputData
        self.lock.release()

    def active(self):
        return self.__active

    def run(self):
        """
        runtime of the Flask server
        """
        global CONTEXT

        self.__active = True
        app = Flask(__name__)

        app.config['BASIC_AUTH_FORCE'] = True
        app.config['BASIC_AUTH_USERNAME'] = self._configs["AppServerSettings"]["serverUser"]
        app.config['BASIC_AUTH_PASSWORD'] = self._configs["AppServerSettings"]["serverPassword"]

        basic_auth = BasicAuth(app)

        @app.route("/")
        @basic_auth.required
        def displayImg():
            image = self.read_blocking()
            if image:
                return send_file(io.BytesIO(image), attachment_filename="disp.jpg", mimetype="image/jpg")
            else:
                return send_file(io.BytesIO(self.__prevData), attachment_filename="disp.jpg", mimetype="image/jpg")
              
        app.run(host=self._configs["AppServerSettings"]["serverIP"], port=4326, debug=False, ssl_context=CONTEXT)