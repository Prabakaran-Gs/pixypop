import cv2
import json
from queue import Queue
from threading import Thread
from ..client.helper import get_name, compare_faces , create_json, find_persons , is_best , is_blurry

QUEUE_SIZE = 5
           

class Sever:

    def __init__(self,camera) -> None:

        # Variable 
        self.cam = cv2.VideoCapture(camera)
        self.image_queue = Queue(maxsize=QUEUE_SIZE)
        
        # Constants
        self.counter :int = 0
        self.person :int = 0
        self.stop :bool = False

        # Threading
        self._img_processor = Thread(target=self.img_processor)
        self._img_processor.start()

    def img_processor(self):
        print("Thread Started")
        while not self.stop:
            while not self.image_queue.empty():
                frame_rgb = self.image_queue.get()
                frame = cv2.cvtColor(frame_rgb,cv2.COLOR_RGB2BGR)

                persons = find_persons(frame_rgb)
                '''
                Best Implementation done
                '''
                if persons and is_best(frame_rgb) and is_blurry(frame_rgb):
                    frame_name = "images/"+str(self.counter)+".jpg"
                    cv2.imwrite(frame_name,frame)
                    self.counter += 1
                    for person_enc in persons:
                        tag = self.get_tag(person_enc)
                        self.store_person(tag,frame_name)

    def start(self):
        print("Camera Opened")
        piks = 0
        while self.cam.isOpened():
            ret , frame = self.cam.read()
            frame_rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            piks += 1
            if piks%5 == 0:
                piks = 0
                if self.image_queue.full():
                    _ = self.image_queue.get()

                self.image_queue.put(frame_rgb)

            if ret:
                cv2.imshow('Video', frame)
                if cv2.waitKey(1) & 0XFF == ord('q'):
                    self.stop = True
                    break
            else:
                break
        
        cv2.destroyAllWindows()
        self.cam.release()

    def get_tag (self,person_enc):
        '''
        comapere with the other person 
        if present return the tag
        else return a new tag (get_name)
        '''
        tag = compare_faces(person_enc)
        if tag == -1:
            self.person += 1
            tag = get_name(self.person)
            create_json(tag,person_enc)
        
        return tag
    
    def store_person (self,tag,image_name):
        json_file = "data/"+str(tag)+".json"
        with open(json_file, 'r') as file:
            data = json.load(file)

        data['images'].append(image_name)

        with open(json_file, 'w') as file:
            json.dump(data, file,indent=4)



if __name__ == "__main__":
    
    place1 = Sever("/dev/video0")
    place1.start()
