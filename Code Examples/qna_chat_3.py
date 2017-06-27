#! python

# Q & A Ver. 3
# TODO:
# MAINTAIN A DICTIONARY OF QUESTIONS AND THEIR NUMBERS
# WHEN THE ANSWER ARRIVES, REMOVE IT FROM THE DICTIONARY
# DISPLAY THE QUESTION AND ANSWER AS A SET
# "Q: What is your favorite color?"
#	"A: blue"

# To ask a question:
#	simply type in the question
# To answer a question:
#	type ':', then the question number, then ':' again, then the answer
# Example:
# 	Question:
# 	What is your favorite color?
#	This will appear on the receiver's end as:
#	Question 2. What is your favorite color?
#	Answer:
#	:2:blue
#	This answer will appear on the other end as:
# "Q: What is your favorite color?"
#	"A: blue"

def ask( sock ):
	global next_question, my_questions
	message= sys.stdin.readline().rstrip()
	if not message:
		return None
	question= 'q:' + str(next_question) + ':' + message
	try:
		print( '(sending question: )' + question )
		sock.send( question.encode() )
	except: # in case the socket is closed
		return None
	my_questions[next_question]= message
	print( "my_questions: " + str(my_questions) )
	next_question+=1
	return 1
	
def answer( sock ):
	global their_questions
	print( 'Questions directed to you:' )
	print( their_questions )
	print( "Enter the number of the question you wish to answer:" )
	question_number= sys.stdin.readline().rstrip()
	if not question_number:
		return None
	question= their_questions[question_number]
	if not question:
		return None
	print( 'Enter your answer:' )
	answer= sys.stdin.readline().rstrip()
	if not answer:
		return None
	message= 'a:' + question_number + ':' + answer
	try:
		sock.send( message.encode() )
	except: # in case the socket is closed
		return None
	their_questions.pop( question_number )
	return 1
	
def displayMenu():
	print( "Enter an option ('q', 'a', 'x'):" )
	print( 'ask a (Q)uestion' )
	print( '(A)nswer a question' )
	print( 'e(X)it' )
	
def getOption():
	response= sys.stdin.readline()
	if not response:
		return None
	return response[0]

def connectToServer( port, server ):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	if server:
		sock.connect((server, int(port)))
	else:
		sock.connect(('localhost', int(port)))
	return sock
	
def listenForConnection( port ):
	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	serversocket.bind(('', int(port)))
	serversocket.listen(5)
	sock, addr= serversocket.accept()
	return sock
		
def oops( server ):
    print( 'Oops! you specified both the listening flag (-1) and a server address (' + server + '), which is used only for a client. Please remove one of them.' )

def usage( script_name ):
    print( 'Usage: py ' + script_name + ' [-l]' + ' <port number>' + ' [<server address>]' )

if __name__ == "__main__":
	# get the command line arguments
	import sys
	import socket
	argc= len( sys.argv )
	if argc < 2 or argc > 4 :
		usage( sys.argv[0] )
		sys.exit()
	# get the command line arguments
	import getopt
	optlist, non_option_args= getopt.getopt( sys.argv[1:], 'l' )
	act_as_server= False
	# check if listening flag is present
	for opt, arg in optlist:
		if opt == '-l':
			act_as_server= True
	# get other args
	host_args_len= len(non_option_args)
	port= non_option_args[0]
	server= None
	# store server address, if present
	if host_args_len == 2:
		server= non_option_args[1]
	if act_as_server == True and server:
		oops( server );
		sys.exit()	
	if act_as_server == True:
		print( 'listening on port ' + port )
	elif server == None:
		print( 'connecting to localhost on port ' + port )
	else:
		print( 'connecting to ' + server + ' on port ' + port )
	# create the socket
	if act_as_server:
		sock= listenForConnection( port )
	else:
		sock= connectToServer( port, server )
	# create global dictionaries of pending questions
	my_questions= {}
	their_questions= {}
	# start thread to receive messages
	from qna_recv_3 import RecvMessages
	RecvMessages( sock, my_questions, their_questions ).start()
	next_question= 1
	# loop to send messages
	while True:
		displayMenu()
		option= getOption()
		if not option:
			break
		if option == 'q': #ask a question
			if not ask( sock ):
				break
		elif option == 'a': #answer a question
			if not answer( sock ):
				break
		elif option == 'x': #exit
			break
		else: #invalid choice
			pass
	try:
		sock.shutdown( socket.SHUT_WR )
		sock.close()
	except:
		pass
