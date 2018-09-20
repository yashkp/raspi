from Tkinter import *
from PIL import Image, ImageTk, ImageDraw
import tkFileDialog
#import requests
import httplib, urllib
import json
import cv2

root = Tk() #Makes the window
root.wm_title("Microsoft") #Makes the title that will appear in the top left
root.config(background = "#FFFFFF")

def load_button_clicked():
    log.insert(0.0, "Load cliked\n")
    global file_path
    file_path = tkFileDialog.askopenfilename(filetypes=[("Image Files","*.jpg; *.gif; *jpeg; *png")])   # ('All','*')]
    if file_path:
        img = Image.open(file_path)
        
        baseheight = 400
        
        hpercent = (baseheight/float(img.size[1]))
        wsize = int((float(img.size[0])*float(hpercent)))
        img = img.resize((wsize,baseheight), Image.ANTIALIAS)
        img.save(file_path)
        imageEx = ImageTk.PhotoImage(img)
        l = Label(photoCanvas, image=imageEx).grid(row=0, column=0, padx=10, pady=2)
        l.pack() 
        root.update()

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

    #you can edit this for different types of visualFeatures
    #params = { 'visualFeatures' : 'Color,Categories,ImageType,Faces,Adult,Tags,Description'}
    #headers = dict()
    #headers['Ocp-Apim-Subscription-Key'] = _key
    #headers['Content-Type'] = 'application/octet-stream'
    #response = requests.request( 'post', _url, json = None, data = data, headers = headers, params = params )

    

    
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

    #log.insert(0.0, response.status_code)
    #if response.status_code == 200:
    #    log.insert(0.0, "Received\n")
    #    log.insert(0.0, response.content)

def capture_clicked():
    global file_path
    log.insert(0.0, "Capture cliked\n")
    cam = cv2.VideoCapture(0)
    
    ret, img = cam.read()
    cv2.imwrite('test.jpg',img)
    img = Image.open('test.jpg')
    file_path = 'test.jpg'
        
    baseheight = 400
    hpercent = (baseheight/float(img.size[1]))
    wsize = int((float(img.size[0])*float(hpercent)))
    img = img.resize((wsize,baseheight), Image.ANTIALIAS)
    img.save('test.jpg')
    imageEx = ImageTk.PhotoImage(img)
    l = Label(photoCanvas, image=imageEx).grid(row=0, column=0, padx=10, pady=2)
    l.pack() 
    root.update()
        
    cam.release()

def onSelectApi(evt):
    global selectedApi
    selectedApi = apiList.get(apiList.curselection())
    serviceList.delete(0, END)
    if selectedApi == 'vision':
        for item in ['analyze', 'describe', 'generate tags', 'OCR']:
            serviceList.insert(END, item)
    elif selectedApi == 'face':
        for item in ['detection', 'similar', 'grouping', 'identification', 'verification']:
            serviceList.insert(END, item)
    elif selectedApi == 'emotion':
        for item in ['emotion']:
            serviceList.insert(END, item)
    serviceList.select_set(0)
    serviceList.event_generate("<<ListboxSelect>>")
    #selectedService = serviceList.get(serviceList.curselection())

def onSelectService(evt):
    global selectedService
    selectedService = serviceList.get(serviceList.curselection())
    print selectedService

vision_key = '43d9aa7711bd4a69a3bacf9c248f3f74'
face_key = 'edbd2401b2414ad48f5e39bbdad34fa9'
emotion_key = '0cb6ccb48a364ffc869d024f82a47851'
_url = None

selectedApi = 'vision'
selectedService = None

#Left Frame and its contents
leftFrame = Frame(root, width=400, height = 600)
leftFrame.grid(row=0, column=0, padx=10, pady=2)

#Label API
Label(leftFrame, text='API', width=25).grid(row=0, column=0)

#Listbox for API
apiList = Listbox(leftFrame, name='apiList', exportselection=0)
apiList.grid(row=1,column=0)
apiList.bind('<<ListboxSelect>>', onSelectApi)

for item in ['vision', 'face', 'emotion']:
    apiList.insert(END, item)

#Label Services
Label(leftFrame, text='Services', width=25).grid(row=2, column=0)

#Services of a API
serviceList = Listbox(leftFrame, name='serviceList', exportselection=0)
serviceList.grid(row=3,column=0)
serviceList.bind('<<ListboxSelect>>', onSelectService)

#for item in ['analyze', 'describe', 'generate tags', 'OCR', 'thumbnail']:
#    serviceList.insert(END, item)


#apiList.select_set(0)
#apiList.event_generate("<<ListboxSelect>>")

#serviceList.select_set(0)
#serviceList.event_generate("<<ListboxSelect>>")

#Right Frame and its contents
rightFrame = Frame(root, width=200, height = 600)
rightFrame.grid(row=0, column=1, padx=10, pady=2)

Label(rightFrame, text='Microsoft Cognitive Services').grid(row=0, column=0)

photoCanvas = Canvas(rightFrame, width=1000, height=400, bg='white')
photoCanvas.grid(row=1, column=0, padx=10, pady=2)

file_path = None

btnFrame = Frame(rightFrame, width=200, height = 200)
btnFrame.grid(row=2, column=0, padx=10, pady=2)

log = Text(rightFrame, width = 125, height = 10, takefocus=0)
log.grid(row=3, column=0, padx=10, pady=2)

load_button = Button(btnFrame, text="Load", command=load_button_clicked)
load_button.grid(row=0, column=0, padx=10, pady=2)

submit_button = Button(btnFrame, text="Submit", command=submit_button_clicked)
submit_button.grid(row=0, column=1, padx=10, pady=2)

capture_button = Button(btnFrame, text="Capture", command=capture_clicked)
capture_button.grid(row=0, column=2, padx=10, pady=2)


root.mainloop() #start monitoring and updating the GUI