import time
import os
import pyrebase

firebaseConfig = {
    "apiKey": "AIzaSyBDp7nvGcsPt1PEvtBUOkxfn2SgOG-Ylbc",
    "authDomain": "proiectsi-ee95a.firebaseapp.com",
    "projectId": "proiectsi-ee95a",
    "storageBucket": "proiectsi-ee95a.appspot.com",
    "messagingSenderId": "250200043696",
    "appId": "1:250200043696:web:62c0090ac2437a2a6fcb75",
    "measurementId": "G-J9W7MFNZ93",
    "databaseURL": "gs://proiectsi-ee95a.appspot.com"
};
firebase = pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()
count =0
while True:
    saas=os.listdir(path='image')
    time.sleep(1)

    for x in saas:
        time.sleep(1)
        path = "image/imgNr" + str(count) +".png"
        pathloc ="image/" +x
        count = count +1
        storage.child(path).put(pathloc)
        print(pathloc)
        if os.path.exists(pathloc):
            os.remove(pathloc)
        
    

    
