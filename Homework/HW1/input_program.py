#Arpan Patel#
#csc376#
#Programming Exercise 1 #

# this program that properly handles two types of input command line and standard input.

import sys ## module allow us to access the some varaibles used or maintained by the python interpreter.
# In this program I used sys.argv is the list of command line arugments passed to a python script. 

#code below is going to read string from standard input and output.  it will print it
print("Standard Input:") # this will just print line as "Standard Input" 
text = sys.stdin.readline() # leaves the newline char at the end  and this will get me some standard input as user enter. 
while text:# this will keep executing the code until we get no text from the user.  
        print(text, end= '') # this line will print text user enteres (another words)it will be strings that they enter. 
        text=sys.stdin.readline()#leaves the newline char at the end  and this will get me some standard input.
        # this will keep reading the line until we get no text from the user.
           
print("Command line arguments:")# this will just print line as "Command line arguments"
# this list all the command line arugments users have enteres. 
argc= len( sys.argv ) # argv has all the string typed on command line and it returns strings. We will find out len(sys.argv)
argList = sys.argv # this arglist of where my arugments(strings) are stored. 

#below are three options which are initialzed varaible as default value. (for this case it is empty string)
option1 = "" #initialize as default value
option2 = "" #initialize as default value
option3 = "" ##initialize as default value

for arg in range(1,argc): # this for loop will thorugh all the arg in sys.argv.  
        opt = argList[arg] #this create list of arglist[arg] to stored the words(string). 

        if opt == '-o': # if -o present in command line 
                option1=("option 1: "+argList[arg+1]+"\n")#this will assgined to as option 1
                #it will stored whatever the string(in our case it is a word) user enteres after the -o. 
        elif opt == '-t':  #if -t present in command line 
                option2=("option 2: "+argList[arg+1]+"\n")##this will assgined to as option 2
                #it will stored whatever the string(in our case it is a word) user enteres after the -t. 
        elif opt == '-h': # if -h present in command line 
                option3=("option 3") # this will assgined to as option 3
                #it will stored only the "option 3" "-h" arugment because there is no data following option -h for our program. 

print(option1+option2+option3) #this print statement will print whatever the users have entered on command line(arugments) 
#options will print in numeric order.  


















