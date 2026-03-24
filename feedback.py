def get_interview_feedback(confidence_score, dominant_emotion, filler_count):
    """Generates personalized feedback for the user based on metrics."""
    feedback = []
    
    # Confidence Feedback
    if confidence_score > 80:
        feedback.append("✅ **Confidence:** Excellent! You sound very professional and self-assured.")
    elif confidence_score > 60:
        feedback.append("⚠️ **Confidence:** Good, but try to speak with a bit more energy to show enthusiasm.")
    else:
        feedback.append("❌ **Confidence:** You sound a bit hesitant. Practice your main points to reduce pauses.")

    # Emotion/Facial Feedback
    # Note: DeepFace returns lowercase emotions like 'happy', 'neutral', 'sad'
    if dominant_emotion.lower() in ['happy', 'neutral']:
        feedback.append(f"😊 **Expression:** Your facial expression was '{dominant_emotion}', which is perfect for an interview.")
    elif dominant_emotion.lower() == 'sad' or dominant_emotion.lower() == 'angry':
        feedback.append(f"❓ **Expression:** You looked a bit '{dominant_emotion}'. Try to relax your facial muscles and smile more.")
    else:
        feedback.append(f"🎭 **Expression:** Your dominant expression was '{dominant_emotion}'. Aim for a friendly, neutral look.")

    # Filler Word Feedback
    total_fillers = sum(filler_count.values())
    if total_fillers > 5:
        feedback.append(f"🚫 **Fillers:** You used {total_fillers} filler words. Try to pause for a second instead of saying 'um' or 'like'.")
    else:
        feedback.append("🎯 **Vocabulary:** Great job! Your speech is clean and direct with very few filler words.")

    return feedback