import httplib, urllib, base64, json

headers = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': 'edbd2401b2414ad48f5e39bbdad34fa9',
}

params = urllib.urlencode({
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
})

faceOneFileName = '1.jpg'
faceTwoFileName='3.jpg'

faceOne=None;
faceTwo=None;

def postToFaceApi(fileName):
    try:
        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        conn.request("POST", "/face/v1.0/detect?%s" % params, open(fileName, 'rb'), headers)
        response = conn.getresponse()
        data = response.read()
        print(data)
        conn.close()
        return json.loads(data)
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))



def CompareFaces(faceId1, faceId2):
    headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': 'edbd2401b2414ad48f5e39bbdad34fa9',
    }

    params = urllib.urlencode({
    })

    body={}
    body['faceId1']= faceId1
    body['faceId2']=faceId2
    json_data= json.dumps(body)
    try:
        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        conn.request("POST", "/face/v1.0/verify?%s" % params, json_data, headers)
        response = conn.getresponse()
        data = response.read()
        print(data)
        return json.loads(data)
        conn.close()
    except Exception as e:
        print e
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

def TestCompareFaces():
    faceOne= postToFaceApi(faceOneFileName)
    faceTwo=postToFaceApi(faceTwoFileName)
    print(faceOne[0])
    result=CompareFaces(faceOne[0]['faceId'], faceTwo[0]['faceId'])
    print(result['isIdentical'])

TestCompareFaces()
