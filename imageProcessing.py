import numpy as np
import cv2

class ImgProcessing:
    factv = 0.4
    facth = 0
    def __init__(self,cam):
        self.cap = cv2.VideoCapture(cam)
    
    def getValue(self):
        # update data
        ret,frame = self.cap.read()

        img_bn = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        v = int(img_bn.shape[0]/10)
        h = int(img_bn.shape[1]/10)
        """d1 = int(0.2*v/2)
        d2 = int(1.8*v/2)
        w1 = int(0.2*h)
        w2 = int(0.8*h)"""
        #cv2.rectangle(frame,(w1,d1),(w2,d2),(0,255,0),1)
        # getting region
        img_bn = cv2.resize(img_bn,(h,v),interpolation = cv2.INTER_AREA)
        img_bn = cv2.GaussianBlur(img_bn,(5,5),0)
        img_bn = img_bn[int(self.factv*v/2):int((2-self.factv)*v/2),int(self.facth*h):int((1-self.facth)*h)]
        obj = np.mean(img_bn, axis=1)
        dobj = np.convolve(obj, [25, -25], 'valid')

        # drawing
        """retval = cv2.plot.Plot2d_create(dobj)
        retval.setMaxY(100)
        retval.setMinY(-100)
        mplot = retval.render()"""
        # analisis
        t1 = np.max(dobj)
        t2 = np.min(dobj)
        return t1,t2