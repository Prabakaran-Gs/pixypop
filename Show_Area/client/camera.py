from threading import Thread
from helper import find_persons, compare_faces
import cv2
import time
from icecream import ic
# ic.disable()

class Camera:
    def __init__(self, camera=0):
        self.user = None
        self._stop = False
        self.cam = cv2.VideoCapture(camera)
        ic("Object Created")

    def start_process(self):
        self.thread_obj = Thread(target=self.process, daemon=True)
        self.thread_obj.start()

    def stop_process(self):
        self._stop = True
        self.thread_obj.join()

    def process(self):
        while not self._stop:
            ret, frame = self.cam.read()
            if not ret:
                print("Error Occurred: Video is not received successfully")
                self.stop_process()
                return
            
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            ic(frame_rgb.shape)

            persons = find_persons(frame_rgb)

            if persons:
                for person in persons:
                    tag = compare_faces(person)
                    if tag != -1:
                        ic(tag)
                        self.user = tag

            # Store the frame to be displayed later
            self.current_frame = frame

            time.sleep(1)  # Add a small delay to prevent high CPU usage

    def show_frame(self):
        while not self._stop:
            if hasattr(self, 'current_frame'):
                cv2.imshow("output", self.current_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.stop_process()

if __name__ == '__main__':
    
    cam = Camera()
    cam.start_process()

    # Start a loop in the main thread for displaying the frames
    cam.show_frame()

    cam.stop_process()
    cv2.destroyAllWindows()
