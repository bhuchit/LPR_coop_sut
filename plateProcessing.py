from __future__ import print_function
from imutils.video import WebcamVideoStream
import argparse
import imutils
import cv2
import datetime
import pytesseract
import re
import numpy as np
from db import DB
cv2
MODEL_CASCADE_0 = ('static/classifier/cascade.xml')
LICENSE_PLATE_CASCADE = cv2.CascadeClassifier(MODEL_CASCADE_0)
REGEX_PATTERN = r"[ฯ-๛\s!-/:-@[-~]+"
TESSERACT_CONFIG = ('-l tha --oem 1 --psm 6')
DATE = datetime.date.today()

db = DB()

class PlateProcessing(object):

    def plateProcessing(self, frame):
        self.licensePlateCrop = None
        self.licensePlateRecognition = None
        self.licensePlate = []
        self.status = False
        self.frame = frame

        def recognition(LicensePlateCrop):
            self.licensePlateRecognition = pytesseract.image_to_string(LicensePlateCrop, config=TESSERACT_CONFIG)
            self.licensePlateRecognition = re.sub(REGEX_PATTERN, '', self.licensePlateRecognition)
            return self.licensePlateRecognition

        # self.frame = cv2.resize(self.frame, (640,480))
        frame_rgb = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        licensePlatesCascade = LICENSE_PLATE_CASCADE.detectMultiScale(frame_rgb, 1.1, 1)

        if licensePlatesCascade is not ():
            COLORS = np.random.randint(0, 255, size=3 )
            colors = [int(c) for c in COLORS]
            font = cv2.FONT_HERSHEY_SIMPLEX
            for (x, y, w, h) in licensePlatesCascade:
                
                self.LicensePlateCrop = self.frame[y:y+h, x:x+w]
                self.licensePlate.append(recognition(self.LicensePlateCrop))

                print(recognition(self.LicensePlateCrop))
                if db.check_licensePlate_is_equal(recognition(self.LicensePlateCrop)) is True:
                    cv2.rectangle(self.frame, (x,y), (x+w,y+h), (0,255,0), 2)
                    cv2.putText(self.frame, '[ Found ]', (x,y-10), font, 0.5, (0,255,0), 10, cv2.LINE_AA)
                    objId = db.get_objId_findBy_lpId(recognition(self.LicensePlateCrop))
                    file_name = '%s-%s.jpg' % (objId, DATE)
                    print(self.licensePlate,': updated')
                    self.status = True
                    outFile = 'static/img/img_lp_detected/%s' % (file_name)
                    self.license_plate = cv2.resize(self.LicensePlateCrop, (320, 180))
                    cv2.imwrite(outFile, self.LicensePlateCrop)
                    db.update_detection_status_and_source_path(objId, file_name)
                else:
                    cv2.rectangle(self.frame, (x,y), (x+w,y+h), colors, 2)
                    cv2.putText(self.frame,'License Plate',(x,y-10), font, 0.5, colors, 2, cv2.LINE_AA)

        jpeg = cv2.imencode('.jpg', self.frame)[1].tobytes()

        return jpeg, self.frame