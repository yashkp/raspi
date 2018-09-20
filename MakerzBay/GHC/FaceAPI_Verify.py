from Tkinter import *
from PIL import Image, ImageTk, ImageDraw
import tkFileDialog
import httplib, urllib
import cv2
import json
import requests

root = Tk() #Makes the window
root.wm_title("Window Title") #Makes the title that will appear in the top left
root.config(background = "#FFFFFF")
#imageEx = None
#imageEx2= None
def capture1_clicked():
    log.insert(0.0, "Capture1 cliked\n")

    cam = cv2.VideoCapture(0)
    ret, img = cam.read()
    cv2.imwrite('pic1.jpg',img)
    img = Image.open('pic1.jpg')
    cam.release()
        
    baseheight = 300
    hpercent = (baseheight/float(img.size[1]))
    wsize = int((float(img.size[0])*float(hpercent)))
    img = img.resize((wsize,baseheight), Image.ANTIALIAS)
    img.save('pic1.jpg')
    imageEx = ImageTk.PhotoImage(img)
    l = Label(photoCanvas1, image=imageEx)
    l.image = imageEx
    l.grid(row=0, column=0, padx=10, pady=2).pack()
    #l.pack() 
    root.update()
        
    

def capture2_clicked():
    log.insert(0.0, "Capture2 cliked\n")

    cam = cv2.VideoCapture(0)
    ret, img = cam.read()
    cv2.imwrite('pic2.jpg',img)
    img = Image.open('pic2.jpg')
    cam.release()
        
    baseheight = 300
    hpercent = (baseheight/float(img.size[1]))
    wsize = int((float(img.size[0])*float(hpercent)))
    img = img.resize((wsize,baseheight), Image.ANTIALIAS)
    img.save('pic2.jpg')
    imageEx = ImageTk.PhotoImage(img)
    l = Label(photoCanvas2, image=imageEx)
    l.image = imageEx
    l.grid(row=0, column=0, padx=10, pady=2).pack()
    #l.pack() 
    root.update()
        
    

faceId1 = None
faceId2 = None

def getFaceId(filename):
    global faceId1, faceId2
    data = None
    faceId = None
    with open( filename, 'rb' ) as f:
        data = f.read()

    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': face_key,
    }
    _url = '/face/v1.0/detect?%s'
    params = urllib.urlencode({
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
    })
    
    conn = httplib.HTTPSConnection('api.projectoxford.ai')
    conn.request("POST", _url % params, data, headers)
    response = conn.getresponse()
    data = response.read()
    result = json.loads(data)

    conn.close()

    img = Image.open(filename)
    for i in result:
        faceId = i['faceId']

        y0 = i['faceRectangle']['top']
        y1 = i['faceRectangle']['height']
        x0 = i['faceRectangle']['left']
        x1 = i['faceRectangle']['width']
                
        dr = ImageDraw.Draw(img)
        dr.rectangle(((x0,y0),(x0+x1,y0+y1)), fill=None, outline = "blue")
            
        imageEx = ImageTk.PhotoImage(img)
        if filename == 'pic1.jpg':
            faceId1 = faceId
            #l = Label(photoCanvas1, image=imageEx)
            #l.image = imageEx
            #l.grid(row=0, column=0, padx=10, pady=2).pack()
            #root.update()
        elif filename == 'pic2.jpg':
            faceId2 = faceId
            #l = Label(photoCanvas2, image=imageEx)
            #l.image = imageEx
            #l.grid(row=0, column=0, padx=10, pady=2).pack()
            #root.update()
    
def submit_button_clicked():
    getFaceId('pic1.jpg')
    getFaceId('pic2.jpg')

    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': face_key,
    }
    _url = '/face/v1.0/verify?%s'
    body = ({
        'faceId1': faceId1,
        'faceId2': faceId2
    })
    
    params = urllib.urlencode({

    })

    try:
        r = requests.post("https://api.projectoxford.ai/face/v1.0/verify", json=body,headers=headers)
        #print(r.json())
        log.insert(0.0, r.json())
        log.insert(0.0, '\n')
    except Exception as e:
        pass

def onSelectApi(evt):
    w = evt.widget
    api = w.get(w.curselection())
    print api
    serviceList.delete(0, END)
    if api == 'vision':
        for item in ['analyze', 'describe', 'generate tags', 'OCR', 'thumbnail']:
            serviceList.insert(END, item)
    elif api == 'face':
        for item in ['detection', 'similar', 'grouping', 'identification', 'verification']:
            serviceList.insert(END, item)
    elif api == 'emotion':
        for item in ['stream', 'url', 'video']:
            serviceList.insert(END, item)
    elif api == 'video':
        for item in ['Video Stabilization', 'Motion Detection', 'Face Tracking', 'Video Thumbnail']:
            serviceList.insert(END, item)
    elif api == 'optionApi':
        for item in ['option1', 'option2', 'option3']:
            serviceList.insert(END, item)
    #print w.curselection()

face_key = 'edbd2401b2414ad48f5e39bbdad34fa9'

#Left Frame and its contents
leftFrame = Frame(root, width=400, height = 600)
leftFrame.grid(row=0, column=0, padx=10, pady=2)

#Label API
Label(leftFrame, text='API', width=25).grid(row=0, column=0)

#Listbox for API
apiList = Listbox(leftFrame, name='apiList')
apiList.grid(row=1,column=0)
apiList.bind('<<ListboxSelect>>', onSelectApi)

for item in ['vision', 'face', 'emotion', 'video', 'optionApi']:
    apiList.insert(END, item)

#Label Services
Label(leftFrame, text='Services', width=25).grid(row=2, column=0)

#Services of a API
serviceList = Listbox(leftFrame)
serviceList.grid(row=3,column=0)

#for item in ['analyze', 'describe', 'generate tags', 'OCR', 'thumbnail']:
#    serviceList.insert(END, item)


apiList.select_set(0)
apiList.event_generate("<<ListboxSelect>>")

#Right Frame and its contents
rightFrame = Frame(root, width=200, height = 600)
rightFrame.grid(row=0, column=1, padx=10, pady=2)

Label(rightFrame, text='VISION API').grid(row=0, column=0, columnspan=2)

photoCanvas1 = Canvas(rightFrame, width=400, height=300, bg='white')
photoCanvas1.grid(row=1, column=0, padx=2, pady=2, sticky='W')

photoCanvas2 = Canvas(rightFrame, width=400, height=300, bg='white')
photoCanvas2.grid(row=1, column=1, padx=2, pady=2, sticky='W')

file_path = ''

btnFrame = Frame(rightFrame, width=200, height = 200)
btnFrame.grid(row=2, column=0, padx=10, pady=2, columnspan=2)

log = Text(rightFrame, width = 125, height = 15, takefocus=0)
log.grid(row=3, column=0, padx=10, pady=2, columnspan=2)

load_button = Button(btnFrame, text="Capture 1", command=capture1_clicked)
load_button.grid(row=0, column=0, padx=10, pady=2)

submit_button = Button(btnFrame, text="Submit", command=submit_button_clicked)
submit_button.grid(row=0, column=1, padx=10, pady=2)

btn3 = Button(btnFrame, text="Capture 2", command=capture2_clicked)
btn3.grid(row=0, column=2, padx=10, pady=2)


root.mainloop() #start monitoring and updating the GUI
