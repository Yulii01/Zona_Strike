import subprocess

def Deinterleizing(intput,output):
    cmd = ["ffmpeg","-i",intput,"-vf", "yadif", "-c:v", "libx264","-preset", "slow", "-crf", "19", "-c:a", "aac", "-b:a", "256k", output]
    exit_code = subprocess.call(cmd)

