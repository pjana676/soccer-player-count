import cv2
import numpy as np
import os
import sys

def count_people(image_data):
    net = cv2.dnn.readNet(
        "/app/darknet/yolov3.weights",
        "/app/darknet/cfg/yolov3.cfg"
    )
    classes = []
    with open("/app/darknet/data/coco.names", 'r') as f:
        classes = [line.strip() for line in f.readlines()]

    nparr = np.fromstring(image_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    height, width, _ = img.shape

    blob = cv2.dnn.blobFromImage(img, scalefactor=1/255.0, size=(416, 416), swapRB=True, crop=False)


    net.setInput(blob)
    
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

    detections = net.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []

    for out in detections:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5 and classes[class_id] == 'person':
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                x2 = x + w
                y2 = y + h

                boxes.append([x, y, x2, y2])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    num_people = len(indexes)

    return num_people