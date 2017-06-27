### Arpan Patel ###
## ChatClient ##

#Giving useful information to the user. 
def usage(file_name):#create function called usage
    #simply just print statement and it will print the program name giving by the user.
    print('Usage: py' + file_name + ' <port number>')

# IMPORT THREADING
'''
This is the library youre going to use to do thread work
'''
#thread modulea allow us manage serval threads of execution
from threading import Thread

def send_message(sock): #create send_message fucntion with sock as parameter
    '''
    This is going to be my sender, the thread will use this as the "target"
    '''
    #while the condition is true keep executing. 
    while True:
        #try this block of code
        try:
            print('Enter your message: ', end= '') # print message and where user can type it 
            sys.stdout.flush() # this line flush out after each print to keep buffer clean
            #and write everything in the buffer to terminal.
            message = sys.stdin.readline()#read message from standard input 
            
            ## This checks to see if you just sent a blank message.
            # If so, then break out of the while loop and the thread will end.
            if not message:
                break
            #trasmit the message as bytes(which is what send/recv uses)
            sock.send(message.encode())
        except KeyboardInterrupt: # this line check except the keyboard interrupt.
            #this just print line and give useful info to users. 
            print ("press Ctrl d(on mac) or Ctrl z(on windows) to end the chat...")
        
        
def receive_message(sock): #create receive message with sock as parameter.
    '''
    This will be the receiver, also "target" for threads
    '''
    #while the condition is true keep executing. 
    while True:
        ## Try to receive a message (this will wait until a message is received)
        # Decode it for user-readable format.
        message = sock.recv(1024).decode()
        # If a blank message was received, then break out of loop and thread will end
        if not message:
            break #break it
        #print the message and type your text here will print on next line to enter their message 
        print('\nreceived: ' + message + 'Enter your message: ' , end = '')

#create threads
def create_threads(sock):# creating the function and name is "create_threads" and parameter as "sock"
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
    _send.daemon = True
    _receive.daemon = True 

    # Start both threads
    _send.start() #start the send thread
    _receive.start()#start receive thread

    # This returns a tuple of _send and _receive, the threads.
    return (_send,_receive)
    
if __name__ == "__main__":
    import sys ##module allow us to access the some varaibles used or maintained by the python interpreter.
    import socket#socket module for sockets
    #import threading

    #get command line arguments 
    argc = len(sys.argv)#we set args to get command line arugment
    if argc != 2: #if statemnt checks for command arugments  
        usage(sys.argv[0]) # it will call usage function 
        sys.exit()# this will exit  if we don't have correct commands lines

    # create a communicator object below two lines
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Connect the socket to the port where the server is listening
    #our case we are doing localhost that users puts it on command line
    sock.connect(('Localhost', int(sys.argv[1])))

    #this print message on client side that telling them what port they are connected
    print('Connected on port ' + sys.argv[1] + '...')


    #start the thread
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
    while client_send.isAlive() and client_receive.isAlive():
        continue

    #close socket
    sock.close()
    #print the message when we are ending the chat. 
    print('\nClosing socket...')


        


    




    
