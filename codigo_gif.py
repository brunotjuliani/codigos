#BIBLIOTECAS
import cv2
import numpy as np
import glob
import os

#DEFINE VARIAVEIS
modelo = "NCEP_WRF5K" #COPEL / ECMWF / NCEP_WRF5K
data = "2020-12-07"
#diretorio = "/discolocal/bruno/Mapas_Chuva/"+modelo+"/"+data
diretorio = "/Users/brunojuliani/github/dados/"+modelo+"/"+data

#CODIGO USUAL
os.chdir(diretorio)
img_array = []

for filename in sorted(glob.glob(diretorio+"/*.png")):
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(img)


out = cv2.VideoWriter(modelo+"_"+data+'.avi',cv2.VideoWriter_fourcc(*'MJPG'), 1.1, size)

for i in range(len(img_array)):
    out.write(img_array[i])
out.release()


#CODIGO RADAR
#modelo = "RADAR" #COPEL / ECMWF / NCEP_WRF5K / RADAR
#data = "2020-08-18-17"
#diretorio = "/home/bruno/Documentos/Mapas_Chuva/"+modelo+"/"+data

#os.chdir(diretorio)
#img_array = []
#for filename in glob.glob(diretorio+"/*.jpeg"):
#    img = cv2.imread(filename)
#    height, width, layers = img.shape
#    size = (width,height)
#    img_array.append(img)


#out = cv2.VideoWriter(modelo+"_"+data+'.mp4',cv2.VideoWriter_fourcc(*'MP4V'), 1.3, size)

#for i in range(len(img_array)):
#    out.write(img_array[i])
#out.release()
