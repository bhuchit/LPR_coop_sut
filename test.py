import cv2
import pip._vendor.requests as requests
import numpy as np

#@title กรอกข้อมูล เพื่อกำหนดค่าให้กับตัวแปร
Apikey = "BghsplRaCk6QRBZR5fX7krSjOdn1RS0w" #@param {type:"string"}
url_lpr = "https://api.aiforthai.in.th/lpr-v2" #@param {type:"string"}
image_lpr = "/home/b5809820/Downloads/present/thai-car-dataset/195.jpg" #@param {type:"string"}
img = cv2.imread(image_lpr)
# img = cv2.resize(img,(600, 300))
#url = "https://api.aiforthai.in.th/lpr-v2"
url = url_lpr
payload = {'crop': '1', 'rotate': '1'}
files = {'image':open(image_lpr, 'rb')}
 
headers = {
    'Apikey': Apikey,
    }

if url_lpr.endswith("v2") == False:
    data = None

response = requests.post( url, files=files, data = payload, headers=headers)

print(response.json())

lpr = None
bbox = None
lp_obj = None
xLeftTop = None
yLeftTop = None
xRightBottom = None
yRightBottom = None
COLORS = np.random.randint(0, 255, size=3 )
colors = [int(c) for c in COLORS]

for r in response.json():
    lp_obj = r
    lpr = lp_obj.get('lpr')
    bbox = lp_obj.get('bbox')
    xLeftTop = int(bbox.get('xLeftTop'))
    yLeftTop = int(bbox.get('yLeftTop'))
    xRightBottom = int(bbox.get('xRightBottom'))
    yRightBottom = int(bbox.get('yRightBottom'))

cv2.rectangle(img,(xLeftTop, yLeftTop), (xRightBottom, yRightBottom), colors, 2)

# cv2.putText(img, lpr, (xLeftTop, yLeftTop), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv2.LINE_AA)
cv2.imshow('img', img)
cv2.waitKey(0)