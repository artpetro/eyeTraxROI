import os

anno_path = 'E:/frames_10_bins/annotations.txt'
filtered_anno_path = 'E:/frames_10_bins/annotations_filtered.txt'
readed_anno = []
filtered_anno = []

#read annotations
with open(anno_path, 'r') as annotations:
    readed_anno = annotations.readlines()
    
#filter
for anno in readed_anno:
    if os.path.isfile(anno.split()[0]):
        filtered_anno.append(anno)

print(f'readed {len(readed_anno)}')
print(f'filtered {len(filtered_anno)}')

#write annotations
with open(filtered_anno_path, "a") as ann_file:
    for anno in filtered_anno:
        ann_file.write(anno)