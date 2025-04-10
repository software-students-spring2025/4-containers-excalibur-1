def extraction(faces):
    weights = {
        "happy": 1,
        "sad": 1,
        "angry": 1,
        "fear": 1,
        "surprise": 1,
        "disgust": 1,
        "neutral": 1,
    }
    emotion_dicts = []
    for face in faces:
        emo = face["emotions"]
        weighted = {k: emo[k] * weights.get(k, 1) for k in emo}
        emotion_dicts.append(weighted)

    return emotion_dicts


def get_emojis_from_faces(emotion):
    emoji_table = {
        "happy": ["🙂", "😊", "😄"],
        "sad": ["😞", "😢", "😭"],
        "angry": ["😒", "😠", "😡"],
        "fear": ["😨", "😰", "😱"],
        "surprise": ["😳", "😲", "🤯"],
        "disgust": ["🥴", "🤢", "🤮"],
        "neutral": ["😐", "😶‍🌫️", "🫥"],
    }

    primary = max(emotion, key=emotion.get)
    weight = emotion[primary]
    if weight <= 0.3:
        level = 0
    elif weight <= 0.7:
        level = 1
    else:
        level = 2
    emoji = emoji_table[primary][level]

    return {"emotion": primary, "emoji": emoji, "level": level}
