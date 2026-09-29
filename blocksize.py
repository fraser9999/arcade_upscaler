from scipy.ndimage import label, find_objects
import cv2

from distances import get_distance


# Bild binarisieren (Schwarz-Weiß)
def find_block(image_path, max_block_size=64):


    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

    # Zusammenhängende Blöcke markieren
    labeled_array, num_features = label(thresh)
    bounding_boxes = find_objects(labeled_array)


    dist=[]

    # Koordinaten auslesen
    for box in bounding_boxes:
        if box is not None:
            y_slice, x_slice = box
            #print(f"Block von Pixel X({x_slice.start} bis {x_slice.stop}) und Y({y_slice.start} bis {y_slice.stop})")

            x = x_slice.stop - x_slice.start
            y = y_slice.stop - y_slice.start
            #print(str(x),str(y)) 

            dist.extend([x,y])

    return dist
 

def find_block_size(image_path, max_block_size=64):

    dist = find_block(image_path,64)
    distanz = get_distance(dist,1,2)

    return distanz


