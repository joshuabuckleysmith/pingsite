import os
import subprocess
import threading
import sys
import re
import signal
from IPy import IP
from subprocess import Popen, PIPE, check_output
import tkinter as tk
from time import sleep

test = 1
T=threading.Thread
STOREOK = False
process = 0
root = tk.Tk()
pingcomponents = {}
pingcomponents["store"]=1
pingcomponents["test"]="primary"
pingcomponents["pingnumber"]="1"
pingcomponents["prefix"]="IP Address"
store = tk.StringVar()
prefix = tk.StringVar()
options = {"Router(dg)":"dg", "Switch US(ussw010)":"ussw010", "Switch Canada(casw010)":"casw010", "Workstation(mws)":"mws", "IP Address":""}    
prefix.set("IP Address")
test = tk.StringVar()
pingnumber = tk.IntVar()

def startasthread(funct):
    thread = T(target = funct)
    thread.start()

def tkbuttons(): 
    global pingcomponents
    def kill():
        killthread(cancelping, ping)
    def sp():
        pingcomponents["store"]=store.get()
        pingcomponents["test"]=test.get()
        pingcomponents["pingnumber"]=pingnumber.get()
        pingcomponents["prefix"]=options[prefix.get()]
        startasthread(startping(store.get(), test.get(), pingnumber.get(), ping, cancelping, prefix.get(), options, storetxt))
    
    '''creates tk window'''
    testbutton = tk.Checkbutton(text="Set MTU to 4000 (default 1345)", variable=test, onvalue="secondary", offvalue="primary",)
    testbutton.deselect()
    testbutton.grid(row=2, column=2)
    pingtxt = tk.Label(text="Ping Number") #Ping test labels for text boxes.
    pingtxt.grid(row=0, column=2)
    storetxt = tk.Label(text="Store Number") #Ping test labels for text boxes.
    storetxt.grid(row=0, column=1)
    pingentry = tk.Entry(text="Number of Pings", textvariable = pingnumber)
    pingentry.grid(row=1, column=2)
    storeentry = tk.Entry(text="Store Number", textvariable = store)
    storeentry.grid(row=1, column=1)
    
    dropdown = tk.OptionMenu(root, prefix, *options)
    dropdown.grid(row=1, column=0)
    #Ping command, sends store, test, pingnumber, ping, cancelping, prefix options and storetxt)
    ping = tk.Button(text="Start Ping", command = sp)
    ping.grid(row=1, column=3)
    #cancelping = tk.Button(text="Cancel Ping", command=lambda:killthread(cancelping, ping))
    cancelping = tk.Button(text="Cancel Ping", command=kill)
    cancelping['state'] = 'disabled'
    cancelping.grid(row=1, column=4)
    exit = tk.Button(text="exit", fg="red", command=root.destroy)
    exit.grid(row=2, column=1)
    def updatetext(button1, button2):
        while True:
            sleep(0.05)
            #print('checking text button')
            if button1.get() == "IP Address":
                button2['text']="IP Address"
            if button1.get() != "IP Address":
                button2['text']="Store Number"   
    textdaemon = T(target = updatetext, args = [prefix, storetxt])
    textdaemon.setDaemon(True)
    textdaemon.start()
    root.bind('<Return>', sp)
    root.title("Starbucks Ping")
            
#def onclick(event=None):
#    startasthread(lambda:startping(store.get(), test.get(), pingnumber.get(), ping, cancelping, target.get(), options, storetxt))
    
def killthread(buttondis, buttonen):
    buttondis['state'] = 'disabled'
    buttonen['state'] = 'normal'
    global pingcomponents
    process = pingcomponents["process"]
    store = pingcomponents["store"]
    try:
        storeip = IP(store)
    except:
        storeip=store
    if storeip != store:
        store = store.zfill(5)
    else:
        store = storeip
    #print("store is {}".format(store))
    buttondis['state'] = 'disabled'
    buttonen['state'] = 'normal'
    #print("pid is {} ".format(process))
    os.system("TASKKILL /F /PID {} /T > nul".format(process))
    try:
        openfile = open("temp{}.txt".format(store), 'r')
        pingprint(openfile)
        openstring = str(openfile.read())
        print(outputstring)
        #print(outputstring.splitlines()[len3-5])
        #print(outputstring.splitlines()[len3-4])
        #print(outputstring.splitlines()[len3-3])
        #print(outputstring.splitlines()[len3-2])
        openfile.close()
        os.system("del temp{}.txt".format(store))
        print("ping Cancelled")
    except:
        print("temp deletion failed")
        print("\nPing ended, start a new ping when ready\n\n")



def startping(store, test, pingnumber, buttondis, buttonen, prefix, options, storetxt):
    global pingcomponents
    pingsize = 0
    store = pingcomponents["store"]
    pingnumber = pingcomponents["pingnumber"]
    prefix = pingcomponents["prefix"]
    print("store {}".format(store))
    print("test {}".format(test))
    print("pingno {}".format(pingnumber))
    print("pingsize {}".format(pingsize))
    print("options {}".format(options))
    print("prefix passed is {}".format(prefix))
    if test == "primary":
        pingsize = "1345"
    else:
        pingsize = "4000"
    if testpingnumber(pingnumber) == True:
        print("pingnumber tested true")
        if prefix != "IP Address":
            print("prefix did not equal IP Address")
            store = (str(store).zfill(5))
            print('Pinging {}{} with {} bytes {} times.'.format(prefix, store, pingsize, pingnumber))
        if prefix == "":
            print("prefix equals nothing")
            try:
                IP(store)
                print(IP(store))
                print('Pinging ip address {} with {} bytes {} times.'.format(IP(store), pingsize, pingnumber))
            except:
                raise
        buttonen['state'] = 'normal'
        buttondis['state'] = 'disabled'
        pingthread = T(target = pinger, args = [store, pingnumber, test, buttondis, buttonen, prefix])
        pingthread.start()
    else:
        print('Number of pings was not a number.')
    


def testpingnumber(pingnumber):
    if pingnumber == "":
        #print('ping setup 333')
        return False
    try:
        int(pingnumber)
        #print('ping setup 11')
        return True
    except:
        #print('ping setup 12')
        return False 

def pinger(store, pingnumber, primsec, buttondis, buttonen, prefix):
    #print(prefix)
    '''Takes a store number, index as INT, primsec as STRING sets primary or secondary test'''
    global pingcomponents
    print("\n")
    if primsec == "primary":
        print("ping -n {} -l 1345 {}{} > temp{}.txt".format(pingnumber, prefix, store, store))
        pingthread = Popen("ping -n {} -l 1345 {}{} > temp{}.txt".format(pingnumber, prefix, store, store), shell=True)
    if primsec == "secondary":
        print("ping -n {} -l 4000 {}{} > temp{}.txt".format(pingnumber, prefix, store, store))
        pingthread = Popen("ping -n {} -l 4000 {}{} > temp{}.txt".format(pingnumber, prefix, store, store), shell=True)
    pingcomponents["process"] = pingthread.pid  
    print(pingcomponents["process"])
    outputthread = T(target = printoutput, args = [pingthread, store, prefix])
    outputthread.start()
    while True:
        threadalive = bool(pingthread.poll())
        threadalive2 = bool(outputthread.is_alive())
        sleep(0.05)
        #print("pingthread is {}".format(threadalive))
        #print("outputthread is {}".format(threadalive2))
        if threadalive2 == False:
            #print("pid is {} ".format(pingthread.pid))
            #print(pingthread.poll())
            #os.system("TASKKILL /F /PID {} /T > nul".format(pingthread.pid))
            #print('waiting timeout')
            if threadalive == False:
                
                sleep(0.05)
                print("\nPing Complete. Start a new ping with the GUI.")
                buttondis['state'] = 'normal' #reenables buttons when ping completes.
                buttonen['state'] = 'disabled'
                os.system("del temp{}.txt".format(store))
                break


def printoutput(monitoredthread, store, prefix):
    
    outputstring = ""
    pingcount = 0
    sleep(1)
    while True:
        sleep(0.05)
        openfile = open("temp{}.txt".format(store), 'r')
        openstring = str(openfile.read())
        if openstring == "Ping request could not find host {}{}. Please check the name and try again.\n".format(prefix, store):
            print("Ping request could not find host {}{}. Is your prefix correct? Please start ping again when ready.\n".format(prefix, store))
            openfile.close()
            break
        len1 = len(openstring)
        len2 = len(outputstring)
        #print("len 1 is {}".format(len1))
        #print("len 2 is {}".format(len2))
        if len1 > len2:
            outputstring = openstring
            len3 = (len(outputstring.split('\n')))
            #if pingcount > 0:
                #print("{} pings sent".format(pingcount))
            outsplit = outputstring.splitlines()[len3-2]
            if outsplit[0] != " ":
                print("{} {}".format((pingcount+1), outputstring.splitlines()[len3-2]))
            if outsplit[0] == " ":
                print("{} {}".format((pingcount+1), outputstring.splitlines()[len3-7]))
                #print("{} pings sent".format(pingcount+1))
            #print(outputstring)
            pingcount = pingcount + 1
        #print("moni thread{}".format(monitoredthread.poll()))
        th1 = monitoredthread.poll()
        #print("TH1 {}".format(th1))
        if th1 != None:
            #print("monitoredthread.poll() was {}".format(monitoredthread.poll()))
            #print("lines = {}".format(len(outputstring.split('\n'))))
            try:
                print("\n")
                print(outputstring.splitlines()[len3-5])
                print(outputstring.splitlines()[len3-4])
                print(outputstring.splitlines()[len3-3])
                print(outputstring.splitlines()[len3-2])
            except:
                print("nothing to print")
            openfile.close()
            #print("output file closed")
            sleep(0.05)
            break

def pingprint(file):
    openstring = str(openfile.read())
    try:
        ipadd = re.compile('(?<=Ping statistics for )[0-9]+.[0-9]+.[0-9]+.[0-9]+')
        ipadd = ((ipadd.search(openstring).group(0)))
    except:
        ipadd = "none"
        print('ipadd not found')
    try:
        sent = re.compile('(?<=Sent = )[0-9]')
        sent = ((sent.search(openstring).group(0)))
    except:
        sent = 0    
    try:
        received = re.compile('(?<=Received = )[0-9]')
        received = ((received.search(openstring).group(0)))
    except:
        received = 0    
    try:
        lost = re.compile('(?<=Lost = )[0-9]')
        lost = ((lost.search(openstring).group(0)))
    except:
        lost = 0
    try:
        minimum = re.compile('(?<=Minimum = )[0-9]*')
        minimum = ((minimum.search(openstring).group(0)))
    except:
        minimum = 0
    try:
        maximum = re.compile('(?<=Maximum = )[0-9]*')
        maximum = ((maximum.search(openstring).group(0)))
    except:
        maximum = 0
    try:
        average = re.compile('(?<=Average = )[0-9]*')
        average = ((average.search(openstring).group(0)))
    except:
        average = 0
    sent_total += int(sent)
    received_total += int(received)
    lost_total += int(lost)
    if maximum_total < int(maximum):
        maximum_total = int(maximum)
    if minimum_total > int(minimum):
        minimum_total = int(minimum)
        average_total += int(average)
    loss_total = int(round(lost_total/sent_total*100))
    average_total = int(round(average_total/sent_total, 0))
    percentage_lost = (lost_total/sent_total*100)
    print('\nPing Statistics: \n')
    print('Ping statistics for {}:\nPackets: Sent = {}, Received = {}, Lost = {} ({}% loss),\nApproximate round trip times in milli-seconds:\nMinimum = {}ms, Maximum = {}ms, Average = {}ms'.format(ipadd, sent_total, received_total, lost_total, loss_total, minimum_total, maximum_total, average_total))

def main():
    tkbuttons()
    root.mainloop()


