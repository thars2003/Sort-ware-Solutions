#import-----------------
import cv2
import numpy as np
#--------------------------


#setup and initialization variables-------------------
cam=cv2.VideoCapture(0) #laptop camera- 0


card_id=0
#----------------------------------------
def order_points(pts):
    #order: tl, tr, br, bl
    rect=np.zeros((4,2), dtype="float32")
    sum=np.sum(pts,axis=1)
    diff= np.diff(pts,axis=1)


    rect[0]= pts[np.argmin(sum)] #sum min = tl
    rect[1]= pts[np.argmin(diff)] #diff min = tr
    rect[2]= pts[np.argmax(sum)] #sum max = br
    rect[3]= pts[np.argmax(diff)] #sum max = bl


    return rect


def flatten_image(image, pts):
    rect= order_points(pts)
    (tl, tr, br, bl) = rect


    widthA = np.linalg.norm(br - bl)
    widthB = np.linalg.norm(tr - tl)
    maxWidth = int(max(widthA, widthB)) #max width


    heightA = np.linalg.norm(tr - br)
    heightB = np.linalg.norm(tl - bl)
    maxHeight = int(max(heightA, heightB)) #max height


    newpts = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")
   
    M= cv2.getPerspectiveTransform(rect,newpts)
    warped= cv2.warpPerspective(image,M, (maxWidth,maxHeight))#warped the image


    return warped




# Main Loop----------------
while True:
    ret,frame = cam.read()
    if ret==False:
        break          #breaks if the frame is not read properly


    gray= cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # make it b/w
    blur= cv2.GaussianBlur(gray,(5,5),0) #blurs a 5x5 grid
    edged= cv2.Canny(blur,50,150) # takes edges ranging from 50-150
    contours,_= cv2.findContours(edged, cv2. RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #finds the points all around the edge


    for cnt in contours:
        perimeter= cv2.arcLength(cnt, True)
        approx= cv2.approxPolyDP(cnt, 0.02 * perimeter, True) #gives 4 points for rectangular shape


        if len(approx) == 4 and cv2.contourArea(approx)>1000: #checks if rect and checks if it's big might need to change the value later
            cv2.drawContours(frame, [approx], -1, (0,255,),2) #creates a orange contour around the card


            warped= flatten_image(frame, approx.reshape(4,2))#flattenning the card 4 points in x,y
            cv2.imshow("Flattened Card", warped)


            card_id += 1
            cv2.imwrite(f"card_{card_id}.png", warped) #saving the image

    cv2.imshow("Live Camera Feed", frame)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break


cam.release()
cv2.destroyAllWindows()









