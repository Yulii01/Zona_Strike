import subprocess
import  bashejecutetion
from os import mkdir
import shutil



#si no estan creados los clip entonces toma el video completo 
def clip ():
    archivo = open('tiempos.txt')
    titulo= archivo.readline().split('\n')
    count = 1
    for tiempos in archivo:
        tiempos= tiempos.split()
        cut_video(titulo[0],(tiempos[0]),(tiempos[1]),count)
        bashejecutetion.Deinterleizing(str(count)+".mp4",str(count)+".mp4")
        count=count+1

def cut_video(video,initial,end,count):
    cmd =["ffmpeg", "-i", str(video), "-map" ,"0",  "-ss",str(initial), "-to",str(end) ,"-c","copy", str(count)+".mp4"]
    exit_code = subprocess.call(cmd)

#clip()    

#si ya estan los clip
def main (max):
    count =  1
    while(count < max):
        if count < 10:
            mkdir("Clip 0" + str(count))
            bashejecutetion.Deinterleizing("0" + str(count)+".mp4","0"+ str(count)+ " Deinterleizing"+".mp4")
            shutil.move('./0' + str(count) + '.mp4','./Clip 0'+ str(count))
            shutil.move('./0'+ str(count)+ ' Deinterleizing.mp4','./Clip 0'+ str(count))
            shutil.move('./0'+ str(count),'./Clip 0'+ str(count))

            count=count+1

        else :
            mkdir("Clip " + str(count))
            bashejecutetion.Deinterleizing(str(count)+".mp4",str(count)+ " Deinterleizing"+".mp4")
            shutil.move('./' + str(count) + '.mp4','./Clip '+ str(count))
            shutil.move('./'+ str(count)+ ' Deinterleizing.mp4','./Clip '+ str(count))
            shutil.move(str(count),'./Clip '+ str(count))
            count=count+1




