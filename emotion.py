from textblob import TextBlob
from deepface import DeepFace
import cv2

def analyze_emotion(text):
    """Analyzes the sentiment of the transcript (Text-based)."""
    if not text or text.strip() == "":
        return {"sentiment": "Neutral", "score": 0.0}
    
    analysis = TextBlob(text)
    score = analysis.sentiment.polarity
    
    if score > 0.1:
        emotion = "Positive/Enthusiastic"
    elif score < -0.1:
        emotion = "Negative/Stressed"
    else:
        emotion = "Neutral/Professional"
        
    return {"sentiment": emotion, "score": round(score, 2)}

def analyze_face_emotion(video_path):
    """Analyzes facial emotions from video frames (Vision-based)."""
    cap = cv2.VideoCapture(video_path)
    emotions_list = []
    frame_count = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Analyze every 60th frame (roughly every 2 seconds) to keep it fast
        if frame_count % 60 == 0:
            try:
                # enforce_detection=False prevents crashing if a face isn't perfectly clear
                results = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
                emotions_list.append(results[0]['dominant_emotion'])
            except:
                continue
        frame_count += 1
    
    cap.release()
    
    if not emotions_list:
        return "neutral" # Default if no face is detected
        
    # Find the most frequent emotion shown on the face
    most_common = max(set(emotions_list), key=emotions_list.count)
    return most_common