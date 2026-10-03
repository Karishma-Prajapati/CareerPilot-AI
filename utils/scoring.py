def calculate_communication_score(
    speaking_speed,
    total_fillers,
    total_words,
    repeated_words
):
    # Start with full score
    score = 100

    # Speaking speed
    if speaking_speed < 100:
        score -= 5

    elif speaking_speed <= 150:
        score += 0

    elif speaking_speed <= 180:
        score -= 5

    else:
        score -= 10

    # Filler words
    if total_words > 0:

        filler_percentage = (
            total_fillers / total_words
        ) * 100

        if filler_percentage > 8:
            score -= 15

        elif filler_percentage > 5:
            score -= 10

        elif filler_percentage > 3:
            score -= 5

    # Repeated words
    repeated_count = len(repeated_words)

    if repeated_count > 5:
        score -= 10

    elif repeated_count > 3:
        score -= 5

    # Keep score between 0 and 100
    score = max(0, min(100, score))

    return score