from Tkinter import *
from PIL import Image, ImageTk, ImageDraw
import tkFileDialog
import requests
import httplib, urllib
import json
import cv2
import tkFont
import rfid

root = Tk() #Makes the window
root.wm_title("Microsoft") #Makes the title that will appear in the top left
root.config(background = "#FFFFFF")

dict_of_projs = {'AudioSense':63960, 'Rail Rakshak':63954, 'Connected Car':63903, 'Smart Office Chair':63915,
                 'Pop ur Pills':63990, 'MakeWayForAmbulance':63949, 'Digital Railway Stations':63926,
                 'Strap the Dog':63909, 'Traffic Robot':63859, 'Accident Controller':63922,
                 'WatchOver':63896, 'IWAR (I will always remember)':63898, 'iPark':63890, 
                 'Smart Reminder':63943, 'Navigation Stick':63902}


def vote_button_clicked():
    global dict_of_projs
    log.delete(1.0, END)
    log.insert(0.0, "vote cliked\n")
    headers = {'content-type': 'application/json'}
    data = json.dumps({'id': 0, 'projectid': dict_of_projs[selectedApi], 'cardId': '15'})
    r = requests.post(_url+'vote/', data=data, headers=headers)
    #print r.status_code
    #print r.reason
    log.delete(1.0, END)
    log.insert(0.0, r.content+'\n')
    #global file_path
    #file_path = tkFileDialog.askopenfilename(filetypes=[("Image Files","*.jpg; *.gif; *jpeg; *png")])   # ('All','*')]
    #if file_path:
    #    img = Image.open(file_path)
        
    #    baseheight = 400
        
    #    hpercent = (baseheight/float(img.size[1]))
    #    wsize = int((float(img.size[0])*float(hpercent)))
    #    img = img.resize((wsize,baseheight), Image.ANTIALIAS)
    #    img.save(file_path)
    #    imageEx = ImageTk.PhotoImage(img)
    #    l = Label(photoCanvas, image=imageEx).grid(row=0, column=0, padx=10, pady=2)
    #    l.pack() 
    #    root.update()

def submit_button_clicked():
    global file_path, selectedApi, selectedService, _url, vision_key, face_key
    params = None
    log.insert(0.0, "Submit cliked\n")
    data = None
    with open( file_path, 'rb' ) as f:
        data = f.read()

    if selectedApi == 'vision':
        headers = {
            'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': vision_key,
        }
        if selectedService == 'analyze':
            #_url = 'https://api.projectoxford.ai/vision/v1.0/analyze'
            _url = '/vision/v1.0/analyze?%s'
            params = urllib.urlencode({
                'visualFeatures': 'Categories, Tags, Description, Faces, ImageType, Color, Adult',
            })
        elif selectedService == 'describe':
            _url = '/vision/v1.0/describe?%s'
            params = urllib.urlencode({
                'maxCandidates': '1',
            })
        elif selectedService == 'generate tags':
            _url = '/vision/v1.0/tag?%s'
            params = urllib.urlencode({
            })

        elif selectedService == 'OCR':
            _url = '/vision/v1.0/ocr?%s'
            params = urllib.urlencode({
                'language': 'unk',
                'detectOrientation ': 'true',
            })
        #log.insert(0.0, _url)
    elif selectedApi == 'face':
        headers = {
            'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': face_key,
        }
        if selectedService == 'detection':
            _url = '/face/v1.0/detect?%s'
            params = urllib.urlencode({
                'returnFaceId': 'true',
                'returnFaceLandmarks': 'false',
            })
    elif selectedApi == 'emotion':
        headers = {
            'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': emotion_key,
        }
        if selectedService == 'emotion':
            _url = '/emotion/v1.0/recognize?%s'
            params = urllib.urlencode({
            })
    
    conn = httplib.HTTPSConnection('api.projectoxford.ai')
    conn.request("POST", _url % params, data, headers)
    response = conn.getresponse()
    data = response.read()
    if selectedService == 'detection':
        result = json.loads(data)
        img = Image.open(file_path)
        for i in result:
            y0 = i['faceRectangle']['top']
            y1 = i['faceRectangle']['height']
            x0 = i['faceRectangle']['left']
            x1 = i['faceRectangle']['width']
                
            dr = ImageDraw.Draw(img)
            dr.rectangle(((x0,y0),(x0+x1,y0+y1)), fill=None, outline = "blue")
            
        imageEx = ImageTk.PhotoImage(img)
        l = Label(photoCanvas, image=imageEx).grid(row=0, column=0, padx=2, pady=2)
        l.pack()
        #root.update()
    log.insert(0.0, data+'\n')
    conn.close()


def onSelectApi(evt):
    global e, v
    global selectedApi
    selectedApi = apiList.get(apiList.curselection())
    #print dict_of_projs[selectedApi]

    r = requests.get(_url+'project/'+str(dict_of_projs[selectedApi]))
    log.delete(1.0, END)
    log.insert(0.0, r.content+'\n')

    top = Toplevel(root)

    Label(top, text="Value").pack()

    v=StringVar()
    e = Entry(top, textvariable=v)
    e.pack(padx=5)

    b = Button(top, text="OK", command=ok)
    b.pack(pady=5)

def ok():
    global e, v
    v.set('hello')
    print e.get()
    

_url =  'http://idcmakerfestvotingapi.azurewebsites.net/api/'


#Left Frame and its contents
leftFrame = Frame(root, width=400, height = 600)
leftFrame.grid(row=0, column=0, padx=10, pady=2)

#Label API
Label(leftFrame, text='Projects', width=25, fg="red", font=tkFont.Font(size=15)).grid(row=0, column=0)

#Listbox for API
apiList = Listbox(leftFrame, name='apiList', exportselection=0, height=25, width=30, font=tkFont.Font(size=15))
apiList.grid(row=1,column=0)
apiList.bind('<<ListboxSelect>>', onSelectApi)

for item in dict_of_projs.keys():
    apiList.insert(END, item)


#Right Frame and its contents
rightFrame = Frame(root, width=200, height = 600)
rightFrame.grid(row=0, column=1, padx=10, pady=2)

Label(rightFrame, text='MakerFest Voting').grid(row=0, column=0)

photoCanvas = Canvas(rightFrame, width=1000, height=400, bg='white')
photoCanvas.grid(row=1, column=0, padx=10, pady=2)

btnFrame = Frame(rightFrame, width=200, height = 200)
btnFrame.grid(row=2, column=0, padx=10, pady=2)

log = Text(rightFrame, width = 125, height = 10, takefocus=0)
log.grid(row=3, column=0, padx=10, pady=2)

vote_button = Button(btnFrame, text="Vote", command=vote_button_clicked)
vote_button.grid(row=0, column=0, padx=10, pady=2)

#submit_button = Button(btnFrame, text="Submit", command=submit_button_clicked)
#submit_button.grid(row=0, column=1, padx=10, pady=2)

#capture_button = Button(btnFrame, text="Capture", command=capture_clicked)
#capture_button.grid(row=0, column=2, padx=10, pady=2)


root.mainloop() #start monitoring and updating the GUI
