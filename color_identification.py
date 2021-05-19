#The sample picture should be in the folder in which you have the code and the colors
#data

#First importing the required modules 
from cv2 import cv2              #OpenCV
import pandas as pd              #pandas
import argparse                  #argparse

#creating argument parse to take image path from command line 
parser=argparse.ArgumentParser()
parser.add_argument('-i','--image',required=True,help='Image path')
args=vars(parser.parse_args())
img_path=args['image']

img=cv2.imread(img_path)        #reading the image with opencv

#getting the dimensions of the image
dimensions=img.shape
height=img.shape[1]
width=img.shape[0]
area=height*width


#declaring global variables
click=False
r = g = b = xpos = ypos =0

#reading csv file with pandas and giving names to each column
index=["color","color_name","hex","R","G","B"]
csv=pd.read_csv('MYshades.csv',names=index,header=None)

#function to get closest-matching color
def getColorName(R,G,B):
    minimum=float('inf')
    cname=""
    for i in range(len(csv)):
        d = abs(R-int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(G - int(csv.loc[i, "B"]))
        if d<=minimum:
            minimum=d
            cname=csv.loc[i,"color_name"]
    return cname

 #function to get x,y coordinators of mouse double click
def draw_function(event,x,y, flags,param):
    if event==cv2.EVENT_LBUTTONDBLCLK:
        global b,g,r, xpos,ypos,click
        click=True
        xpos=x
        ypos=y
        b,g,r=img[y, x]
        b=int(b)
        g=int(g)
        r=int(r)

if area<=612000:
    cv2.namedWindow('image')
else:
    cv2.namedWindow('image',cv2.WINDOW_NORMAL)
    cv2.setMouseCallback('image',draw_function)

while(1):
    cv2.imshow("image",img)
    if click:
        recEnd=(round(width*.735),round(height*.1))
        textStart = (round(width*.03), round(height*.05))
        cv2.rectangle(img, (28,28), recEnd, (b,g,r), -1)
        text = 'Color is: '+ getColorName(r, g, b)  + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)
        if r + g+ b >=600:
            cv2.putText(img , text , textStart, cv2.FONT_HERSHEY_TRIPLEX, 1, (0,0,0) , 1 , cv2.LINE_AA)
        else:
            cv2.putText(img, text, textStart, cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
        click=False

#break loop when user hits 'esc' key
    if cv2.waitKey(20) & 0xFF == 27:
        break




                
