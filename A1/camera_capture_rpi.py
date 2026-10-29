import datetime
import cv2
from picamera2 import Picamera2
import threading
import os

picam2 = Picamera2()
config = picam2.create_still_configuration(
    main = {"size": picam2.sensor_resolution},
    raw  = {"size": picam2.sensor_resolution}
)

# Disable lens distortion correction
#config["controls"]["draft:LensShadingEnable"]  = False
#config["controls"]["draft:NoiseReductionMode"] = 0

picam2.configure(config)
picam2.start()

def show_preview(mode):
    while True:
        image = picam2.capture_array(mode)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        cv2.imshow("Frame", cv2.resize(image, (800,600)))
        key = cv2.waitKey(1)
        if key == ord("q"):
            break
        elif key == ord('s'):  # save image
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            image_name = f"image_{timestamp}.png"
            success = cv2.imwrite(image_name, image)
            if success:
                print(f"Saved image: {image_name}")
            else:
                cwd = os.getcwd()
                print(f"Failed to save image. Check if folder '{cwd}' is write-protected.")
    
    cv2.destroyAllWindows()
    picam2.stop()
    picam2.close()
    os._exit(0)

#mode = "raw"
mode = "main"

thread = threading.Thread(target = show_preview, args=(mode,))
thread.start()

# Show available camera controls
#print(picam2.camera_controls)

# Show info for controls
#picam2.camera_ctrl_info

# Set controls
#picam2.set_controls({'AeEnable':False})       # Values: True or False
#picam2.set_controls({'AnalogueGainMode':1})   # Values: 0 or 1
#picam2.set_controls({'ExposureTime': 10000})  # Values: 75 to 1238765 [microseconds]
#picam2.set_controls({'AnalogueGain': 1.0})    # Values: 1.0 to 10.66
#picam2.set_controls({'Brightness': 0.0})      # Values: -1.0 to 1.0
#picam2.set_controls({'Contrast': 1.0})        # Values: 0.0 to 32.0
