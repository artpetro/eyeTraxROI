'''
Created on 03.11.2020
Extend annotations file with iris ROIs data
@author: artpetro
'''
import os
import glob
import csv
import cv2

shuffled_anno_path = 'E:/frames_10_bins/annotations_shuffled.txt'
extended_anno_path = 'E:/frames_10_bins/annotations_extended.txt'
iris_anno_path = 'E:/frames_10_bins/annotations_only_iris.txt'

shuffled_anno = []
extended_anno = []
iris_anno = []
measurements = {}

def draw_roi_and_ellipse(path, roi, pupil_ellipse):
    image = cv2.imread(path) 
    window_name = 'Image'
  
    #roi
    start_point = (roi[0], roi[1]) 
    end_point = (roi[2], roi[3]) 
    color = (255, 0, 0) 
    thickness = 1
    image = cv2.rectangle(image, start_point, end_point, color, thickness) 
    
    #ellipse
    center_coordinates = (int(pupil_ellipse[0]), int(pupil_ellipse[1])) 
    axesLength = (int(pupil_ellipse[2]), int(pupil_ellipse[3])) 
    angle = pupil_ellipse[4]
    startAngle = 0
    endAngle = 360
       
    color = (0, 0, 255)
    thickness = 1

    image = cv2.ellipse(image, center_coordinates, axesLength, 
               angle, startAngle, endAngle, color, thickness)
    
    cv2.imshow(window_name, image)
    key = cv2.waitKey(0)
    print(key)
    
    return key
    
     

def read_pupil_data(path):
    pupil_data = {}
    with open(path) as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        for row in reader:
            pupil_data[row[0]] = row[1:]
        
        return pupil_data

def get_pupil_data(path):
    measurement_id = os.path.splitext(path)[0]
    if measurements.get(measurement_id) is None:
        measurements[measurement_id] = read_pupil_data(path)
        
    return measurements.get(measurement_id)

def get_pupil_roi(path, pupil_coords_rel):
    
    height, width, _  = cv2.imread(path).shape
    pupil_centre_x = float(pupil_coords_rel[0]) * width
    pupil_centre_y = float(pupil_coords_rel[1]) * height
    
    roi_half_size = width / 5
    
    x_min = pupil_centre_x - roi_half_size
    y_min = pupil_centre_y - roi_half_size
    x_max = pupil_centre_x + roi_half_size
    y_max = pupil_centre_y + roi_half_size
    
    x_min = max(0, x_min)
    y_min = max(0, y_min)
    x_max = min(width, x_max)
    y_max = min(height, y_max)
    
    return int(x_min), int(y_min), int(x_max), int(y_max)


def get_pupil_ellipse(path, pupil_coords_rel):
    height, width, _  = cv2.imread(path).shape
    pupil_centre_x = float(pupil_coords_rel[0]) * width
    pupil_centre_y = float(pupil_coords_rel[1]) * height
    #print(pupil_coords_rel)
    pupil_x_axis = float(pupil_coords_rel[2]) * max(width, height)
    pupil_y_axis = float(pupil_coords_rel[3]) * max(width, height)
    
    pupil_angle = float(pupil_coords_rel[4])
    
    return pupil_centre_x, pupil_centre_y, pupil_x_axis, pupil_y_axis, pupil_angle
    
  
def write_annotations(anno_path, annotations):
    with open(anno_path, "a") as ann_file:
        for anno in annotations:
            ann_file.write(anno)
            pass

'''
def repair_annotations():
    repaired_anno_path = 'E:/frames_10_bins/annotations_repaired_iris.txt'
    repaired_anno = []
    
    with open(iris_anno_path, 'r') as annotations:
        corrupted_anno = annotations.readlines() 
    
    for corr_ann in corrupted_anno:
        frame_path, _ = corr_ann.split()
        frame_dir, frame_id = os.path.split(frame_path)
        os.chdir(frame_dir)
        pupil_data_file = glob.glob("*.tsv")[0]
        
        pupil_data = get_pupil_data(pupil_data_file)
        pupil_coords_rel = pupil_data.get(frame_id)
        
        print(frame_path)
        if pupil_coords_rel is not None:
            roi = get_pupil_roi(frame_path, pupil_coords_rel)
            pupil_ellipse = get_pupil_ellipse(frame_path, pupil_coords_rel)   
            repaired_anno.append(f"{corr_ann.split()[0]} {roi[0]},{roi[1]},{roi[2]},{roi[3]},0\n")
            
    write_annotations(repaired_anno_path, repaired_anno)

repair_annotations()
'''



# CREATE ANNOTATIONS MANUALLY

#read annotations
with open(shuffled_anno_path, 'r') as annotations:
    shuffled_anno = annotations.readlines() 
    
#for anno in shuffled_anno:
for i in range(4088, len(shuffled_anno)):
    anno = shuffled_anno[i]
    frame_path, _ = anno.split()
    frame_dir, frame_id = os.path.split(frame_path)
    os.chdir(frame_dir)
    pupil_data_file = glob.glob("*.tsv")[0]
    
    pupil_data = get_pupil_data(pupil_data_file)
    pupil_coords_rel = pupil_data.get(frame_id)
    
    if pupil_coords_rel is not None:
        roi = get_pupil_roi(frame_path, pupil_coords_rel)
        pupil_ellipse = get_pupil_ellipse(frame_path, pupil_coords_rel)
        key = draw_roi_and_ellipse(frame_path, roi, pupil_ellipse)
        #extend anno
        anno = f"{anno.rstrip()} {roi[0]},{roi[1]},{roi[2]},{roi[3]},1\n"
        #space
        if key == 32:
            iris_anno.append(f"{anno.split()[0]} {roi[0]},{roi[1]},{roi[2]},{roi[3]},0\n")
            print(f"{anno.split()[0]} {roi[0]},{roi[1]},{roi[2]},{roi[3]},0")
            print(f"total: {len(iris_anno)}")
        elif key == 27:
            break
    extended_anno.append(anno)

#TODO uncomment
#write_annotations(extended_anno_path, extended_anno)
write_annotations(iris_anno_path, iris_anno)

        