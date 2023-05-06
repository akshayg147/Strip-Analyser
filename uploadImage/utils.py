import cv2
import numpy as np
import json

class NumpyEncoder(json.JSONEncoder):
    '''
    Encoder that can handle JSON serialization of numpy.ndarray and numpy.integer types.
    '''
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.integer):
            return int(obj)
        return json.JSONEncoder.default(self, obj)

def process_image(image_path):
    # Load the image and convert it to grayscale
    strip = cv2.imdecode(np.frombuffer(image_path, np.uint8), cv2.IMREAD_UNCHANGED)

    # Convert the strip to grayscale
    gray_strip = cv2.cvtColor(strip, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to the grayscale image to binarize it
    _, thresh_strip = cv2.threshold(gray_strip, 110, 95, cv2.THRESH_BINARY_INV)

    # Find the contours in the thresholded image
    contours, _ = cv2.findContours(thresh_strip, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Loop through the contours and filter out small ones (noise) and large ones (the strip itself)
    for contour in contours:
        area = cv2.contourArea(contour)
        if area < 0 or area > 100000000:
            continue

        # Get the bounding box of the contour
        x, y, w, h = cv2.boundingRect(contour)

        # Draw a rectangle around the contour (for visualization)
        cv2.rectangle(strip, (x, y), (x + w, y + h), (0, 0, 255), 2)
        roi = strip[y:y + h, x:x + w]

    # Display the image
    img = roi
    cv2.imshow('image', img)
    cv2.waitKey(0)
    # Define the number of color blocks on the strip and the block size
    num_blocks = 10
    block_width = 70
    block_height = 70

    # Generate block coordinates
    xs = np.zeros(num_blocks, dtype=int) + img.shape[1] - block_width
    ys = np.linspace(24, (num_blocks - 1) * block_height, num_blocks, dtype=int)
    block_coords = zip(xs, ys)

    # List to store the RGB values of each block
    colors = {}

    # list of things to be detected
    testElement = ['URO', 'BIL', 'KET', 'BLD', 'PRO', 'NIT', 'LEU', 'GLU', 'SG', 'PH']
    # Loop over each block
    for i, (x, y) in enumerate(block_coords):
        # Crop the block using its coordinates
        block = img[y:y + block_height, x:x + block_width]

        # Calculate the RGB value of the block as the mean value
        color_value = np.mean(block, axis=(0, 1)).astype(int)

        # Add the RGB value of the block to the list
        # colors.append(tuple(color_value))
        colors[testElement[i]] = list(color_value)
    return json.dumps(colors, cls=NumpyEncoder)
