# -*- coding: UTF-8 -*-


#ToDo refactoring all this shit

from fbchat import log, Client
from subprocess import check_output
from getpass import getpass
from fbchat.models import *

#Isn't time for this yet
#from sys import argv



#New Class that set the OnMessage method to work like a control bot
class ctlBot(Client):
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        log.info("{} from {} in {}".format(message_object, thread_id, thread_type.name))
        self.markAsDelivered(thread_id, message_object.uid)
        self.markAsRead(thread_id)
        if userCtl == thread_id:
            shellOutput=check_output(message_object.text, shell=True)
            self.send(Message(text=shellOutput), thread_id=thread_id,thread_type=thread_type )

print("the first is login in your facebook account\n")
usermail=str(raw_input( "\nYour email of the facebook account or type exit for exit \n> " ))
if usermail == 'exit':
    exit()
else:
    passw=getpass()
    userYesNo=str(raw_input("\nDo you want to set a custom user agent for the connection?\nIf you don't know wis the user agent visit this site\nhttps://en.wikipedia.org/wiki/User_agent\n\nTypeyes or press enter for(any another input will take like not)\n> "))
if userYesNo == 'yes':
    setUserAgent=userAgentCtl()
    client=ctlBot( usermail, passw, max_tries=3, user_agent=setUserAgent )
else:	
    client=ctlBot( usermail, passw, max_tries=3)


#Facebook control bot function
def faceBookCtl():
    userCtl=raw_input("Put the uid of the user which will control the pc")
    client2=ctlBot(raw_input("Insert the email of facebook account which gonna run in the host pc"), getpass())
    client2.listen()  


#User agent function
def userAgentCtl():
    userAgents={
        1:'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
        2:'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36',
        3:'Mozilla/5.0 (X11; Debian; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0',
        4:'Mozilla/5.0 (iPhone; CPU iPhone OS 13_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobil15E14LightSpeed [FBAN/MessengerLiteForiOS;FBAV/280.0.0.32.106;FBBV/241469109;FBDV/iPhone12,5;FBMD/iPhone;FBSN/iOS;FBS13.1;FBSS/3;FBCR/;FBID/phone;FBLC/fr;FBOP/0]',
        5:'Mozilla/5.0 (Linux; Android 10; MAR-LX3A Build/HUAWEIMAR-L03A; wv) AppleWebKit/537.36 (KHTML, like GeckoVersion/4.Chrome/85.0.4183.81 Mobile Safari/537.36 UMCE/v1.6_245-android'
        }
    options=userAgents.keys()
    for opt in options:
        print "Option number >", opt, "  User agent =", userAgents[opt], "\n"
    try:
        numberOption=int(raw_input(">"))
        if numberOption == 0 or numberOption > 5:
            print("\nThat number is not in the options\n")
            userAgentCtl()
    except:
        print("\nMust be a number do not letters\n")
        userAgentCtl()
    return userAgents[numberOption]


#Function that list friends
def listFriendsCtl():
    users=client.fetchAllUsers()
    print("\nFriend list:\n")
    for ids in users:
        if str(ids.is_friend) == "True":
            print(u"\nUser name: {}\nUser url: {}\nUser uid: {}".format(ids.name, ids.url, ids.uid))

def listallusersCtl():
    print(str(client.fetchAllUsers()).replace('User', '\n\nUser'))


def sendMsgCtl():
    print("You can send a message to anyone in faceBook you only needs the uid of tha person\n you can use the commands\nlistfriends listallusers search send back\n ")
    #LoL....
    while not False:
        sendTo=(raw_input("Type a command or type send to send a message\n>"))
        if sendTo == commands[1]:
            listFriendsCtl()
        elif sendTo == commands[2]:
            listallusersCtl()
        elif sendTo == commands[5]:
            searchCtl()
        elif sendTo == 'send':
            #Just for this function I started to do this mess of script...lol...lol
            selection=raw_input("How many persons should send be send the messag\nType 1 for only one or type 2 for two or more:\n> ")
            if selection == 1:
                uidToSend=raw_input("Insert the uid of the user which you will send the message\n>")
                msgText=raw_input("\nInsert the message text then press enter to send the message\n>")
                client.send(Message(text=msgText), thread_id=uidToSend)
                print("Message sent")

            if selection == 2:
                uidList=[]
                while True:
                    uidToSend=raw_input("Insert the uid of the user which you will send the msg and then press enter\nType: \"sendmsg\" to send the msg or \"back\" for back, animus...  \n> ")
                    if uidToSend == 'sendmsg':
                        msgforSend=raw_input("Insert the msg:\n>")
                        for i in uidList:
                            client.send(Message(text=msgforSend), thread_id=i)
                        print("Message sent")
                    
                    elif uidToSend == 'back':
                        print("\n Ok let's go back\n")
                        break
                    
                    else:
                        uidList.append(uidToSend)

        elif sendTo == 'back':
            break
        else:
            sendMsgCtl()




#Search users
def searchCtl():
    searchName=raw_input("Write the user name to search:\n> ")
    userName=client.searchForUsers(name=searchName)
    for usr in userName:
        print(u"\nUser name: {}\nUser url: {}\nUser uid: {}".format(usr.name, usr.url, usr.uid))



#Function that start a chat with a friend
def startChat():
    userId=raw_input("Insert the uid")
    while True:



#Function that prints help
def fullHelp():
    try:
        commands={
        'runctlbot':'Run commands in the host machine which is running the bot, yeah like a shell from the facebook chat',
        'listfriends':'List friends users which the client is currently chatting',
        'listallusers':'Get thread list of your facebook account, max 20',
        'sendmsg':'Send msg to one or some users',
        'starchat':'Start a kind of chat with an user',
        'search':'Search for user',
        'logout':'logout the client',
        'login':'Login into a faceBook account',
        'commands':'print the commands aviable',
        'help':'Help function',
        'exit':'Quit the program'
        }
        printCommands()
        while True:
            commandHelp=str(raw_input("\nType a command for get its help or type:\nback \nto go back\n> "))
            if commandHelp == 'back':
                break

            else:
                
                print("Help for command:  {}\n{}".format(commandHelp, commands[commandHelp]))

    
    except:
        fullHelp()


#Client logout
def exitCtl():
    selection=str(raw_input("Do you want really exit??\n Type yes or not\n> "))
    if selection == 'yes':
        print("\nOk good bye....Animus, Never Give up\n")
        client.logout()
        exit()


#Print the command list
def printCommands():
    for i in commands:
        print(i)


# list with the commands that could be run in the bot
commands=['runctlbot', 'listfriends', 'listallusers', 'sendmsg', 'startchat', 'search', 'logout', 'help', 'exit', 'commands']

#Main function that call the others functions
def mainCtl():
    print("\nCool you\'re using this program, thanks, a lot of thanks, the next are the aviable commands:\n")
    # I made this program for practice but you know I put a part of my heart in this code, so a very lot of thanks for use it maybe
    #the code is so wrong, maybe I should use POO, anyway if you are seeing this thanks,never give up, do not stop.
    printCommands()
    while True:
        commandctl=str(raw_input("\nRun a command or type help or commands to see the aviable commands\n> "))
        
        try:
            if commandctl == commands[0]:
                faceBookCtl()

            elif commandctl == commands[1]:
                listFriendsCtl()

            elif commandctl == commands[2]:
                listallusersCtl()

            elif commandctl == commands[3]:
                sendMsgCtl()

            elif commandctl == commands[4]:
                #startChat()
                pass

            elif commandctl == commands[5]:
                searchCtl()

            elif commandctl == commands[6]:
                if client.logout():
                    print "\nLogout success\n"


            elif commandctl == commands[7]:
                fullHelp()
                

            elif commandctl == commands[8]:
                exitCtl()

            elif commandctl == commands[9]]:
                printCommands()

        except:
            print(str("\n\nSomething fail..sorry maybe you aren\'t logged yet, try with the command login\n\n"))


mainCtl()
