#Arpan Patel
#Homework 4 Final 5/30/2017

#TO RUN ON WINDOWS 
# run to this program I set it up as local host connections.
# to run as server (py -3 direct_messenger_with_files.py -l 6001)
#to run as client(py -3 direct_messenger_with_files.py 6001 localhost)

#TO RUN ON MAC
# run to this program I set it up as local host connections.
# to run as server (python3 direct_messenger_with_files.py -l 6001)
#to run as client(python3 direct_messenger_with_files.py 6001 localhost)


#usage info
def usage( script_name ):
    print( 'Usage: py ' + script_name + ' ' + '-l' + '(run Server with port number)' + '' + ' <port number>' + "localhost" + ' ' + '(run as localhost with same port number)' )


#get messages
def receive_messages(sock):
   while(True):
       #print("Enter you message: ")
       #sys.stdout.flush()
       message = sock.recv(1024).decode()
       if(message):
           print(message, end='')
       else:
            sock.close()
            break

#listen for server connection 
def listenForConnection(port):
    # create a server objects
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # binds to any available interface
    serversocket.bind(('', int(port)))
    # queue up to 5 requests
    serversocket.listen(5)
    # wait for a connection and accept it
    sock, addr= serversocket.accept()
    
	
    #threading for receive_messages_Thread
    receive_messages_Thread = threading.Thread(target=receive_messages, args=[sock])
    receive_messages_Thread.setDaemon(True)
    receive_messages_Thread.start()
	
    ##listens for conncetions
    serversocket.listen(5)
    # wait for a connection and accept it
    Socket_Listener_For_File, addr= serversocket.accept()
	
	
    #threading for retrieve files from server
    retrieve_File_Thread = threading.Thread(target=retrieve_File_From_Server, args=[Socket_Listener_For_File, serversocket])
    retrieve_File_Thread.setDaemon(True)
    retrieve_File_Thread.start()
	
    #threading for displayMenu 
    display_Menu_Thread = threading.Thread(target=displayMenu, args=(sock, Socket_Listener_For_File, True, serversocket, None, None))
    display_Menu_Thread.setDaemon(True)
    display_Menu_Thread.start()

    #Now  we  just  wait  until  both  threads  are dead.   
    while(receive_messages_Thread.isAlive() and retrieve_File_Thread.isAlive() and display_Menu_Thread.isAlive()):
        pass
		
    #close sockets 
    sock.close()
    Socket_Listener_For_File.close()

#connect to server function 
def connectToServer(port, server):
    #Connects to server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server, int(port)))
	
    #receive message threading 
    receive_messages_Thread = threading.Thread(target=receive_messages, args=[sock])
    receive_messages_Thread.setDaemon(True)
    receive_messages_Thread.start()

    # create a server objects
    Socket_Listener_For_File = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Socket_Listener_For_File.connect((server, int(port)))
	
    #retrieve file threading 
    retrieve_File_Thread = threading.Thread(target=retrieve_File_From_client , args=[Socket_Listener_For_File, port, server])
    retrieve_File_Thread.setDaemon(True)
    retrieve_File_Thread.start()
	
    #display menu threadign 
    display_Menu_Thread = threading.Thread(target=displayMenu, args=(sock, Socket_Listener_For_File, False, None, port, server))
    display_Menu_Thread.setDaemon(True)
    display_Menu_Thread.start()

    #Now  we  just  wait  until  both  threads  are dead.
    while(receive_messages_Thread.isAlive() and retrieve_File_Thread.isAlive() and display_Menu_Thread.isAlive()):
        pass

    #close sockets
    sock.close()
    Socket_Listener_For_File.close()

#file copying function
def File_Copy(sock, Name_of_File):
    file_size = sock.recv(1024)
    file_open = open(Name_of_File, 'wb')
    while(file_size):
        print("copying a file")
        file_open.write(file_size)
        file_size = sock.recv(1024)
    print("File has been successfully been copied into the folder.")
    file_open.close()

	
#display menu for users
def displayMenu(sock, Socket_Listener_For_File, act_as_server, serversocket, port, server):
    #use while true for options 
      while True:
        #print option
        print("Enter an option ('m', 'f', 'x'):")
        print( '(m)essage (send)' )
        print( '(f)ile (request )' )
        print( 'e(X)it' )
		
	#user option 
        getoption = sys.stdin.readline()[:-1]

	#check which option user have choosen
        if getoption == 'f' or getoption == "F":
            print("Can you please enter the name of the file you are trying to get it: ")
            Name_of_File = sys.stdin.readline()[:-1]
            Socket_Listener_For_File.send(Name_of_File.encode())
			
	    #act as server
            if act_as_server:
                serversocket.listen(5)
                sock, addr= serversocket.accept()
	    # connect server and port 
            else:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((server, int(port)))
            #file copy 
            File_Copy(sock, Name_of_File)

        # if they select 'm' then send message 
        elif getoption == 'm' or getoption == "M":
            message = sys.stdin.readline()
            sock.send(message.encode())
	# if they select 'x' then exit and pring message other side close
        elif getoption == 'x' or getoption == "X":
            sock.send(''.encode())
            Socket_Listener_For_File.send(''.encode())
            print( '\n[other side shutdown; closing socket...]' )        
            sock.close()
            Socket_Listener_For_File.close()
            os._exit(0)
			
#get file from server 
def retrieve_File_From_Server(Socket_Listener_For_File, serversocket):
    while True:
        try:
            #decode it
            Name_of_File = Socket_Listener_For_File.recv(1024).decode()
            if not Name_of_File:
                Socket_Listener_For_File.close()
                serversocket.close()
                break
            #listen
            serversocket.listen(5)
            sock, addr= serversocket.accept()
            try:
                print ("receiving the file "+ Name_of_File)
                file_open = open(Name_of_File, 'rb')
                read_file = file_open.read()
                sock.sendall(read_file)
                file_open.close()
                print("File has been successfully transferred in your folder.")
                sock.shutdown(socket.SHUT_WR)
                sock.close()
            except FileNotFoundError:
                print("File does not exist in this folder or is empty?" )
                sock.shutdown(socket.SHUT_WR)
                sock.close()
        except:
            break
#file retrieve
def retrieve_File_From_client (Socket_Listener_For_File, port, server):
    while True:
        try:
            Name_of_File = Socket_Listener_For_File.recv(1024).decode()
            if not Name_of_File:
                Socket_Listener_For_File.close()
                server.close()
                break
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((server, int(port)))
            try:
               print ("receiving the file "+ Name_of_File)
               file_open = open(Name_of_File, 'rb')
               read_file = file_open.read()
               sock.sendall(read_file)
               file_open.close()
               print("File has been successfully transferred in your folder.")
               sock.shutdown(socket.SHUT_WR)
               sock.close()
            except FileNotFoundError:
                print("File does not exist in this folder or is empty?" )
                sock.shutdown(socket.SHUT_WR)
                sock.close()
        except:
            break
if __name__ == "__main__":
    #all imports
    import getopt , sys ,threading, socket
    argc = len(sys.argv)
    if argc < 2 or argc > 3: 
        usage(sys.argv[0]) 
        sys.exit()
    #gets command line arguments
    options, args = getopt.getopt(sys.argv[1:], "-l:")
    #run as server using the command line with this option '-l'
    if len(options) == 1:
        listenForConnection(options[0][1])
    #runs connectToServer if there is no '-l' and make sure to type the "port" + "localhost"
    else:
        connectToServer(args[0], args[1])
		
		
	
