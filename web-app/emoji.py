def map_emotion_to_emojis(emotions):
    # 大类映射表
    class_map = {
        'happy': 'joy',
        'surprise': 'joy',
        'neutral': 'joy',  # 可调为sad
        'sad': 'sad',
        'angry': 'angry',
        'disgust': 'angry',
        'fear': 'fear'
    }

    # 完整emoji表（已归类）
    emoji_bank = {
        'joy': [
            '🙂', '😊', '😄', '😁', '😃', '😀', '😅', '😆', '😂', '🤣', '🤩', '🥳',
            '😉', '😇', '☺️', '🙃', '😋', '😛', '😜', '🤪', '😎', '🤗', '🥰', '😍', '😘', '😗', '😙', '😚'
        ],
        'sad': [
            '😐', '😶', '😕', '🙁', '☹️', '😞', '😔', '😟', '😣', '😖', '😫', '😩', '😢', '😭', '🥲', '🥹', '😮‍💨', '🥺',
            '😥', '😓', '😴', '😪', '😵', '🫠', '🫩'
        ],
        'angry': [
            '😤', '😒', '😠', '😡', '🤬', '😏', '😬', '🤯', '🙄', '🙂‍↔️', '🙂‍↕️'
        ],
        'fear': [
            '😯', '😦', '😧', '😨', '😰', '😱', '🥵', '🥶', '😳', '🫣'
        ]
    }

    # Step 1: 找出前三大情绪
    top3 = sorted(emotions.items(), key=lambda x: x[1], reverse=True)[:3]

    # Step 2: 权重评分
    weights = [3, 2, 1]
    class_scores = {'joy': 0, 'sad': 0, 'angry': 0, 'fear': 0}
    for i, (emo, _) in enumerate(top3):
        cls = class_map[emo]
        class_scores[cls] += weights[i]

    # Step 3: 找到主情绪大类
    primary_class = max(class_scores, key=class_scores.get)

    # Step 4: 找该大类下的最强子情绪（用于判断强度）
    relevant = [(e, emotions[e]) for e in emotions if class_map[e] == primary_class]
    main_emotion, strength = max(relevant, key=lambda x: x[1])

    # Step 5: 映射强度到多个emoji
    emoji_list = emoji_bank[primary_class]
    idxs = [
        min(int(strength * 0.3 * len(emoji_list)), len(emoji_list)-1),
        min(int(strength * 0.5 * len(emoji_list)), len(emoji_list)-1),
        min(int(strength * 0.8 * len(emoji_list)), len(emoji_list)-1)
    ]
    return [emoji_list[i] for i in idxs]

sample = {
    'angry': 0.02,
    'disgust': 0.0,
    'fear': 0.45,
    'happy': 0.16,
    'neutral': 0.09,
    'sad': 0.27,
    'surprise': 0.01
}

emojis = map_emotion_to_emojis(sample)
print("Selected Emojis (30% / 50% / 80%):", emojis)
