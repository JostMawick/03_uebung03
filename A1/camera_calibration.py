#!/usr/bin/env python3

import glob
import pathlib
import sys

import cv2 as cv
import numpy as np
import yaml
import matplotlib.pyplot as plt

PATTERN = (7,7) # number of checker-board corners (7x7 for 8x8 squares)
#PATTERN_WIDTH = 0.059 # pyhsical corner-distance: 59mm

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((PATTERN[0]*PATTERN[1],3), np.float32)
objp[:,:2] = np.mgrid[0:PATTERN[0],0:PATTERN[1]].T.reshape(-1,2)

#objp *= PATTERN_WIDTH

# arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

# get all images in current directory
folder = pathlib.Path(__file__).parent.resolve()
images = glob.glob(f'{folder}/*.png')

if len(images) == 0:
    print(f"Error: No calibration images found in {folder}")
    sys.exit()

# loop over all images:
for fname in images:
    print(fname)
    img = cv.imread(fname)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # find the chess board corners
    ret, corners = cv.findChessboardCorners(gray, PATTERN, None, flags=cv.CALIB_CB_ADAPTIVE_THRESH)

    if ret == True:
        print("corners found successfully")
        # refine corner positions
        #subpix_criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        #corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), subpix_criteria)

        # add object points and image points    
        objpoints.append(objp)
        imgpoints.append(corners)

        # draw and display the corners
        if True:
            cv.drawChessboardCorners(img, (7,7), corners, ret)
            plt.imshow(img)
            plt.title('detected corners')
            plt.show()
    else:
        print("Error: corners NOT found!")
        plt.imshow(img)
        plt.title('NO corners detected!!')
        plt.show()

# compute camera parameters
flags = cv.CALIB_ZERO_TANGENT_DIST | cv.CALIB_FIX_ASPECT_RATIO 
ret, camera_matrix, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],
                                                            None, None, None, None, flags)

# --- test ---
test_image = images[0]
img = cv.imread(test_image)
plt.imshow(img[:,:,::-1])
plt.title('original')
plt.show()

h, w = img.shape[:2]
#new_camera_matrix, roi = cv.getOptimalNewCameraMatrix(camera_matrix, dist, (w,h), 1, (w,h))

# undistort
img_undistorted = cv.undistort(img, camera_matrix, dist) #, None, new_camera_matrix)
plt.imshow(img_undistorted[:,:,::-1])
plt.title('undistorted')
plt.show()

# crop the image
#x, y, w, h = roi
#img_undistorted_cropped = img_undistorted[y:y+h, x:x+w]
#plt.imshow(img_undistorted_cropped)
#plt.title('undistorted and cropped')
#plt.show()

print(
    yaml.dump(
        {"intrinsic": {"matrix": camera_matrix.tolist(), "distortion": dist.tolist()[0]}},
        default_flow_style=None,
    )
)

# calculate re-projection error
mean_error = 0
for i in range(len(objpoints)):
    imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], camera_matrix, dist)
    error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2)/len(imgpoints2)
    mean_error += error
print(f"total error: {mean_error/len(objpoints)}")

# plot radial distortion function
k1 = dist[0,0]
k2 = dist[0,1]
k3 = dist[0,4]
C = camera_matrix
Cinv = np.linalg.inv(C)
u_rect_img = np.linspace(0, img.shape[1]*1.2)
v_rect_img = C[1,2]
x_rect_cam = Cinv[0,0] * u_rect_img + Cinv[0,2]
y_rect_cam = Cinv[1,1] * v_rect_img + Cinv[1,2]

r_out = np.sqrt(x_rect_cam**2 + y_rect_cam**2) # = x_rect_cam (central horizontal line)
rin_rout = 1+ k1*r_out**2 + k2*r_out**4 + k3*r_out**6
plt.plot(r_out, rin_rout)
plt.xlabel('r_out')
plt.ylabel('r_in/r_out')
plt.show()
