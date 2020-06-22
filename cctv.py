class CCTV(object):
    
    def __init__(self, url = '', rtsp = '', username = '', password = ''):
        self.rtsp = rtsp
        self.username = username
        self.password = password

    # Methods
    def get_rtsp(self):
        return self.rtsp 

    def set_rtsp(self, rtsp):
        self.rtsp = rtsp

    def get_username(self):
        return self.username 

    def set_username(self, username):
        self.username = username

    def get_password(self):
        return self.password 

    def set_password(self, password):
        self.password = password

