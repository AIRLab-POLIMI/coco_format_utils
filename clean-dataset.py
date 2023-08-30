import json
import re

annotation_filename = 'valid_annotations.coco.json'

# Load the merged COCO dataset JSON file
with open(annotation_filename, 'r') as f:
    coco_data = json.load(f)

# Update the paths and filenames in the image entries
for image_info in coco_data['images']:
    original_filename = image_info['file_name']
    new_filename = re.sub(r'_png\.rf\.[a-f0-9]+\.jpg$', '.png', original_filename)
    image_info['file_name'] = new_filename

# Save the updated JSON back to the file
with open(annotation_filename, 'w') as f:
    json.dump(coco_data, f)

