from random import randint, random
import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy import spatial

class Detection_blob:
    def __init__(self):
        self.black = (255, 255, 255)
        self.Th = 240
        self.thresholdDistance = 20
        self.ROI_TH = 30

        # Setup SimpleBlobDetector parameters.
        self.params = cv2.SimpleBlobDetector_Params()

        # Change thresholds
        self.params.minThreshold = 10
        self.params.maxThreshold = 200

        # Filter by Area.
        self.params.filterByArea = True
        self.params.minArea = 20
        self.params.maxArea = 175

        # Filter by Circularity
        self.params.filterByCircularity = True
        self.params.minCircularity = 0.4

        # Filter by Convexity
        self.params.filterByConvexity = True
        self.params.minConvexity = 0.3

        # Filter by Inertia
        self.params.filterByInertia = True
        self.params.minInertiaRatio = 0.3

        # Filter by Color
        self.params.filterByColor = True
        self.params.blobColor = 255

        self.detector = cv2.SimpleBlobDetector_create(self.params)    # son detectados 'blobs' o grupos de píxeles que la forma de la agrupación está determinada por los parámetros anteriores

        self.backSub = cv2.createBackgroundSubtractorMOG2() 
    
    def Softened(self,frame):
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        gray= cv2.medianBlur(gray,5)
        gray = self.backSub.apply(gray)
        return gray


    def Blob_Ocurrence_for_Frame(self,frame2,gray):
            gray2 = self.Softened(frame2)
            gray2= self.backSub.apply(gray2)
            output = gray2.copy()
            rested = gray2 - gray
            gray = gray2
            ret, result = cv2.threshold(rested,self.Th,255,cv2.THRESH_BINARY)
            keypoints = self.detector.detect(result)
            return keypoints



    def Blob_Cordinates(self,keypoints):
            blob=[]
            if keypoints:   #si existen keypoints, es reajustado el centro y guardado el keypoint y el número del frame en que se tomó
                for keypoint in keypoints:
                    newCenter = [keypoint.pt[0], keypoint.pt[1]]
                    blob.append(keypoint.pt)
            return blob

    def draw_Keypoints(self,frame,keypoints):
        image=cv2.drawKeypoints(frame, keypoints, np.array([]), (0,0,255),  cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)  # se muestran los keypoints
        return image
            
    def Draw_distributiony(self,all_blob):
        x_val = [element[0] for element in all_blob]
        y_val = [element[1]*-1 for element in all_blob]
        k =sorted(all_blob)
        plt.scatter(x_val,y_val)
        m,n,points=self.Ransac(x_val,y_val)
        x = range (40,90)
        plt.plot(x, [self.recta(i,m,n) for i in x])
        plt.show()
        return points
      
    def Draw_distributionX(self,all_blob):
        x_val = [element[0] for element in all_blob]
        y_val = [element[1]*-1 for element in all_blob]
        k =sorted(all_blob)
        plt.scatter(x_val,y_val)
        a,b,c,points=self.RansacPar(x_val,y_val)
        x = range (40,90)
        plt.plot(x, [self.parabola_ecua([a,b,c],i) for i in x])
        plt.show()
        return points
    
    def punto_aislado(self,points):
        ctr =False
        candidatos=[]
        for i in range(len(points)):
            for j in range(len(points)):
                if(j==i):
                    continue
                if(self.is_in_ratio(points[i][0],points[i][1],points[j][0],points[j][1],20)):
                    ctr = True
            if(ctr):
                ctr=False
                candidatos.append((points[i]))
        
        return candidatos          
    
    def is_in_ratio(self,x,y,x1,y1,r):
        return abs(np.sqrt((x-x1)**2 + (y-y1)**2))<=r

    def Video_Blob_Detector(self,video):
        cap = cv2.VideoCapture(video)
        ret, frame = cap.read()
        gray= self.Softened(frame)
        all_blob=[]
        i=0
        frameNumber=0
        y_distribution=[]
        x_distribution=[]
        while True:
            ret2, frame2 = cap.read()
            if frame2 is None:
                break
            frameNumber += 1
            if(frameNumber)<1 or frameNumber>90:
                continue
            gray2 = self.Softened(frame2)
            output = gray2.copy()
            rested = gray2 - gray
            gray = gray2
            ret, result = cv2.threshold(rested,self.Th,255,cv2.THRESH_BINARY)
            keypoints = self.detector.detect(result)

            if keypoints:   #si existen keypoints, es reajustado el centro y guardado el keypoint y el número del frame en que se tomó
                for keypoint in keypoints:
                    newCenter = [keypoint.pt[0], keypoint.pt[1]]
                    if(keypoint.pt[1])>320:
                        continue
                    x_distribution.append((frameNumber,keypoint.pt[0]))
                    y_distribution.append((frameNumber,keypoint.pt[1]))
        x_distribution = self.punto_aislado(x_distribution)
        y_distribution = self.punto_aislado(y_distribution)
        return y_distribution , x_distribution



    def detect_parab(self,points):
        try:
            A = np.array([[points[0][0]**2, points[0][0], 1], [points[1][0]**2, points[1][0], 1], [points[2][0]**2, points[2][0], 1]])
            B = np.array([points[0][1], points[1][1], points[2][1]])
            X = np.linalg.inv(A).dot(B)

            return X
        except :
            return [0,0,0]    
    
    def RansacPar(self,x_val,y_val):
        max_count =0
        max_a =0
        point_X=[]
        max_b =0
        max_c=0
        for i in range(500):
            r1 = randint(0,len(x_val)-1) 
            r2 = randint(0,len(x_val)-1)
            r3 = randint(0,len(x_val)-1)
            a,b,c = self.detect_parab([(x_val[r1],y_val[r1]),(x_val[r2],y_val[r2]),(x_val[r3],y_val[r3])])
            if(a>0):
                continue                
            count =0    
            point=[]      
            for x in range(len(x_val)):

                if((abs(a*x_val[x]**2 +b*x_val[x] + c - y_val[x]) <=10)):
                    count +=1
                    point.append((x_val[x],y_val[x]))
                   
                if(count >5 and count <=20):
                    if (count>=max_count)   :
                        max_count =count
                        max_a =a
                        max_b=b
                        max_c =c 
                        point_X = point.copy()
                        
       
        return (max_a,max_b,max_c,point_X)



    def ecuacion(self,x1,y1,x2,y2):
        try:
            m=(y2 - y1) / (x2-x1)
        except:
            m=0
        n = y1-m*x1 
        return m,n



    def Ransac(self,x_val,y_val):
        max_count =0
        max_m =0
        point_X=[]
        max_n =0
        for i in range(500):
            r1 = randint(0,len(x_val)-1) 
            r2 = randint(0,len(x_val)-1)
            m,n = self.ecuacion(x_val[r1],y_val[r1],x_val[r2],y_val[r2])
            if(m>0):
                continue       
            count =0 
            point=[]   
                              
            for x in range(len(x_val)):
                if((abs(m*x_val[x]+n - y_val[x]) <=10)):
                    count +=1
                    point.append((x_val[x],y_val[x]))
                   
                if(count >5 and count <=20):
                    if (count>=max_count)   :
                        max_count =count
                        max_m =m
                        max_n=n 
                        point_X = point.copy()
                       
           
        return (max_m,max_n,point_X)

    def recta (self,x,m,n):
        return  m*x+n  

    def parabola_ecua (self,coef,x):
        return coef[0]*x**2 + coef[1]*x+coef[2]
        
    def main (self,videos):
        for video in videos:
            valoresx,valoresy= self.Video_Blob_Detector(video)

            pointrecta=self.Draw_distributiony(valoresy)

            pointpara = self.Draw_distributionX(valoresx)

            ball=[]
            for i in pointpara:
                for j in pointrecta:
                    if(i[0]==j[0]):
                        ball.append((-j[1],-i[1]))

            cap = cv2.VideoCapture(video)

            while True:
                ret,frame= cap.read()
                if (frame is None):
                    break
                for i in ball:
                    cv2.circle(frame,(int(i[0]),int(i[1])),10,(0,0,255))
                
                cv2.imshow("tracking",frame)
                keyboard = cv2.waitKey()
                if keyboard == 'q' or keyboard == 27:
                        break


            cap.release()
            cv2.destroyAllWindows()


################
# Ejecutar metodo main con en el nombre del clip 
#sale primero x_distribution 
#sale segundo y_distribution
#Frame de video con circulos rojos (mejorable) tocar cualkier tecla y seguir al proximo frame

detec = Detection_blob().main(["01 Deinterleizing.mp4"])