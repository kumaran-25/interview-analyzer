def calculate_confidence_score(text, duration_seconds, filler_counts):
    """
    Calculates a confidence score (0-100).
    - Pacing (WPM): 40%
    - Fluency (Filler Penalty): 60%
    """
    if not text or duration_seconds <= 0:
        return {"score": 0, "wpm": 0, "status": "Inconclusive"}

    words = text.split()
    word_count = len(words)
    
    # 1. Calculate Words Per Minute (WPM)
    # Average professional speech is 120-160 WPM
    wpm = (word_count / duration_seconds) * 60
    
    # Pacing Score logic
    if 120 <= wpm <= 160:
        pacing_score = 100
    else:
        # Subtract points if too slow or too fast
        dist = min(abs(120 - wpm), abs(160 - wpm))
        pacing_score = max(0, 100 - (dist * 2))

    # 2. Fluency Score (Penalty for 'um', 'uh', 'like')
    total_fillers = sum(filler_counts.values())
    # Subtract 5 points for every filler word used
    fluency_score = max(0, 100 - (total_fillers * 5))

    # 3. Final Weighted Score
    final_score = (pacing_score * 0.4) + (fluency_score * 0.6)
    
    # Determine Level
    if final_score >= 80:
        status = "High Confidence"
    elif final_score >= 60:
        status = "Moderate Confidence"
    else:
        status = "Needs Improvement"

    return {
        "score": round(final_score, 1),
        "wpm": round(wpm, 1),
        "status": status
    }