import io
import time
import cv2
import os
from Components.Actuators.Relay import relays

class WebcamService:
    def get_photo(self) -> bytes:
        cap = cv2.VideoCapture(0)

        ret, frame = cap.read()

        cap.release()

        if not ret:
            return None

        _, photo_bytes = cv2.imencode(".jpg", frame)

        return photo_bytes.tobytes()

    def get_timelapse(self):
        # Create a list of photo filenames in the save directory
        photos = [f"./photos/{file}" for file in os.listdir("./photos") if file.endswith(".jpg")]

        if not photos:
            print("No photos found for timelapse.")
            return None

        # Sort the photos by modification time (oldest first)
        photos.sort(key=lambda x: os.path.getmtime(x))

        # Define the codec and video parameters
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        fps = 2  # Frames per second
        width, height = cv2.imread(photos[0]).shape[1], cv2.imread(photos[0]).shape[0]

        # Create a VideoWriter object with a dummy filename (it won't be used)
        output_filename = "dummy.mp4"
        out = cv2.VideoWriter(output_filename, fourcc, fps, (width, height))

        # Read and write each photo to the video
        for photo in photos:
            frame = cv2.imread(photo)
            out.write(frame)

        # Release the video writer
        out.release()

        # Read the written video file into a BytesIO object
        with open(output_filename, "rb") as video_file:
            video_data = video_file.read()

        # Return the video data as bytes
        return video_data
    
    def get_save_photo(self):
        print("Fotografando ambiente")
        lightInitialState = relays["light"].get_state()
        if lightInitialState == "OFF":
            relays["light"].turn_on()
            time.sleep(0.5)
        
        photo_bytes = self.get_photo()
        if photo_bytes:
            photoName = str((time.time() * 1000)).replace(".", "")
            with open(f"./photos/{photoName}.jpg", "wb") as f:
                f.write(photo_bytes)
        
        if lightInitialState == "OFF": 
            relays["light"].turn_off()

webcamService = WebcamService()
