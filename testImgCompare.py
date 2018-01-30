import cv2
import os
import numpy as np
from matplotlib import pyplot as plt

# Y:\local\cpstub-apps의 모든 폴더에서 icob.png를 가져옴
def readAndSaveIcons():
    loadPath = 'Y:/local/cpstub-apps'
    savePath = 'C:/git/myProject/test/icon'
    index = 0
    filenames = os.listdir(loadPath)
    for filename in filenames:
        filePath = os.path.join(loadPath, filename)
        if os.path.isdir(filePath):
            try:
                iconPath = os.path.join(filePath, "icon.png")
                if os.path.exists(iconPath):
                    img = cv2.imread(iconPath, cv2.IMREAD_UNCHANGED)
                    cv2.imwrite(os.path.join(savePath, str(index)+".png"), img)
                    index += 1
                else:
                    print(iconPath,"is not exists!!!!!")
            except Exception as e:
                print('*** Caught exception: %s: %s' % (e.__class__, e))
        else:
            print(filePath, "is not a dir!")

# helper tool로 캡쳐한 화면들 가져오기
def loadAllCapture():
    path = 'C:/git/orderingTestTool/test-helper2/download'
    filenames = os.listdir(path)
    captures = []
    for filename in filenames:
        filePath = os.path.join(path, filename)
        if os.path.isfile(filePath):
            try:
                img = cv2.imread(filePath, cv2.IMREAD_UNCHANGED)
                captures.append(img)
            except Exception as e:
                print('*** Caught exception: %s: %s' % (e.__class__, e))
        else:
            print(filePath, "is not a file!")
    print("success loadAllCapture.")
    return captures

# 오더링 부분만 잘라서 return
def cropOrdering(imgs):
    result = []
    for img in imgs:
        result.append(img[505:710, :, :])
    print("success cropOrdering.")
    return result

# Capture 이미지의 각 CP를 잘라서 return
def divImg(img):
    width = 133
    gap = 40
    startX = 44 + gap
    resultImg = []
    while startX <= img.shape[1]:
        startX -= gap
        resultImg.append(img[:, startX:startX+width,:])
        startX += width
    return resultImg

# 캡쳐들 가져와서 오더링의 CP부분을 분리해서 test/base 폴더에 저장
def doDivAndSaveCaptures():
    index = 0
    basePath = 'C:/git/myProject/test/base'
    captures = loadAllCapture()
    cropCaptures = cropOrdering(captures)
    for img in cropCaptures:
        divImgs = divImg(img)
        for div in divImgs:
            divPath = os.path.join(basePath, str(index)+'.png')
            cv2.imwrite(divPath, div)
            index += 1

# base에 icon이미지가 포함되어있는지 확인
def checkImageIncluded(baseImg, iconImg):
    #baseImg = cv2.imread(baseImgPath, cv2.IMREAD_COLOR)
    #iconImg = cv2.imread(iconImagePath, cv2.IMREAD_COLOR)

    baseImgCopy = baseImg.copy()

    res = cv2.matchTemplate(baseImgCopy, iconImg, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res > 0.8)
    count = 0
    for i in zip(*loc[::-1]):
        count += 1
    if count>0:
        return True
    else:
        return False

# icon 폴더에서 icon들을 읽어옴
def loadIcons():
    path = 'C:/git/myProject/test/icon'
    filenames = os.listdir(path)
    results = []
    for filename in filenames:
        filePath = os.path.join(path, filename)
        if os.path.isfile(filePath):
            try:
                img = cv2.imread(filePath, cv2.IMREAD_COLOR)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                results.append(img)
            except Exception as e:
                print('*** Caught exception: %s: %s' % (e.__class__, e))
        else:
            print(filePath, "is not a file!")
    return results

def removeSystemOrdering(toRemoveIcon):
    path = 'C:/git/myProject/test/base'
    filenames = os.listdir(path)
    for filename in filenames:
        filePath = os.path.join(path, filename)
        if os.path.isfile(filePath):
            try:
                img = cv2.imread(filePath, cv2.IMREAD_COLOR)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                if checkImageIncluded(img, toRemoveIcon):
                    os.remove(filePath)
            except Exception as e:
                print('*** Caught exception: %s: %s' % (e.__class__, e))
        else:
            print(filePath, "is not a file!")
    print("success remove system ordering")

def removeIconOverlap(toRemoveIcon, currentFileName):
    path = 'C:/git/myProject/test/icon'
    filenames = os.listdir(path)
    for filename in filenames:
        filePath = os.path.join(path, filename)
        if os.path.isfile(filePath):
            try:
                img = cv2.imread(filePath, cv2.IMREAD_COLOR)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                if checkImageIncluded(img, toRemoveIcon):
                    if filename != currentFileName:
                        os.remove(filePath)
            except Exception as e:
                print('*** Caught exception: %s: %s' % (e.__class__, e))
        else:
            print(filePath, "is not a file!")
    print("success remove system ordering")
"""
img = cv2.imread('C:/git/myProject/test/icon/49.png', cv2.IMREAD_COLOR)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
removeIconOverlap(img, "49.png")
"""
basePath = 'C:/git/myProject/test/base'
icons = loadIcons()
filenames = os.listdir(basePath)
trueList = []
f = open("C:/git/myProject/test/result.txt","w")
for filename in filenames:
    filePath = os.path.join(basePath, filename)
    if os.path.isfile(filePath):
        try:
            img = cv2.imread(filePath, cv2.IMREAD_COLOR)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            for index, icon in enumerate(icons):
                resCondition = checkImageIncluded(img, icon)
                if resCondition == True:
                    '''
                    print("base : ",filename, ", icon:", index)
                    print("===================================")
                    print("result : ",resCondition,"\n\n")
                    '''
                    if filename in trueList:
                        print("arleady added: ",filename)
                        plt.subplot(121),plt.imshow(img,cmap = 'gray')
                        plt.title('base'), plt.xticks([]), plt.yticks([])
                        plt.subplot(122),plt.imshow(icon,cmap = 'gray')
                        plt.title('icon'), plt.xticks([]), plt.yticks([])
                        plt.suptitle(resCondition)

                        plt.show()
                    else:
                        trueList.append(filename)
                    ## imshow하기
                    '''
                    plt.subplot(121),plt.imshow(img,cmap = 'gray')
                    plt.title('base'), plt.xticks([]), plt.yticks([])
                    plt.subplot(122),plt.imshow(icon,cmap = 'gray')
                    plt.title('icon'), plt.xticks([]), plt.yticks([])
                    plt.suptitle(resCondition)

                    plt.show()
                    '''
        except Exception as e:
            print('*** Caught exception: %s: %s' % (e.__class__, e))
    else:
        print(filePath, "is not a file!")
if trueList == filenames:
    print("=========================================================")
    print("All OK!!!")
else:
    print("=========================================================")
    print("Different List")
    print("=========================================================")
    print("not in filenames.")
    for i in trueList:
        if i not in filenames:
            print(i)
    print("=========================================================")
    print("not in trueList. = True여야하는데 False처리됨")
    count = 0
    for j in filenames:
        if j not in trueList:
            count += 1
            print(j)
    print("=========================================================")
    print("만약 False여야하는데 True처리된 애들이 있으면 하기 값이 다름")
    print(len(set(filenames)))
    print("False 처리 갯수 : ", count)
    print(len(trueList))
    print(len(set(trueList)))
