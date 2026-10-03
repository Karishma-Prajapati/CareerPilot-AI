import re
from collections import Counter


# Common filler words
FILLER_WORDS = [
    "um",
    "uh",
    "like",
    "actually",
    "basically",
    "literally",
    "you know",
    "i mean",
    "sort of",
    "kind of"
]


def analyze_text(text):
    """
    Analyze transcript and return communication metrics.
    """

    # Convert to lowercase
    clean_text = text.lower()

    # Extract words
    words = re.findall(r"\b[a-zA-Z]+\b", clean_text)

    total_words = len(words)

    # Count sentences
    sentences = re.split(r"[.!?]+", text)
    sentences = [s.strip() for s in sentences if s.strip()]

    sentence_count = len(sentences)

    # Count filler words
    filler_counts = {}

    for filler in FILLER_WORDS:

        if " " in filler:
            count = clean_text.count(filler)
        else:
            count = words.count(filler)

        if count > 0:
            filler_counts[filler] = count

    total_fillers = sum(filler_counts.values())

    # Count word frequency
    word_frequency = Counter(words)

    # Remove very common words
    ignored_words = {
        "the", "a", "an", "is", "are", "was",
        "were", "to", "of", "and", "in", "on",
        "for", "it", "this", "that", "i", "my",
        "me", "we", "you"
    }

    repeated_words = {
        word: count
        for word, count in word_frequency.items()
        if count >= 3 and word not in ignored_words
    }

    return {
        "total_words": total_words,
        "sentence_count": sentence_count,
        "filler_counts": filler_counts,
        "total_fillers": total_fillers,
        "repeated_words": repeated_words
    }