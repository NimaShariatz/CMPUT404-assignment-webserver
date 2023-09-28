#  coding: utf-8 
import socketserver, os

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

#Click on link above when server running!


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        #print("***********NEW TEST*************")
        self.data = self.request.recv(1024).strip()
        
        dataInput = self.data.decode('utf-8')

        requested_command = dataInput.split('\r\n')
        #print("requested_command: ", requested_command)#['GET / HTTP/1.1', 'Host: 127.0.0.1:8080', 'User-Agent: curl/8.0.1', 'Accept: */*']
        requested_command = requested_command[0]
        #print("requested_command: ", requested_command)#GET / HTTP/1.1
        
        
        command_type = requested_command.split(' ')
        #print("command_type: ", command_type)#['GET', '/', 'HTTP/1.1']
        command_type = command_type[0] 
        #print("command_type: ", command_type)#GET

        
        the_path = requested_command.split(' ')
        #print("requested_val: ", the_path)# ['GET', '/', 'HTTP/1.1']
        
        try:#sometimes when you move between pages quickly, an error in the server side pops up. it causes no issues though, just some print lines.
            the_path=the_path[1]#i suspect it has something to do with the socket, which is outside of the scope of this assignment
        except:#the try and except is not necassary. as i said, it doesnt cause any issues regardless other than a few print lines in server
            
            #print(requested_command.split(' '),"AND",the_path) #these will appear empty when the socket side error occurs, but the page still works.
            pass#perphaps its because we are using TDP and its merely getting the data again after it missed out on it when switching quickly between pages
        #print("requested_val: ", the_path) # /
        
        #print()
       
        
        code_200 = "HTTP/1.1 200 OK\r\n" #type out the error codes here as variables, it will look neater
        
        code_301 = "HTTP/1.1 301 Move Permanently\r\n"
        
        code_404 = "HTTP/1.1 404 Not Found\r\n"
        
        code_405 = "HTTP/1.1 405 Method Not Allowed\r\n"
        
        
        #405 error checking
        check_405 = self.send_405(command_type, code_405)
        if check_405 == False:#405 found an error so end it the program
            return# end the program
        #405 error checking
        
        else:
            
            #print(the_path, "passed 405")
            #301 error checking
            check_301 = self.send_301(the_path, code_301)
             
            if(check_301==False):#301 picked up an error
                return
            #print(the_path, "passed 301") 
            #301 error checking
            
            temp = the_path.count('.')
            if temp < 1:
                #print("the period count is", temp, "on" , the_path, "so index.html was added")
                the_path+="index.html"
                
            
            the_path = "./www" + the_path
            if the_path[-1] == "/":
                the_path = the_path[:-1]
                #print("/ added to end of", the_path)
            
            #404 error checking
            check_404 = self.send_404(the_path, code_404)
            if (check_404 == True):# if 404 passed
                #print("404 path found with:", the_path)
                content_type = ""
                if(the_path.endswith(".html")):
                    content_type = "Content-type: text/html\r\n\r\n"
                    #print(the_path, "ends with .html")
                elif(the_path.endswith(".css")):
                    #print(the_path, "ends with .css")
                    content_type = "Content-type: text/css\r\n\r\n"
            #404 error checking
            
                
                
                self.send_200(the_path, content_type, code_200)
                
                return
            
            else:#it means 404 did return false and failed the test. so end program
                return
        
            
        
        
        
        
        
        
        
        
        
        
    def send_405(self, command_type, status_code):
        
        if command_type != "GET":
            #print("405 raised there is no GET in", command_type)
            self.request.sendall(status_code.encode())
            return False
        else:
            return True
    
    def send_301(self, the_path, status_code):
        #print("301 function - the path:", the_path, "the_path[-1]->", the_path[-1], "the path at split(/)[-1]->", the_path.split("/")[-1])
        if ((the_path[-1] != "/") and ("." not in the_path.split("/")[-1])):
            corrected_path = the_path + "/"
            
            
            #print("301 raised with", the_path, "Corrected: ", corrected_path)
            status_code = status_code + "Location:" + corrected_path
            self.request.sendall(status_code.encode())
            return False
        else:
            return True

    def send_404(self, the_path, status_code):
        if os.path.exists(the_path) and ((".html" in the_path) or (".css" in the_path)):
            return True
        else:
            self.request.sendall(status_code.encode())
            #print("404 raised with" , the_path, "path not found")
            return False
    
    def send_200(self, the_path, content_type, status_code):
        
        file = open(the_path, "r")
        data = file.read()
        file.close()
        
        collection = status_code + content_type + data
        #print("200 raised with", the_path)
        self.request.sendall(collection.encode())

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
