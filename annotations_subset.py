import random

SEED = 42
random.seed(SEED)

filtered_anno_path = 'E:/frames_10_bins/annotations_filtered.txt'
shuffled_anno_path = 'E:/frames_10_bins/annotations_shuffled.txt'
filtered_anno = []

#read annotations
with open(filtered_anno_path, 'r') as annotations:
    filtered_anno = annotations.readlines()
    
random.shuffle(filtered_anno)

with open(shuffled_anno_path, "a") as ann_file:
    for anno in filtered_anno:
        ann_file.write(anno)