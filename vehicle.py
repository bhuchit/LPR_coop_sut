class Vehicle(object):

    def __init__(self, plate="", brand="", province="", color="", detection_status=bool, detected_dateTime="", img_path=""):
        super().__init__()
        self.plate = plate
        self.brand = brand
        self.province = province
        self.color = color
        self.detection_status = detection_status
        self.detected_dateTime = detected_dateTime
        self.img_path = img_path
    # Methods
    def get_plate(self):
        return self.plate 

    def set_plate(self, plate):
        self.plate = plate
    
    def get_brand(self):
        return self.brand 

    def set_brand(self, brand):
        self.brand = brand

    def get_province(self):
        return self.province 

    def set_province(self, province):
        self.province = province

    def get_color(self):
        return self.color 

    def set_color(self, color):
        self.color = color
    
    def get_detection_status(self):
        return self.detection_status 

    def set_detection_status(self, detection_status):
        self.detection_status = detection_status
    
    def get_detected_dateTime(self):
        return self.detected_dateTime 

    def set_detected_dateTime(self, detected_dateTime):
        self.detected_dateTime = detected_dateTime

    def get_img_path(self):
        return self.img_path 

    def set_img_path(self, img_path):
        self.img_path = img_path