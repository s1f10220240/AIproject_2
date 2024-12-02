from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
import json
from fer import FER
from PIL import Image
import numpy as np
from .forms import MoodAndImageForm
import openai
import logging


logger = logging.getLogger(__name__)


# OpenAI APIキーを設定
openai.api_key = "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"  # 必ず安全に保管する

travel_plan = None


def index(request):
    form = MoodAndImageForm()
    return render(request, 'html/index.html', {'form': form})

def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        logger.debug("感情分析を開始します...")
        image = request.FILES['image']
        # 保存先のしてい
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'uploads'))
        # ファイルへの保存
        fs.save(image.name, image)
        
        # 感情分析の処理
        result = analyze_emotion()
          

        form = MoodAndImageForm(request.POST)
        if form.is_valid():
            mood = form.cleaned_data['mood']
            gender = form.cleaned_data['gender']
            age = form.cleaned_data['age']
            hobby = form.cleaned_data['hobby']
            dominant = result.get('dominant_emotion', 'データなし')
            score = result.get('emotion_score', 'データなし') 
            print("???????????????????????????")

            # ChatGPT APIを呼び出して旅行プランを作成 
            prompt = f"""
            性別: {gender}
            年齢: {age}
            趣味: {hobby}
            備考: {mood}
            ユーザー感情: 
                - 支配的な感情: { dominant }
                - スコア: { score }

            上記の気分に合った旅行プランを考え、以下の形式で出力してください。

            1. 場所: (都内)
            2. 主なアクティビティ:
            3. 必要日数:
            4. 注意点:
            """
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}]
                )
                travel_plan = response['choices'][0]['message']['content']
                print("主な感情：", dominant)
                print("score:", score)
                return render(request, 'html/show.html', {'travel_plan': travel_plan})
            
            except Exception as e:
                print(f"エラーが発生しました: {e}")
                return render(request, 'html/index.html', {'error': str(e)})

    else:
        return render(request, 'html/index.html', {'form': form, 'error': form.errors})




def analyze_emotion():
    
    images = os.listdir(os.path.join(settings.MEDIA_ROOT, 'uploads'))  # 保存ディレクトリ内の画像を取得
    uploads_directory = os.path.join(settings.MEDIA_ROOT, 'uploads')
    images = os.listdir(uploads_directory)

    if not images:
        raise FileNotFoundError("No images found in the uploads directory.")

    images = sorted(
    images,
    key=lambda x: os.path.getmtime(os.path.join(uploads_directory, x)),
    reverse=True)

    # 最新の画像を取得
    image_path = os.path.join(uploads_directory, images[0])

    # 画像をPILで読み込む
    pil_image = Image.open(image_path).convert("RGB")  # RGBAをRGBに変換
    image = np.array(pil_image)  # NumPy配列に変換
    
    # FERライブラリでの顔検出
    emo_detector = FER(mtcnn=True) # mtcnnを有効することによって精度の向上

    # 感情認識の実行
    captured_emotions = emo_detector.detect_emotions(image)
    dominant_emotion, score = emo_detector.top_emotion(image)

    # 結果を辞書としてまとめる
    result = {
        "dominant_emotion": dominant_emotion,
        "emotion_score": score,
    }
    return result


''' 
    travel_plan = None

    if request.method == "POST":
        form = MoodForm(request.POST)
        if form.is_valid():
            mood = form.cleaned_data['mood']
            
            # ChatGPT APIを呼び出して旅行プランを作成
            prompt = f"""
            ユーザーの気分: {mood}

            上記の気分に合った旅行プランを考え、以下の形式で出力してください。

            1. 場所: 
            2. 主なアクティビティ:
            3. 推奨する滞在日数:
            4. 他の注意点:
            """
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}]
                )
                travel_plan = response['choices'][0]['message']['content']
            except Exception as e:
                travel_plan = f"エラーが発生しました: {e}"
    else:
        form = MoodForm()

    return render(request, 'index.html', {'form': form, 'travel_plan': travel_plan})
'''