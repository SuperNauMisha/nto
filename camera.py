import cv2
import cv2.aruco as aruco
import numpy as np

cap = cv2.VideoCapture(0)
work_zone1 = (200, 0)
work_zone2 = (1050, 800)
keep_area = (0, 0, 0)
load_area = (105, 236, 226)
unload_area = (170, 130, 210)
dh, ds, dv = 45, 33, 47

def calculate_angle(corners):
    # Углы маркера: [top-left, top-right, bottom-right, bottom-left]
    top_left = corners[0][0]
    top_right = corners[0][1]

    vector = top_right - top_left
    angle_rad = np.arctan2(vector[1], vector[0])
    angle_deg = np.degrees(angle_rad)
    return angle_deg


def findAruco(img, draw=True):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    arucoDict = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)  # Используем новый метод
    arucoParam = aruco.DetectorParameters()
    detector = aruco.ArucoDetector(arucoDict, arucoParam)  # Создаём детектор
    bbox, ids, _ = detector.detectMarkers(gray)  # Используем детектор
    if ids is not None and draw:
        for i, marker_id in enumerate(ids):
            color = (0, 255, 0)
            if marker_id == 9 or marker_id == 10:
                color = (255, 0, 0)
            corners = bbox[i].astype(int)
            angle = calculate_angle(corners)
            cv2.polylines(img, [corners], isClosed=True, color=color, thickness=2)
            cv2.putText(img, f"{marker_id[0]} Ang: {angle:.1f}", tuple(corners[0][0]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (120, 0, 255), 1)
    return bbox, ids


def click(event, x, y, flags, param):
    global keep_area, load_area, unload_area
    if event == cv2.EVENT_RBUTTONDOWN:
        keep_area = hsv[y][x]
        print(keep_area)
    if event == cv2.EVENT_MBUTTONDOWN:
        load_area = hsv[y][x]
        print(load_area)
    if event == cv2.EVENT_LBUTTONDOWN:
        unload_area = hsv[y][x]
        print(unload_area)



def draw_contours(image, mask, color=(0, 255, 0), thickness=2):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        cv2.drawContours(image, [contour], -1, color, thickness)


def hue_dh_trackbar(val):
    global dh
    dh = val
def hue_ds_trackbar(val):
    global ds
    ds = val
def hue_dv_trackbar(val):
    global dv
    dv = val


cv2.namedWindow("Trackbars")
cv2.createTrackbar("dh", "Trackbars", dh, 255, hue_dh_trackbar)
cv2.createTrackbar("ds", "Trackbars", ds, 255, hue_ds_trackbar)
cv2.createTrackbar("dv", "Trackbars", dv, 255, hue_dv_trackbar)



cv2.namedWindow("img")
cv2.setMouseCallback("img", click)

while True:
    #_, img = cap.read()
    img = cv2.imread("new.png")[work_zone1[1]:work_zone2[1], work_zone1[0]:work_zone2[0]]
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    bbox, ids = findAruco(img)

    lowKA = np.array([max(int(keep_area[0]) - dh, 0), max(int(keep_area[1]) - ds, 0), max(int(keep_area[2]) - dv, 0)])
    highKA = np.array([min(int(keep_area[0]) + dh, 255), min(int(keep_area[1]) + ds, 255), min(int(keep_area[2]) + dv, 255)])
    keep_area_mask = cv2.inRange(hsv, lowKA, highKA)

    lowLA = np.array([max(int(load_area[0]) - dh, 0), max(int(load_area[1]) - ds, 0), max(int(load_area[2]) - dv, 0)])
    highLA = np.array([min(int(load_area[0]) + dh, 255), min(int(load_area[1]) + ds, 255), min(int(load_area[2]) + dv, 255)])

    load_area_mask = cv2.inRange(hsv, lowLA, highLA)

    lowUA = np.array([max(int(unload_area[0]) - dh, 0), max(int(unload_area[1]) - ds, 0), max(int(unload_area[2]) - dv, 0)])
    highUA = np.array(
        [min(int(unload_area[0]) + dh, 255), min(int(unload_area[1]) + ds, 255), min(int(unload_area[2]) + dv, 255)])
    unload_area_mask = cv2.inRange(hsv, lowUA, highUA)


    cv2.imshow("keep_area_mask", keep_area_mask)
    cv2.imshow("load_area_mask", load_area_mask)
    cv2.imshow("unload_area_mask", unload_area_mask)
    # load_area_mask = detect_color(hsv, lower_green, upper_green)
    # unload_area_mask = detect_color(hsv, lower_green, upper_green)

    draw_contours(img, keep_area_mask, color=(255, 0, 0), thickness=2)
    draw_contours(img, load_area_mask, color=(0, 255, 0), thickness=2)
    draw_contours(img, unload_area_mask, color=(0, 0, 255), thickness=2)

    cv2.imshow("img", img)
    if cv2.waitKey(1) == 113:
        break

cap.release()
cv2.destroyAllWindows()