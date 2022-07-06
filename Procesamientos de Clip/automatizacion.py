import cv2 as cv 
import os
import imageio_ffmpeg
import pandas as pd


# Clase destinada a la creacion de metadatos interesantes para la inestigacion guardados a un csv
#
class Csv:
   
    def __init__(self,clip) :
        self.clip = clip
        self.total_frames=0
        self.Inicio=0
        self.final=0
        self.estadio = ""
        self.Horario=""
        self.direccion="" 
        self.total_segundos=0  
        self.fps = 0
        self.decision = ""
        
        
    def frame_detection(self):
        self.total_frames, self.total_segundos = imageio_ffmpeg.count_frames_and_secs(self.clip)
        self.fps = self.total_frames/self.total_segundos
        video = cv.VideoCapture(self.clip)
        frame_list = []
        count = 0
        while video.isOpened() and count <=120:
            ret,frame = video.read()
            count = count +1 
            if(not ret): break
            frame_list.append(frame)

        self.cantidad_frame=len(frame_list)
        return frame_list


    def show_frame(self,frame_list:list):
        count  = 1
        for frame in frame_list:
            if(count>40):
                cv.imshow("Frame%d" % count,frame)
                #cv.waitKey(0)
                if cv.waitKey(0) & 0xFF == ord('q'):
                    
                    cv.destroyAllWindows()
                    break  
                        
                cv.destroyAllWindows()
            count = count + 1

    def detection_mov(self):
        self.Inicio = input("Inicio del lanzamiento")
        self.final = input("Final del lanzamiento")

    def completar (self):
        self.Horario = input("Horario de juego"  )
        self.estadio = input("Estadio de juego"  )
        self.decision = input("Decision arbitral")
        

    def exportar(self,clip):
        tf = ["total_frames",self.total_frames]
        ts = ["total segndos",self.total_segundos]
        fps = ["Fps",self.fps]
        ini = ["inicio lanzamiento",self.Inicio]
        fin= ["final lanzamiento",self.final]
        estdio= ["Estadio",self.estadio]
        Hor= ["Horario",self.Horario]
        dir = ["Direccion",self.direccion]

        filas = [tf,ts,fps,ini,fin,estdio,Hor,dir]
        df = pd.DataFrame(filas,columns=['Dato','Valor'])

        df.to_csv(clip,index=False)


    @staticmethod
    def crear_csv(cant_clip):
        count = 1

        while (count<cant_clip):
            if (count < 10):
                archivo = Csv('0'+str(count)+'.mp4')  
                lis = archivo.frame_detection()
                archivo.show_frame(lis) 
                archivo.detection_mov()
                archivo.completar()
                archivo.exportar('0'+str(count))     
            else:
                archivo = Csv(str(count)+'.mp4')  
                lis = archivo.frame_detection()
                archivo.show_frame(lis) 
                archivo.detection_mov()
                archivo.completar()
                archivo.exportar(str(count)) 
            count = count+1    

