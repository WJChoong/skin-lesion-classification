import os
from PIL import Image
import imagehash

def list_overlapping_images(dir1, dir2):
    # Create hashes for all images in the first directory
    hashes_dir1 = {}
    for filename in os.listdir(dir1):
        if filename.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            path = os.path.join(dir1, filename)
            image = Image.open(path)
            image_hash = imagehash.average_hash(image)
            hashes_dir1[image_hash] = filename

    # Compare images in the second directory with the first
    overlapping_images = []
    for filename in os.listdir(dir2):
        if filename.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            path = os.path.join(dir2, filename)
            image = Image.open(path)
            image_hash = imagehash.average_hash(image)

            if image_hash in hashes_dir1:
                overlapping_images.append((hashes_dir1[image_hash], filename))

    return overlapping_images

# Example usage
dir1 = 'path/to/first/directory'
dir2 = 'path/to/second/directory'
overlaps = list_overlapping_images(dir1, dir2)
print("Overlapping images:", overlaps)