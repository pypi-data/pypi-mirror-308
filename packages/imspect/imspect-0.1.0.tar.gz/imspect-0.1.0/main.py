import pdb

import cv2


def main():
    img1 = cv2.imread("poop.png")
    img2 = cv2.imread("cake.png")

    h,w,c = img2.shape
    img2 = img2[:round(0.6 * h):, round(0.2 * w):round(0.8 * w)]

    breakpoint()  # activate debugger here

    print(img2.shape)

    return img1, img2

if __name__ == "__main__":
#     main()
    from imspect import imspect
    import numpy as np

    # examples of acceptable images
    img1 = np.empty((60, 100, 3), dtype=np.uint8)
    img2 = np.zeros((60, 100), dtype=np.uint8) + 255

    imspect(img1 , img2)