from flask import Flask, request
import cv2
import numpy as np
import face_recognition
import requests
import os
import sys

app = Flask(__name__)

# =========================
# TELEGRAM CONFIG
# =========================
BOT_TOKEN = "8631637642:AAFA1Mit3cShikO5NM0Fmm8qxBBVva8GDP8"
CHAT_ID = "1339280432"

ESP32_STREAM_URL = "http://192.168.122.22"

def send_telegram(image_bytes):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    files = {"photo": ("image.jpg", image_bytes)}
    data = {
        "chat_id": CHAT_ID,
        "caption": f"🚨 Unknown person detected!\nLive: {ESP32_STREAM_URL}"
    }

    try:
        response = requests.post(url, files=files, data=data)
        print("📤 Telegram status:", response.status_code)
    except Exception as e:
        print("❌ Telegram error:", e)


# =========================
# LOAD KNOWN FACES (MULTI)
# =========================
known_encodings = []
known_names = []

def load_known_faces():
    folder = "known_faces"

    if not os.path.exists(folder):
        print("❌ 'known_faces' folder missing")
        sys.exit()

    for file in os.listdir(folder):
        path = os.path.join(folder, file)

        try:
            img = face_recognition.load_image_file(path)
            encodings = face_recognition.face_encodings(img)

            if len(encodings) == 0:
                print(f"⚠️ No face in {file}")
                continue

            known_encodings.append(encodings[0])
            known_names.append(file)

            print(f"✅ Loaded: {file}")

        except Exception as e:
            print(f"❌ Error loading {file}: {e}")

    if len(known_encodings) == 0:
        print("❌ No valid faces loaded!")
        sys.exit()

    print(f"🎯 Total known faces: {len(known_encodings)}")


load_known_faces()


# =========================
# MAIN ENDPOINT
# =========================
@app.route("/upload", methods=["POST"])
def upload():
    img_bytes = request.data

    if len(img_bytes) == 0:
        return "No data", 400

    # Convert bytes → image
    nparr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if img is None:
        return "Decode failed", 400

    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Detect faces
    face_locations = face_recognition.face_locations(rgb)
    encodings = face_recognition.face_encodings(rgb, face_locations)

    print("\n📸 New frame received")
    print("Faces found:", len(encodings))

    unknown_detected = False

    for encoding in encodings:
        matches = face_recognition.compare_faces(known_encodings, encoding)
        face_distances = face_recognition.face_distance(known_encodings, encoding)

        print("Match results:", matches)
        print("Distances:", face_distances)

        if True in matches:
            best_match_index = np.argmin(face_distances)
            name = known_names[best_match_index]
            print(f"✅ Recognized: {name}")
        else:
            print("🚨 Unknown face detected!")
            unknown_detected = True

    # Send alert ONLY if unknown face exists
    if unknown_detected:
        send_telegram(img_bytes)
    elif len(encodings) == 0:
        print("⚠️ No face detected")
    else:
        print("🙂 All faces known")

    return "OK", 200


# =========================
# RUN SERVER
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)