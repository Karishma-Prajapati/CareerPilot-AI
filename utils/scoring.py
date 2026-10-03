def calculate_communication_score(
    speaking_speed,
    total_fillers,
    total_words,
    repeated_words
):
    # --------------------------------
    # 1. Speaking Score - 40 points
    # --------------------------------

    if speaking_speed <= 0:
        speed_score = 0

    elif 120 <= speaking_speed <= 150:
        # Ideal interview speaking speed
        speed_score = 40

    elif 100 <= speaking_speed < 120:
        speed_score = 34

    elif 150 < speaking_speed <= 170:
        speed_score = 34

    elif 80 <= speaking_speed < 100:
        speed_score = 26

    elif 170 < speaking_speed <= 190:
        speed_score = 26

    else:
        speed_score = 18

    # --------------------------------
    # 2. Filler Word Score - 30 points
    # --------------------------------

    if total_words > 0:

        filler_percentage = (
            total_fillers / total_words
        ) * 100

    else:
        filler_percentage = 100

    if filler_percentage <= 2:
        filler_score = 30

    elif filler_percentage <= 4:
        filler_score = 25

    elif filler_percentage <= 6:
        filler_score = 20

    elif filler_percentage <= 8:
        filler_score = 14

    else:
        filler_score = 8

    # --------------------------------
    # 3. Repeated Words Score - 30 points
    # --------------------------------

    repeated_count = len(repeated_words)

    if repeated_count <= 2:
        repetition_score = 30

    elif repeated_count <= 4:
        repetition_score = 25

    elif repeated_count <= 6:
        repetition_score = 20

    elif repeated_count <= 10:
        repetition_score = 14

    else:
        repetition_score = 8

    # --------------------------------
    # Final Score
    # --------------------------------

    score = (
        speed_score
        + filler_score
        + repetition_score
    )

    # Keep between 0 and 100
    score = max(0, min(100, score))

    return score