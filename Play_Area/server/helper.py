import json
import face_recognition as fr
import os
import numpy as np
import cv2
import brisque
import icecream as ic

BEST_VAL = 35
BLUR_THRESHOLD = 100

def find_persons(image):
    '''
    Detect faces in the image and return a list of face encodings
    '''
    return fr.face_encodings(image)


'''
Creation of new face data
'''
# Creation of new face data

def get_name(n):
    result = ""
    while n > 0:
        n -= 1  # Decrease n by 1 to make modulo operation compatible with 'A' being 1 not 0
        remainder = n % 26
        result = chr(65 + remainder) + result
        n = n // 26
    return result

def create_json(result,person_enc):
    data = dict()
    data["name"] = result
    data["encoding"] = person_enc.tolist()
    data["images"] = []
    with open(f"static/data/{result}.json", "w") as json_file:
        json.dump(data, json_file,indent=4)

'''
Identification
'''
# Identification of new face data

def compare_faces(person_enc):
    names , encodings = get_all_encodings()
    arr = fr.compare_faces(encodings, person_enc,tolerance=0.4)
    # arr = [i==person_enc for i in encodings ]
    for name,flag in zip(names,arr):
        if flag:
            return name
    return -1


def get_all_encodings():
    encodings = []
    names = []
    for filename in os.listdir("static/data"):
        if filename.endswith(".json"):
            with open(f"static/data/{filename}", "r") as json_file:
                data = json.load(json_file)
                encodings.append(np.array(data["encoding"]))
                names.append(data["name"])
    return names,encodings


'''
    Best Image Check
'''
def is_best(image):
    import brisque
    brisque = brisque.BRISQUE()
    score = brisque.score(image)
    ic(score)   #! Printing the brisque score
    return score < BEST_VAL and score > 0

def is_blurry(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    ic(laplacian_var)   #! Printing the laplacian_blur
    return laplacian_var < BLUR_THRESHOLD

def get_images(tag):
    json_file = os.path.join("static","data",tag+".json")
    with open(json_file, 'r') as file:
        data = json.load(file)
    return data["images"]


