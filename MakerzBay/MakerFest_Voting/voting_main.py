from Tkinter import *
import rfid
import thread
import json
import requests

master = Tk()
master.wm_title('MAkerFest voting')

i=1
dict_of_projs = {'AudioSense':63960, 'Rail Rakshak':63954, 'Connected Car':63903, 'Smart Office Chair':63915,
                 'Pop ur Pills':63990, 'MakeWayForAmbulance':63949, 'Digital Railway Stations':63926,
                 'Strap the Dog':63909, 'Traffic Robot':63859, 'Accident Controller':63922,
                 'WatchOver':63896, 'IWAR (I will always remember)':63898, 'iPark':63890, 
                 'Smart Reminder':63943, 'Navigation Stick':63902}


for item in dict_of_projs.keys():
    if i<=10:
        Label(master, text=item).grid(row=i, column=1, padx=50, sticky=W)
    else:
        Label(master, text=item, bd=2, anchor=E).grid(row=(i-10), column=4, padx=50, sticky=N+S+W)
    i = i+1


for i in range(1,16):
    if i<=10:
        Button(master, text="VOTE", font=('Helvetica', 16), command=lambda x=i: vote_clicked(x)).grid(row=i, column=2)
    else:
        Button(master, text="VOTE", font=('Helvetica', 16), command=lambda x=i: vote_clicked(x)).grid(row=i-10, column=5)

    


def vote_clicked(i):
    global selectedProj
    global top
    global device
    global selectedProjName
    print dict_of_projs.keys()[i-1]
    selectedProjName = dict_of_projs.keys()[i-1]
    selectedProj = dict_of_projs[dict_of_projs.keys()[i-1]]
    
    top = Toplevel(master)
    Label(top, text="Please scan your Badge", font=('Helvetica', 50)).pack()
    #b = Button(top, text="OK", command=ok)
    #b.pack()
    top.grab_set()
    top.attributes('-topmost', True)
    
    #getData()
    thread.start_new_thread(getData, ())
    

def ok():
    global top
    top.destroy()
    top.grab_release()
    #print 'ok'

def ok2():
    global returned
    returned.destroy()

def getData():
    try:
        message = 'Default90abchlrtwy'
        global cardId
        global returned
        global selectedProjName
        cardId = rfid.get_input(device)
        print cardId
        ok()
        headers = {'content-type':'application/json'}
        data = json.dumps({'id':0, 'projectid': selectedProj, 'cardId':cardId})
        r = requests.post(_url+'/vote/', data=data, headers=headers)
        print r.content
        print r.reason
        print r.status_code

        returned = Toplevel(master)
        if r.status_code == 409:
            message = 'You have already voted'
        elif r.status_code == 201:
            message = 'Voted successfully to '+str(selectedProjName)
        elif r.status_code == 500:
            message = 'Please Retry'
        Label(returned, text=message, font=('Helvetica', 25)).pack()
        b2 = Button(returned, text="OK", font=('Helvetica', 50), command=ok2)
        b2.pack()
    except e:
        print e


global top, returned
global device
global cardId
device = rfid.initialize_from_voting()
global selectedProj
global selectedProjName

_url = 'http://idcmakerfestvotingapi.azurewebsites.net/api/'
mainloop( )
