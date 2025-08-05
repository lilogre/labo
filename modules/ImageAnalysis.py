import cv2
import numpy as np
import matplotlib.pyplot as plt
import logging
from modules.OutputData import plt2npa
from modules.OutputData import OutputImageData

logger = logging.getLogger(__name__)

def AnalyzeColor(data_dir, img, x1, y1, x2, y2):
    # Load the image
    try:
        image_bgr = cv2.imread(img)
        if image_bgr is None:
            raise Exception(f"can't open/read file: {img}")
    except Exception as e:
        logger.error(f"Error loading image: {e}")
        raise Exception("AnalyzeColor failed")
    else:
        logger.info(f"Image loaded successfully from {img}")
    
    # Cut out region（ROI: Region of Interest）
    try:
        roi_bgr = image_bgr[y1:y2, x1:x2]
        if roi_bgr.size == 0:
            raise ValueError("The selected area is outside the image or is invalid.")
    except ValueError as e:
        logger.error(f"ROI: {e}")
        raise Exception("AnalyzeColor failed")
    else:
        logger.info(f"Region Of Interest selected at ({x1}, {y1})x({x2}, {y2})")
    
    roi_hsv = cv2.cvtColor(roi_bgr, cv2.COLOR_BGR2HSV)

    # Display ROI on the image (for confirmation)
    cv2.rectangle(image_bgr, (x1, y1), (x2, y2), (0, 0, 255), 5)
    plt.figure(figsize=(10, 8))
    plt.imshow(cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB))
    plt.title("Measurement area (red frame)")
    plt.axis('on')
    img_conf = plt2npa(plt)
    plt.close()

    # Calculate average BGR and HSV values of ROI
    mean_bgr = cv2.mean(roi_bgr)[:3]
    mean_hsv = cv2.mean(roi_hsv)[:3]
    
    # Calculate the histogram
    h_hist = cv2.calcHist([roi_hsv], [0], None, [180], [0, 180]) # Hue has 180 bins
    s_hist = cv2.calcHist([roi_hsv], [1], None, [256], [0, 256])
    v_hist = cv2.calcHist([roi_hsv], [2], None, [256], [0, 256])
    # Plot histogram
    fig, axs = plt.subplots(3, 1, figsize=(10, 8))
    axs[0].plot(h_hist, color='red')
    axs[0].set_title('Hue histogram')
    axs[0].set_xlim([0, 180])
    axs[1].plot(s_hist, color='green')
    axs[1].set_title('Saturation histogram')
    axs[1].set_xlim([0, 256])
    axs[2].plot(v_hist, color='blue')
    axs[2].set_title('Value (Brightness) histogram')
    axs[2].set_xlim([0, 256])
    plt.tight_layout()
    img_hist = plt2npa(fig)
    plt.close()

    # Color square with average color of ROI
    img_blob = np.zeros((100,100,3), np.uint8) # blank image
    cv2.rectangle(img_blob, (0, 0), (100, 100), mean_bgr, -1) # fill with mean color

    OutputImageData(data_dir, mean_bgr[::-1], mean_hsv, img_conf, img_hist, cv2.cvtColor(img_blob, cv2.COLOR_BGR2RGB))