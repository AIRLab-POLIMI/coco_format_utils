import os
import json
import random
import math
import shutil
import zipfile
from pycocotools.coco import COCO

def split_coco_dataset(ann_file, image_dir, num_splits):
    # Load COCO annotations
    coco = COCO(ann_file)
    
    # Get list of image IDs
    image_ids = list(coco.imgs.keys())
    
    # Shuffle the image IDs randomly
    random.shuffle(image_ids)
    
    # Calculate the number of images per split
    images_per_split = math.ceil(len(image_ids) / num_splits)
    
    for split_idx in range(num_splits):
        # Create a new COCO-style dictionary for the split
        split_data = {
            #"info": coco.dataset["info"],
            #"licenses": coco.dataset["licenses"],
            "categories": coco.dataset["categories"],
            "images": [],
            "annotations": []
        }
        
        # Create a directory for split images
        split_image_dir = os.path.join(image_dir, f'split_{split_idx}')
        os.makedirs(split_image_dir, exist_ok=True)
        
        # Add images and annotations to the split data
        images_in_split = image_ids[split_idx * images_per_split : (split_idx + 1) * images_per_split]
        for img_id in images_in_split:
            split_data["images"].append(coco.imgs[img_id])
            annotations = coco.imgToAnns[img_id]
            
            image_path = os.path.join(image_dir,coco.imgs[img_id]["file_name"])
            shutil.copy(image_path, split_image_dir)
            
            for ann in annotations:
                split_data["annotations"].append(ann)
                
        # Update image paths in the split data
        for img_info in split_data["images"]:
            img_info["file_name"] = os.path.join(f'split_{split_idx}', img_info["file_name"])
        
        # Save split data to a JSON file
        split_ann_file =  os.path.join(image_dir,f'annotations_split_{split_idx}.json')
        with open(split_ann_file, 'w') as f:
            json.dump(split_data, f) 

    
    print(f"Dataset split into {num_splits} subsets.")


if __name__ == "__main__":
    annotation_file = "./subset/subset_dataset.coco.json"
    image_directory = "./subset/"
    num_splits = 4  # Change this to the desired number of splits
    
    split_coco_dataset(annotation_file, image_directory, num_splits)

