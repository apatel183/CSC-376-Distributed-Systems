#Arpan Patel# 
#Messgener server/client
# create a direct messenger program.

import sys#module allow us to access the some varaibles used or maintained by the python interpreter.
import socket#socket module for sockets

#Giving useful information to the user. 
def usage( script_name ): #create function called usage
    #simply just print statement and it will print the program name giving by the user.
    print( 'Usage: py ' + script_name + ' <port number>' + '[<server address>]' )

# IMPORT THREADING
'''
This is the library youre going to use to do thread work
'''
#thread modulea allow us manage serval threads of execution
from threading import Thread

'''
The easiest way to handle your threads and sending/receiving messages will be
to create a couple methods for send/receive
'''

def send_message(sock):
    '''
    This is going to be my sender, the thread will use this as the "target"
    '''
    #while the condition is true keep executing. 
    while True:
        #try this block of code 
        try: 
            # Get user input for message and then encode it so it can be sent over
            #the socket connection
            message = input().encode()
            ## This checks to see if you just sent a blank message.
            # If so, then break out of the while loop and the thread will end.
            if not sock.send(message):
                break
            
        #no action required when a socket exception occurs so we will just do pass. 
        except: 
            pass

def receive_message(sock):
    '''
    This will be the receiver, also "target" for threads
    '''
    #while the condition is true keep executing. 
    while True:
        # Try to receive a message (this will wait until a message is received)
        # Decode it for user-readable format.
            message = sock.recv(1024).decode()
        # If a blank message was received, then break out of loop and thread will end
            if not message:
                break #break it 
            print(message) #print the message
        
    
#create threads 
def create_threads(sock): # creating the function and name is "create_threads" and parameter as "sock"
    '''
    Note: same thing for both threads, just different target.
    
    Create a thread for the sender:
        target = send_message : The thread will call send_message()
        args   = (sock,)      : The thread will pass (sock,) to send_message
    
    (sock,) explanation
        - Thread takes args as a tuple, so you need to pass sock as a tuple.
        - If you just do (sock), it wont pass it as a tuple. So you need the comma after it
        - Just a Python quirk
    '''
    #target = send_message : The thread will call send_message()
    #args   = (sock,)      : The thread will pass (sock,) to send_message
    _send     = Thread(target = send_message,    args = (sock,))
    
    #target = receive_message: The thread will call receive_message()
    #args   = (sock,)      : The thread will pass (sock,) receive_message
    _receive  = Thread(target = receive_message, args = (sock,)) 
    
    # daemon just means (from my understanding) that the program will exit when both threads are dead.
    #By setting them as daemon threads, we can let them run and forget about them, and when our program quits,
    _send.daemon     = True #send we set as TRUE
    _receive.daemon  = True ##daemon we set as TRUE
    
    # Start both threads
    _send.start() #start the send thread
    _receive.start()#start receive thread
    
    # This returns a tuple of _send and _receive, the threads.
    return (_send, _receive)


args= sys.argv[1:] #we set args to get command line arugment but we want to start at index 1 that so it won't print the program name and start counting from name.py. 
opt = '-l' #set opt equal "-l"
host = "Localhost" # set host has "localhost"
if opt == args[0]: # this if statment will get the command line argument and we have correct information
    port_number = int(args[1]) #assigned to port number from whatever user have enter 
    print("Starting up server on port: " + str(port_number)) #this just prints starting up server on port whatever port number enter on command line.

    # create a communicator object below two lines
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # binds to any available interface
    serversocket.bind((host,port_number)) 

    # queue up to 5 requests
    serversocket.listen(5)
    
    # wait for a connection and accept it
    sock, addr= serversocket.accept()

    # Since create_threads() returns a tuple with two values,
    # you can just set server_send, server_receive = create_threads(sock)
    # Python will automatically assign the correct objects to them.    
    server_send, server_receive = create_threads(sock)

    '''
    Now  we  just  wait  until  both  threads  are dead.
    We  do   this  by   calling  THREADNAME.isAlive()  in  a while  loop  for  both  threads
    When  one or  both  threads  are no   longer  alive,  we  break  out  of  the  loop  and
    close  the  socket  connection.
    '''
    #server send and receive  
    while server_send.isAlive() and server_receive.isAlive():
        continue

    sock.close() #close the socket
    print("[received no bytes; closing socket....]")#print the message "zero bytes receieved 


#client code 
else:
    #assigned to port number from whatever user have enter AS portnumber
    port_n = int(args[0])
    
    #this just prints starting up server on port whatever port number enter on command line.
    print("Starting up client on port: "  + str(port_n)) 

    # create a communicator object
    host = "Localhost"

    # create a communicator object
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    #our case we doing localhost that users puts it on command line
    sock.connect((host, port_n))

    # Since create_threads() returns a tuple with two values,
    # you can just set client_send, client_receive = create_threads(sock)
    # Python will automatically assign the correct objects to them.    
    client_send, client_receive = create_threads(sock)
    
    '''
    Now  we  just  wait  until  both  threads  are dead.
    We  do   this  by   calling  THREADNAME.isAlive()  in  a while  loop  for  both  threads
    When  one or  both  threads  are no   longer  alive,  we  break  out  of  the  loop  and
    close  the  socket  connection.
    '''
    #client send and receive 
    while client_send.isAlive() and client_receive.isAlive():
        continue
    
    sock.close() #close socket
    print("[closing the socket....]") #print the message when we are ending the chat. 

    


              
        
        
    


