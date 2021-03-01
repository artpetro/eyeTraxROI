import os
import sqlite3
import cv2
import frame_extractor as fe

root_dir = 'E:'
base_dir = 'JanStudie'
db_filename = 'JanStudieKomplett.eyetrax_db'
frames_dir = "frames_10"


def read_rois_from_db(root_dir, base_dir, db_filename):
    conn = sqlite3.connect(os.path.join(root_dir, base_dir, db_filename))
    cursor = conn.cursor()
    
    cursor.execute('SELECT storage_path, ROI_0_X, ROI_0_Y, ROI_0_W, ROI_0_H, ROI_1_X, ROI_1_Y, ROI_1_W, ROI_1_H FROM data')
    
    rois = []
    
    for row in cursor.fetchall():
        if row[0] is not None:
            old_path = os.path.abspath(row[0])
            act_path = os.path.abspath(old_path.replace(old_path[:old_path.index(base_dir)], root_dir))
            measurement_dir = os.path.dirname(act_path)
            roi = [measurement_dir]
            roi.extend(row[1:])
            rois.append(roi)
    
    return rois

def play_video(roi_data):
    head, measurement_id = os.path.split(roi_data[0])
    cap = cv2.VideoCapture(os.path.join(roi_data[0], measurement_id, '000\eye1.mp4'))

    while(cap.isOpened()):
        ret, frame = cap.read()
    
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #cv2.rectangle(frame, (roi_data[1], roi_data[2]), (roi_data[3], roi_data[4]),(0,255,0),1)
        cv2.rectangle(frame, (roi_data[5], roi_data[6]), (roi_data[7], roi_data[8]),(0,255,0),1)
    
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    

def write_annotation_file(roi, annotations_file):
    annotation_path = os.path.join(root_dir, frames_dir, annotations_file)
    head, measurement_id = os.path.split(roi[0])
    dst_dir = head.replace(base_dir, frames_dir)
    
    # eye0 == rightEye ROI_0
    # eye1 == leftEye ROI_1
    for eye in ["LeftEye", "RightEye"]:
        eye_dir = os.path.join(dst_dir, measurement_id, eye)
        frames = []
        # r=root, d=directories, f = files
        for r, d, f in os.walk(eye_dir):
            for file in f:
                if '.png' in file:
                    frames.append(os.path.join(r, file))
        
        #ROI_0
        x1, y1, x2, y2 = roi[1], roi[2], roi[3], roi[4]
        #ROI_1
        if eye == 'LeftEye':
            x1, y1, x2, y2 = roi[5], roi[6], roi[7], roi[8]
            
        roi_coords = f"{x1},{y1},{x2},{y2},0"
        
        with open(annotation_path, "a") as ann_file:
            for frame in frames:
                ann_file.write(f"{frame} {roi_coords}\n")



def extract_frames(roi, bins):
    measurement_dir = roi[0]
    head, measurement_id = os.path.split(measurement_dir)
    dst_dir = head.replace(base_dir, frames_dir)
    measurement_path = os.path.join(measurement_dir, measurement_id + ".eyetrax")
    if os.path.isdir(os.path.join(measurement_dir, measurement_id)):
        fe.extractAllFrames(measurement_path, dst_dir, bins, ignore=True)
        return True
    
    return False
    
bins = 10
rois = read_rois_from_db(root_dir, base_dir, db_filename)
    
#play_video(rois[50])

annotations_file = "annotations.txt"
for roi in rois:
    extract_frames(roi, bins)
    write_annotation_file(roi, annotations_file)

# count valide measurements
#valide_videos_count = 0
#for roi in rois:
#    if extract_frames(roi, bins):
#        valide_videos_count += 1       
#print(f'valide videos {valide_videos_count}')
