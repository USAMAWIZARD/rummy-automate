import cv2
from find_image import ResizeWithAspectRatio
img = cv2.imread("2.png")  # Read image
  
# Setting parameter values
t_lower = 10  # Lower Threshold
t_upper = 540  # Upper threshold
  
# Applying the Canny Edge filter
edge = cv2.Canny(img, t_lower, t_upper)
cv2.saveImage("edge.png", edge)
cv2.imshow('original', ResizeWithAspectRatio(img,width=300))
cv2.imshow('edge', ResizeWithAspectRatio(edge,width=300))
cv2.waitKey(0)
cv2.destroyAllWindows()