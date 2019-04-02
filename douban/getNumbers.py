import sys
import cv2
import numpy as np

#######   training part    ###############
# samples = np.loadtxt('generalsamples.data', np.float32)
# responses = np.loadtxt('generalresponses.data', np.float32)
# responses = responses.reshape((responses.size, 1))
#
model = cv2.ml.KNearest_create()
# model.train(samples, cv2.ml.ROW_SAMPLE, responses)


def getNum(path):
    im = cv2.imread(path)
    out = np.zeros(im.shape, np.uint8)
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    # 预处理一下
    for i in range(gray.__len__()):
        for j in range(gray[0].__len__()):
            if gray[i][j] == 0:
                gray[i][j] == 255
            else:
                gray[i][j] == 0
    thresh = cv2.adaptiveThreshold(gray, 255, 1, 1, 11, 2)

    image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    count = 0
    numbers = []
    for cnt in contours:
        if cv2.contourArea(cnt) > 80:
            [x, y, w, h] = cv2.boundingRect(cnt)
            if h > 25:
                cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)
                roi = thresh[y:y + h, x:x + w]
                roismall = cv2.resize(roi, (30, 30))
                roismall = roismall.reshape((1, 900))
                roismall = np.float32(roismall)
                retval, results, neigh_resp, dists = model.findNearest(roismall, k=1)
                string = str(int((results[0][0])))
                numbers.append(int((results[0][0])))
                cv2.putText(out, string, (x, y + h), 0, 1, (0, 255, 0))
                count += 1
        if count == 10:
            break
    return numbers
