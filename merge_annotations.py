import json

def adjust_ids(annotation_data, start_id):
    id_mapping = {}
    
    for image in annotation_data['images']:
        new_id = start_id + image['id']
        id_mapping[image['id']] = new_id
        image['id'] = new_id
        
    for annotation in annotation_data['annotations']:
        annotation['image_id'] = id_mapping[annotation['image_id']]
        
    return annotation_data, start_id + len(annotation_data['images'])

def renumber_image_ids(annotation_data):
    id_mapping = {}
    for idx, image in enumerate(annotation_data['images']):
        id_mapping[image['id']] = idx
        image['id'] = idx
    for annotation in annotation_data['annotations']:
        annotation['image_id'] = id_mapping[annotation['image_id']]
        
    return annotation_data

def merge_annotations(annotation_files):
    merged_data = {
        'info': [],
        'licenses': [],
        'images': [],
        'annotations': [],
        'categories': []
    }
    
    new_id = 0
    category_mapping = {}  # Map category name to new ID
    next_category_id = 0
    
    for file_path in annotation_files:
        with open(file_path, 'r') as f:
            annotation_data = json.load(f)
            adjusted_data, new_id = adjust_ids(annotation_data, new_id)
            
            for category in adjusted_data['categories']:
                if category['name'] not in category_mapping:
                    category_mapping[category['name']] = next_category_id
                    new_category = {
                        'id': next_category_id,
                        'name': category['name'],
                        'supercategory': category['supercategory']
                    }
                    merged_data['categories'].append(new_category)
                    next_category_id += 1
                    
            for key in merged_data.keys():
                if key != 'categories':
                    merged_data[key].extend(adjusted_data[key])
    
    return merged_data

annotation_files = ['test_annotations.coco.json', 'train_annotations.coco.json', 'valid_annotations.coco.json']
merged_annotation_data = merge_annotations(annotation_files)
merged_annotation_data = renumber_image_ids(merged_annotation_data)

output_file = 'merged_annotations.coco.json'
with open(output_file, 'w') as f:
    json.dump(merged_annotation_data, f)

