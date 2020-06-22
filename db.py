from pymongo import MongoClient
from bson import ObjectId
from time import strftime
from cctv import CCTV
import cv2
DATE = strftime("%Y-%m-%d %H:%M:%S")

class DB(object):
    # initial
    def __init__(self):
        self.client = MongoClient(host='localhost', port=27017)
        self.db = self.client['test']
        self.col_vehicle = self.db['vehicle']
        self.col_cctv = self.db['cctv']

    # cctv: get update delete
    def getRTSP_cctv(self):
        # tmp = []
        self.data = self.col_cctv.find()
        for x in self.data:
            return x.get('rtsp')
            
    def getAll_cctv(self):
        tmp = []
        self.data = self.col_cctv.find()
        for x in self.data:
            tmp.append(x)
            return tmp

    def insert_cctv(self, cctv_obj):
        return self.col_cctv.insert_one(cctv_obj)
    
    def update_cctv(self, ojbId, cctv_obj):
        return self.col_cctv.update_one({'_id': ObjectId(oid=ojbId)}, {'$set':cctv_obj})

    def delete_cctv(self, objId):
        return self.col_cctv.delete_one({'_id': ObjectId(oid = objId)})

    # vehicle: get update delete
    def getAll_vehicle(self):
        self.tmp = []
        self.data = self.col_vehicle.find()
        for x in self.data:
            # print(x)
            self.tmp.append(x)
        return self.tmp
    
    def insert_vehicle(self, vehicle_obj):
        return self.col_vehicle.insert_one(vehicle_obj)

    def update_vechicle(self, ojbId, vehicle_obj):
        return self.col_vehicle.update_one({'_id': ObjectId(oid=ojbId)}, {'$set':vehicle_obj})

    def delete_vehicle(self, objId):
        return self.col_vehicle.delete_one({'_id': ObjectId(oid = objId)})
    
    def check_licensePlate_is_equal(self, lp_id):
        count = self.col_vehicle.find({'$and':[{'plate': lp_id, 'detection_status': False}]}).count()
        if count is not 0 :
            return True
        else:
            return False

    def get_objId_findBy_lpId(self, input):
        data = self.col_vehicle.find({"plate": input})
        for x in data:
            objId = x.get('_id')
            return str(objId)
    
    def update_detection_status_and_source_path(self, objId, source_name):
        return self.col_vehicle.update_one({'_id': ObjectId(oid=objId)}, {'$set':{'detection_status': True, "detected_dateTime": str(DATE), 'img_path': source_name}})
    
    def xxx(self):
       return self.col_vehicle 

