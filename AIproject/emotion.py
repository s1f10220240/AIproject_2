from fer import FER
import matplotlib.pyplot as plt


#画像読み込み
test_image = plt.imread("..\\img\\怒り\\31046586_s.jpg")

# 感情分析実行
emo_detector = FER(mtcnn=True)
capture_emotion = emo_detector.detect_emotions(test_image)

# 結果
print(capture_emotion)


# 画像と最も高い感情表示
dominant_emotion, emotion_score = emo_detector.top_emotion(test_image)
plt.imshow(test_image)
print(dominant_emotion, emotion_score)