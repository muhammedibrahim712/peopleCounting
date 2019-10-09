import cv2
import time
from datetime import datetime
import numpy as np
from detection.FaceDetector import FaceDetector
from centroidtracker import CentroidTracker
import collections
from collections import OrderedDict
from skimage import measure
import webAPI

# Face Size for comparing two faces
ROWS = 30
COLS = 30

# Threshold Values for comparing two faces
TH_CNT_COMPARE_FACES = 7.5
TH_VAL_COMPARE_FACES = 0.4

# Threshold for Detecting Face
TH_AVE_FACE_SCORE = 0.6


# UPS TIME, Duplicated Time
UPS_TIME = 10
DUPLICATED_TIME = 600

# FRAME RATE
FRAME_RATE = 0.3

# CONSIDERED WITHD, HEIGHT
START_WITHD = 6 / 17
END_WIDTH = 11 / 17
START_HEIGHT = 2 / 5
END_HEIGHT = 1

# Criteria that check if image quality is good or bad
IMAGE_QUALITY_CRITERIA = 0.75

# AREA of Non Faces
NON_FACE_AREA_X = 80
NON_FACE_AREA_Y = 80

face_detector = FaceDetector()

# Face Detection Function
def is_detected(frame):
    TH_VAL_FACE_DECTED = 0.5
    boxes, scores, ages, genders = face_detector.detect(frame)
    t_face_boxes = boxes[np.argwhere(scores>TH_VAL_FACE_DECTED).reshape(-1)]
    t_face_scores = scores[np.argwhere(scores>TH_VAL_FACE_DECTED).reshape(-1)]

    H, W, C = frame.shape

    sLimit = 0
    eLimit = 1

    face_boxes = []
    face_scores = []

    cnt = len(t_face_boxes)
    for i in range(cnt):
        if t_face_boxes[i][3] > (W * eLimit):
            continue

        if t_face_boxes[i][1] < (W * sLimit):
            continue

        face_boxes.append(t_face_boxes[i])
        face_scores.append(t_face_scores[i])

    face_ages = []
    face_genders = []

    rows = boxes.shape[0]

    for i in range(rows):
        if scores[i] > TH_VAL_FACE_DECTED:
            face_ages.append(ages[i])
            face_genders.append(genders[i])

    return face_boxes, face_scores, face_ages, face_genders

# Comparing two faces Function
def is_match(faces1, faces2):

    similar_cnt = 0

    faces1_cnt = len(faces1)    
    faces2_cnt = len(faces2)
    if faces1_cnt > 10:
        faces1_cnt = 10

    if faces2_cnt > 10:
        faces2_cnt = 10

    TH_CNT = int((faces1_cnt * faces2_cnt) / TH_CNT_COMPARE_FACES)

    # if TH_CNT < 2 or faces1_cnt <= 2 or faces2_cnt <= 2:
    #     return False

    TH = TH_VAL_COMPARE_FACES   
    for i in range(faces1_cnt):
        f1 = faces1[i]
        for j in range(faces2_cnt):
            f2 = faces2[j]
            ts = measure.compare_ssim(f1, f2)

            if ts > TH:
                similar_cnt = similar_cnt + 1
            

    # similarity = similarity / (faces1_cnt * faces2_cnt)
    print(str(faces1_cnt) + " * " + str(faces2_cnt) + " -> " + str(TH_CNT) + " ??? " + str(similar_cnt))
    if similar_cnt > TH_CNT:
        return True
    else:
        return False


if __name__ == '__main__':

    TOTAL_COUNT = 0

    # cam = cv2.VideoCapture("sample.mp4")
    cam = cv2.VideoCapture("rtsp://admin:Triv45633@192.168.1.25")

    print('Start Recognition!')

    ct = CentroidTracker()
    # the number of each tracking faces
    objectID_cnt = {}

    # face list of tracking faces according to objectID
    objectID_faces = {}
    objectID_centroids = {}
    saving_faces = {}
    objectID_minages = {}
    objectID_maxages = {}
    objectID_genders = {}
    objectID_accuracys = {}
    objectID_scores = {}
    objectID_Y = {}

    CompanyID = 2
    StoreID = 1
    CameraID = 1
    UPS_People_No = 0

    last_people_time = time.time()

    savevisitorinfo_data = {}
    savevisitorinfo_data["ClientCode"] = "VisTest"
    savevisitorinfo_data["CompanyID"] = str(CompanyID)
    savevisitorinfo_data["StoreID"] = str(StoreID)

    visitors = []

    # face DB for last 10 mins according to objectID    
    ten_min_face_db = {}

    # objectID DB for last 10 mins according to the entrance time
    entrance_time_db = {}

    prevTime = time.time()

    while True:

        if UPS_People_No > 0:
            cur_time = time.time()            
            if cur_time > last_people_time + UPS_TIME:

                UPS_People_No = 0
                visitors = []

                print("savevisitorinfo")
                print(savevisitorinfo_data)
                r = webAPI.savevisitorinfo(savevisitorinfo_data)
                print(r)
                print(r.json())

        print(len(entrance_time_db))
        for (objectID, entrance_time) in entrance_time_db.items():
            print(str(objectID) + " - " + str(len(ten_min_face_db[objectID])) + "faces : " + str(time.asctime(time.localtime(entrance_time))))



        ret, frame = cam.read()
        if ret == False:
            continue
        
        # print(frame.shape)
        # showing_frame = cv2.resize(frame, (0, 0), fx=FRAME_RATE, fy=FRAME_RATE)  # resize frame (optional)

        H, W, C = frame.shape
        sW = int(W * START_WITHD)
        eW = int(W * END_WIDTH)
        sH = int(H * START_HEIGHT)
        eH = int(H * END_HEIGHT)
        frame = frame[sH:eH, sW:eW, 0:3]
        showing_frame = cv2.resize(frame, (0, 0), fx=FRAME_RATE, fy=FRAME_RATE)  # resize frame (optional)
        t_frame = frame
        # print(t_frame.shape)
        # print(showing_frame.shape)        
        h_rows, w_cols, dummy = t_frame.shape

        rects = []
        centers = []
        face_boxes, face_scores, face_ages, face_genders = is_detected(frame)
        if len(face_boxes) <= 0:
            print("No Face")

        else:
            frame_save_path = "camera25_frame_" + str(TOTAL_COUNT) + "_" + str(len(face_boxes)) + ".jpg"
            # cv2.imwrite(frame_save_path, frame)
            # print('Detected_FaceNum: %d' % len(face_boxes))
            for i in range(len(face_boxes)):
                box = face_boxes[i]
                rects.append((box[1], box[0], box[3], box[2]))
                center_x = int((box[1] + box[3]) / 2)
                center_y = int((box[0] + box[2]) / 2)
                centers.append((center_x, center_y))
                # cv2.rectangle(frame, (box[1], box[0]), (box[3], box[2]), (0, 255, 0), 2)
                # cv2.circle(frame, (center_x + 10, center_y + 10), 4, (0, 0, 255), -1)

        disappear_flag, disappearedID, objects = ct.update(rects)
        if disappear_flag == True:
            print("---------------------------------------------")

            now_time = time.time()

            del_objectIDs = []

            for (objectID, entrance_time) in entrance_time_db.items():
                if now_time - entrance_time > DUPLICATED_TIME:
                    try:
                        del ten_min_face_db[objectID]
                        del_objectIDs.append(objectID)
                        
                    except KeyError:
                        print("Can't delete element not found")

            for objectID in del_objectIDs:
                try:
                    del entrance_time_db[objectID]
                except KeyError:
                    print("Can't delete element not found")


            print(disappear_flag)        
            print(disappearedID)
            # print(len(objectID_faces[disappearedID]))
            for eID in disappearedID:
                matching_flag = False
                for (objectID, face_list) in ten_min_face_db.items():                    
                    matching_flag = is_match(face_list, objectID_faces[eID])
                    if matching_flag == True:
                        break

                print("Matching Flag------------------------------------------")
                print(matching_flag)
                if matching_flag == True:
                    continue

                ave_score = sum(objectID_scores[eID]) / len(objectID_scores[eID])
                if ave_score < TH_AVE_FACE_SCORE:
                    continue

                if objectID_cnt[eID] < 2:
                    continue


                eID_centroids = objectID_centroids[eID]

                non_face = 0
                for e_cen in eID_centroids:
                    if e_cen[0] < NON_FACE_AREA_X and e_cen[1] < NON_FACE_AREA_X:
                        non_face = non_face + 1

                if objectID_cnt[eID] - non_face < 2:
                    continue

                sy = eID_centroids[0][1]
                ey = eID_centroids[-1][1]

                print(str(eID) + " STARTS " + str(sy) + " ENDS " + str(ey))
                try:
                    del objectID_centroids[eID]
                except KeyError:
                    print("Can't delete element not found")

                if ey <= sy:                
                    continue

                else:
                    TOTAL_COUNT = TOTAL_COUNT + 1
                    add_person = {eID:objectID_faces[eID]}
                    ten_min_face_db.update(add_person)

                    add_entrance_time = {eID:time.time()}
                    entrance_time_db.update(add_entrance_time)
                    # print(entrance_time_db)

                    # print(type(ten_min_face_db[eID]))
                    # print(type(ten_min_face_db[eID][eID]))

                    # tmp_img_path = "camera25_face_" + str(eID) + ".jpg"                    

                    str_time = datetime.now().strftime('%Y%m%d_%H%M%S%f')[:-3]

                    tmp_img_path = "Name_" + str(StoreID) + "_" + str(CameraID) + "_" + str_time + ".jpg"
                    
                    # print(ten_min_face_db[eID][0].shape)
                    cv2.imwrite(tmp_img_path, saving_faces[eID])                   

                    time.sleep(0.03)

                    files = {'media': open(tmp_img_path, 'rb')}
                    print("uploadimage")
                    r = webAPI.uploadimage(files)
                    print(r)
                    print(r.json())
                    time.sleep(0.03)

                    # savevisitorinfo_data = {
                    #   "ClientCode":"VisTest",
                    #   "CompanyID":"2",
                    #   "StoreID":"1",
                    #   "Visits":[
                    #       {
                    #           "NoOfPeople":"1",
                    #           "UPS":"1",
                    #           "VisitDateTime":"9/03/2016 15:24:21 PM",
                    #           "Visitors":[
                    #               {
                    #                   "MinAge":"14",
                    #                   "MaxAge":"25",
                    #                   "Gender":"F",
                    #                   "ActVisitorDateTime":"9/03/2016 15:24:21 PM",
                    #                   "Picture":"face_0.jpg",
                    #                   "Name":"test",
                    #                   "Accuracy":"99.0",
                    #                   "PicQuality":"G"
                    #               }
                    #           ]
                    #       }
                    #   ]
                    # }

                    # print("savevisitorinfo")
                    # r = savevisitorinfo(savevisitorinfo_data)
                    # print(r)
                    # print(r.json())

                    str_time = (datetime.now()).strftime("%m/%d/%Y, %I:%M:%S %p")

                    UPS_People_No = UPS_People_No + 1                    
                    
                    if UPS_People_No == 1:                        
                        savevisitorinfo_data_visits = {}                        
                        savevisitorinfo_data_visits["UPS"] = "1"
                        savevisitorinfo_data_visits["VisitDateTime"] = str_time

                    savevisitorinfo_data_visits["NoOfPeople"] = str(UPS_People_No)


                    min_age = objectID_minages[eID]
                    max_age = objectID_maxages[eID]
                    gender = objectID_genders[eID]                    
                    visitor_name = " "
                    accuracy = "{0:.2f}".format(objectID_accuracys[eID])
                    pic_quality = "G"
                    if objectID_accuracys[eID] < IMAGE_QUALITY_CRITERIA:
                        pic_quality = "B"


                    visits_visitors = {}
                    visits_visitors["MinAge"] = str(min_age)
                    visits_visitors["MaxAge"] = str(max_age)
                    visits_visitors["Gender"] = gender
                    visits_visitors["ActVisitorDateTime"] = str_time
                    visits_visitors["Picture"] = tmp_img_path
                    visits_visitors["Name"] = visitor_name
                    visits_visitors["CameraID"] = str(CameraID)
                    visits_visitors["Accuracy"] = accuracy
                    visits_visitors["PicQuality"] = pic_quality

                    visitors.append(visits_visitors)

                    savevisitorinfo_data_visits["Visitors"] = visitors

                    visits = []
                    visits.append(savevisitorinfo_data_visits)
                    savevisitorinfo_data["Visits"] = visits

                    last_people_time = time.time()

                    # print("savevisitorinfo")
                    # print(savevisitorinfo_data)
                    # r = webAPI.savevisitorinfo(savevisitorinfo_data)
                    # print(r)
                    # print(r.json())

                    # updatevisitorinfo_data = {
                    #     "ClientCode":"VisTest"
                    #     "CompanyID":"2",
                    #     "StoreID":"1",
                    #     "Visitors":[
                    #         {
                    #             "ID":"19780",
                    #             "VisitType":""
                    #         },
                    #         {
                    #             "ID":"19781",
                    #             "VisitType":"R"
                    #         },
                    #         {
                    #             "ID":"19782",
                    #             "VisitType":"R"
                    #         }
                    #     ]
                    # }

                    # response = webAPI.updatevisitorinfo(updatevisitorinfo_data)
                    # print(response)
                    # print(response.json())


            # print(ten_min_face_db)          


        for i in range(len(face_boxes)):
            face_name = ".jpg"
            for (objectID, centroid) in objects.items():
                dx = centers[i][0] - centroid[0]
                dy = centers[i][1] - centroid[1]
                d_dist = pow(dx * dx + dy * dy, 0.5)

                if d_dist < 1:
                    lx = 0 if rects[i][0] <= 30 else rects[i][0] - 30
                    rx = w_cols if rects[i][2] + 30 > w_cols else rects[i][2] + 30
                    ty = 0 if rects[i][1] <= 30 else rects[i][1] - 30
                    by = h_rows if rects[i][3] + 30 > h_rows else rects[i][3] + 30

                    show_cropped_face = np.zeros((by-ty, rx-lx, 3), dtype=np.uint8)
                    show_cropped_face[:,:,:] = t_frame[ty:by, lx:rx, :]
                    
                    cropped_face = t_frame[rects[i][1]:rects[i][3], rects[i][0]:rects[i][2], :]
                    cropped_face = cv2.cvtColor(cropped_face, cv2.COLOR_BGR2GRAY)
                    rows = rects[i][3] - rects[i][1]
                    cols = rects[i][2] - rects[i][0]
                    cropped_face = cv2.resize(cropped_face, (0,0), fx=COLS/cols, fy=ROWS/rows)

                    if objectID in objectID_cnt:
                        objectID_cnt[objectID] = objectID_cnt[objectID] + 1
                        t_faces = objectID_faces[objectID]
                        t_faces.append(cropped_face)
                        t_dict = {objectID:t_faces}
                        objectID_faces.update(t_dict)

                        t_centroids = objectID_centroids[objectID]
                        t_centroids.append((centroid[0], centroid[1]))
                        t_cdict = {objectID:t_centroids}
                        objectID_centroids.update(t_cdict)

                        t_scores = objectID_scores[objectID]
                        t_scores.append(face_scores[i])
                        t_dict = {objectID:t_scores}
                        objectID_scores.update(t_dict)

                        # if objectID_accuracys[objectID] < face_scores[i]:
                        #     objectID_accuracys[objectID] = face_scores[i]
                        #     saving_faces[objectID] = show_cropped_face

                        if objectID_Y[objectID] < centroid[1]:
                            objectID_accuracys[objectID] = face_scores[i]
                            saving_faces[objectID] = show_cropped_face
                            objectID_Y[objectID] = centroid[1]


                    else:
                        objectID_cnt[objectID] = 1
                        objectID_faces[objectID] = [cropped_face]
                        objectID_scores[objectID] = [face_scores[i]]
                        objectID_centroids[objectID] = [(centroid[0], centroid[1])]
                        objectID_minages[objectID] = face_ages[i][0]
                        objectID_maxages[objectID] = face_ages[i][1]
                        objectID_genders[objectID] = face_genders[i]
                        objectID_accuracys[objectID] = face_scores[i]
                        saving_faces[objectID] = show_cropped_face
                        objectID_Y[objectID] = centroid[1]
                        # objectID_faces[objectID].append(cropped_face)

                    face_name = str(objectID) + "_" + str(objectID_cnt[objectID]) + face_name

                    
                    # cv2.imwrite(face_name, cropped_face)

                    break

        for i in range(len(face_boxes)):
            box = face_boxes[i]
            cv2.rectangle(showing_frame, (int(box[1]*FRAME_RATE), int(box[0]*FRAME_RATE)), (int(box[3]*FRAME_RATE), int(box[2]*FRAME_RATE)), (0, 255, 0), 2)
                

        # loop over the tracked objects
        for (objectID, centroid) in objects.items():
            # draw both the ID of the object and the centroid of the
            # object on the output frame
            text = "ID {}".format(objectID)
            cv2.putText(showing_frame, text, (int(centroid[0]*FRAME_RATE) - 10, int(centroid[1]*FRAME_RATE) - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.circle(showing_frame, (int(centroid[0]*FRAME_RATE), int(centroid[1]*FRAME_RATE)), 4, (0, 255, 0), -1)

        # sec = curTime - prevTime
        # prevTime = curTime
        # fps = 1 / (sec)
        cnt_str = 'COUNT: %d' % TOTAL_COUNT
        text_fps_x = len(showing_frame[0]) - 150        
        text_fps_y = 40
        cv2.putText(showing_frame, cnt_str, (text_fps_x, text_fps_y),
                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 0), thickness=2, lineType=2)


        
        # show_H, show_W, dummy = showing_frame.shape
        # print(show_W)
        # sW = int(show_W * 4 / 17)
        # eW = int(show_W * 13 / 17)
        # cv2.rectangle(showing_frame, (sW, 0), (eW, show_H), (0,255,0), 2)
        cv2.imshow('Video', showing_frame)

        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
