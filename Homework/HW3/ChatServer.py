##Arpan Patel##
## Server side##

def usage(file_name):#create function called usage
    #simply just print statement and it will print the program name giving by the user.
    print('Usage: py' + file_name + ' <port number>')


# IMPORT THREADING
'''
This is the library youre going to use to do thread work
'''
#thread modulea allow us manage serval threads of execution
from threading import Thread


def broadcast_messages(sock):#create function called brodcast messages as sock as parameter
    #while the condition is true keep executing. 
    while True:
            #wait for message from one of the client 
            print('Waiting for message...')
            # message recieved from client process it
            message = sock.recv(1024)
            #get the message from client
            if len(message):
                #print the message and decode it for user-readable format.
                print('\nrecieved: ' + message.decode(), end = '')
            else: # there is no bytes are received
                #print this message on server side
                print('recieved no bytes closing socket...')
                #close the socket 
                sock.close()
                #this will remove the client from the list who has left the chat  
                connections.remove(sock)
                break # break it

            #this print on server side saying broadcasting message other clients
            print('now broadcast a message to other clients...' )
            #the code below is going broadcast the messages to all other connected clients
            #this for loop will through the list of connected clients.
            for current_clients in connections:
                #if the client is not in current sock list then
                #do not send the message to master socket
                #and the client who has send us the message
                if current_clients is not sock:
                    #all the other client will get the message.
                    current_clients.send(message)
                   
#create function called accept_client as sock as parameter               
def accept_client(sock):
    #while the condition is true keep executing. 
    while True:
            # wait for a connection and accept it
            sock, addr =serversocket.accept()
            #add client who join the chat to the list
            connections.append(sock)
            #Create a thread for the brocadcasting message
            #target is broadcast_messages and args is sock 
            thread_broadcast = threading.Thread(target = broadcast_messages, args=(sock,))
            #start the thread_broadcast to handle coming connections
            thread_broadcast.start()
              
if __name__== "__main__":
    import sys#module allow us to access the some varaibles used or maintained by the python interpreter.
    import socket#socket module for sockets
    import threading # This is the library youre going to use to do thread work
    connections = [] # create connection as empty list 
    #get command line arguments 
    argc = len(sys.argv) #we set argc to get command line arugment and its length
    if argc != 2: # if the length is not equal 2 then 
        usage(sys.argv[0])#usage will be called and get the port numer
        sys.exit()# or it will exit if the usage is not done right on the command line.

    # create a server objects
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # binds to any available interface
    serversocket.bind(('localhost', int(sys.argv[1])))

    # queue up to 5 requests
    serversocket.listen(5)

    #this just prints starting up server on port whatever port number enter on command line.
    print('waiting for conections on port ' + sys.argv[1] + '...')

    #create thread for the accepting clients
    #target is going to be for accept_client and args is sock
    thread_acceptClient = threading.Thread(target=accept_client, args =(serversocket,))
    #start the thread_accept
    thread_acceptClient.start()
       
