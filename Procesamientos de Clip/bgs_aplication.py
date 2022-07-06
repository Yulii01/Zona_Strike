from demo2 import bgs_library_method

#metodos definidos de bgs para aplicarle al clip
def aplication(cant_clip):
    count = 1;

    while (count<=66):
        if(count<10):
            bgs_library_method("0"+str(count))
        else:
            bgs_library_method(str(count))
        count = count+1     
