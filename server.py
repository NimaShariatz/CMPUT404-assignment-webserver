#  coding: utf-8 
import socketserver

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        print("***********NEW TEST*************")
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data) #b'GET / HTTP/1.1\r\nHost: 127.0.0.1:8080\r\nUser-Agent: curl/8.0.1\r\nAccept: */*'
        self.request.sendall(bytearray("OK",'utf-8'))
        
        dataInput = self.data.decode('utf-8')

        requested_command = dataInput.split('\r\n')
        print("requested_command: ", requested_command)#['GET / HTTP/1.1', 'Host: 127.0.0.1:8080', 'User-Agent: curl/8.0.1', 'Accept: */*']
        requested_command = requested_command[0]
        print("requested_command: ", requested_command)#GET / HTTP/1.1
        
        
        command_type = requested_command.split(' ')
        print("command_type: ", command_type)#['GET', '/', 'HTTP/1.1']
        command_type = command_type[0] 
        print("command_type: ", command_type)#GET

        
        requested_val = requested_command.split(' ')
        print("requested_command: ", requested_val)# ['GET', '/', 'HTTP/1.1']
        requested_val=requested_val[1]
        print("requested_command: ", requested_val) # /
        
        print()
        
        
        #so what next?
        
        
        

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
