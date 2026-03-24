import streamlit as st
import os
import time
from speech import extract_audio, speech_to_text, count_filler_words
from emotion import analyze_emotion, analyze_face_emotion
from confidence import calculate_confidence_score
from feedback import get_interview_feedback
from utils import cleanup_files, generate_report_text

# --- PAGE CONFIG ---
st.set_page_config(page_title="InterviewAI Pro", page_icon="🎯", layout="wide")

# --- CUSTOM CSS FOR BETTER UI ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; border: 1px solid #3e4259; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #ff4b4b; color: white; height: 3em; }
    .report-card { background-color: #262730; padding: 20px; border-radius: 15px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_value=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("🎯 InterviewAI Pro")
    st.markdown("---")
    st.info("Upload your video to get an instant AI-powered performance breakdown.")
    st.write("✅ Confidence Scoring")
    st.write("✅ Facial Emotion Tracking")
    st.write("✅ Filler Word Detection")
    st.write("✅ Detailed Feedback")

# --- MAIN CONTENT ---
st.title("🚀 AI Interview Performance Analyzer")
st.write("Elevate your career with data-driven interview coaching.")

uploaded_file = st.file_uploader("📤 Drag and drop your interview video here", type=["mp4", "mov", "avi"])

if uploaded_file:
    temp_video = "temp_video.mp4"
    with open(temp_video, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    col_v, col_a = st.columns([1.5, 1])
    
    with col_v:
        st.video(temp_video)
    
    with col_a:
        st.subheader("Process Analysis")
        analyze_btn = st.button("✨ Start AI Analysis")
        
        if analyze_btn:
            with st.status("🤖 AI is thinking...", expanded=True) as status:
                st.write("🔊 Processing Audio...")
                audio_path = extract_audio(temp_video)
                transcript = speech_to_text(audio_path)
                fillers = count_filler_words(transcript)
                
                st.write("🎭 Analyzing Facial Expressions...")
                face_emotion = analyze_face_emotion(temp_video)
                
                st.write("📈 Calculating Metrics...")
                text_emotion = analyze_emotion(transcript)
                conf_results = calculate_confidence_score(transcript, 60, fillers)
                feedback = get_interview_feedback(conf_results['score'], face_emotion, fillers)
                
                status.update(label="Analysis Complete!", state="complete")

            # --- METRICS SECTION ---
            st.markdown("### 📊 Performance Overview")
            m1, m2, m3 = st.columns(3)
            m1.metric("Confidence", f"{conf_results['score']}%")
            m2.metric("Emotion", face_emotion.capitalize())
            m3.metric("WPM", conf_results['wpm'])

            # --- FEEDBACK SECTION ---
            st.markdown("### 🤖 AI Coaching")
            for tip in feedback:
                st.success(tip) if "✅" in tip else st.warning(tip)

            # --- TRANSCRIPT & REPORT ---
            with st.expander("📖 View Full Transcript"):
                st.write(transcript)

            report_data = generate_report_text(transcript, text_emotion, conf_results)
            st.download_button("📥 Download Full PDF Report", data=report_data, file_name="Interview_Report.txt")
            
            # Cleanup
            cleanup_files([audio_path, temp_video])