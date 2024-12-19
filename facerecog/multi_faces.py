import multiprocessing
import face_recognition
import cv2
import numpy as np
import os
from collections import deque
import time

known_faces_dir = "facerecog/known_faces/"
if not os.path.exists(known_faces_dir):
    os.makedirs(known_faces_dir)

def load_known_faces():
    """Load known face encodings and names from the known_faces directory."""
    known_face_encodings = []
    known_face_names = []
    try:
        for image_name in os.listdir(known_faces_dir):
            if image_name.endswith(('jpg', 'jpeg', 'png')):
                image_path = os.path.join(known_faces_dir, image_name)
                image = face_recognition.load_image_file(image_path)
                face_encodings_in_image = face_recognition.face_encodings(image)

                if face_encodings_in_image:
                    face_encoding = face_encodings_in_image[0]
                    known_face_encodings.append(face_encoding)
                    known_face_names.append(os.path.splitext(image_name)[0])
    except Exception as e:
        print(f"Error loading known faces: {e}")
    return known_face_encodings, known_face_names

try:
    known_face_encodings, known_face_names = load_known_faces()

    net = cv2.dnn.readNet("facerecog/yolov4.weights", "facerecog/yolov4.cfg")

    with open("facerecog/coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]

    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

except Exception as e:
    print(f"Error initializing models: {e}")
    exit(1)

def capture_video():
    """Capture video from the webcam."""
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Error: Could not open webcam.")
    return cap

def detect_objects(frame):
    file_path="facerecog\sdbjects.txt"
    """Detect objects in the frame using YOLO."""
    height, width, _ = frame.shape
    blob = cv2.dnn.blobFromImage(frame, scalefactor=1/255.0, size=(416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    layer_outputs = net.forward(output_layers)

    boxes, confidences, class_ids = [], [], []

    for output in layer_outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.5:
                center_x, center_y = int(detection[0] * width), int(detection[1] * height)
                w, h = int(detection[2] * width), int(detection[3] * height)
                x, y = int(center_x - w / 2), int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indices = cv2.dnn.NMSBoxes(boxes, confidences, score_threshold=0.5, nms_threshold=0.4)

    # Print the object names
    if len(indices) > 0:
        for i in indices.flatten():
            entry = classes[class_ids[i]]
            #print(entry)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
            # Read existing entries (if any)
            if os.path.exists(file_path):
                with open(file_path, "r") as file:
                    existing_entries = [line.strip() for line in file.readlines()]
            else:
                existing_entries = []
            
            # Check if the entry already exists
            if entry not in existing_entries:
                # Write the new entry at the top, followed by the existing entries
                with open(file_path, "w") as file:
                    file.write(entry + "\n")
                    file.writelines(line + "\n" for line in existing_entries)

    return boxes, confidences, class_ids, indices

recognized_faces_queue = deque(maxlen=5)

def recognize_faces(frame):
    """Recognize faces in the frame."""
    global known_face_encodings, known_face_names
    try:
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)
        recognized_names = []

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
            recognized_faces_queue.append(name)
            recognized_names.append((name, (left, top, right, bottom)))

        with open('facerecog/currentface.txt', 'w') as file:
            for name in recognized_faces_queue:
                file.write(f"{name}\n")

        if all(name == "Unknown" for name in recognized_faces_queue):
            snapshot_filename = os.path.join(known_faces_dir, "stranger.jpg")
            cv2.imwrite(snapshot_filename, frame)
            print(f"All faces unknown. Snapshot saved as {snapshot_filename}")
            known_face_encodings, known_face_names = load_known_faces()
            recognized_faces_queue.clear()
            return snapshot_filename

        return recognized_names

    except Exception as e:
        print(f"Error in face recognition: {e}")
        return []

def save_name(a):
    current_name = 'facerecog/known_faces/stranger.jpg'
    new_name = f'facerecog/known_faces/{a}.jpg'
    try:
        if os.path.exists(current_name):
            os.rename(current_name, new_name)
            print(f"File renamed from {current_name} to {new_name}")
        known_face_encodings, known_face_names = load_known_faces()
        recognized_faces_queue.clear()
    except Exception as e:
        print(f"Error renaming file: {e}")

def main():
    print("starting multiface")
    while True:
        try:
            cap = capture_video()
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                detect_objects(frame)
                recognized_faces = recognize_faces(frame)
                if isinstance(recognized_faces, str):
                    cap.release()
                    break
            cap.release()
            cv2.destroyAllWindows()
        except Exception as e:
            print(f"Error in video processing: {e}")

if __name__ == "__main__":
    try:
        p1 = multiprocessing.Process(target=main)
        p2 = multiprocessing.Process(target=save_name, args=("Shounak",))
        p1.start()
        time.sleep(10)
        p2.start()
    except Exception as e:
        print(f"Error in multiprocessing: {e}")
