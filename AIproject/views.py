from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
import json
from fer import FER
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np


def upload_image(request):
    if request.method == 'POST' and request.FILES['image']:
        image = request.FILES['image']
        # 保存先のしてい
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'uploads'))
        # ファイルへの保存
        fs.save(image.name, image)
        
        # 感情分析の処理
        result = analyze_emotion()
        # 保存先の指定
        json_directory = os.path.join(settings.MEDIA_ROOT, 'json')
        result_file_url = os.path.join(json_directory, 'emotion_result.json')
        # 結果をjsonで保存
        with open(result_file_url, 'w') as f:
            json.dump(result, f)
        
        return redirect('show_image')
    # 仮におかしいものが来たら同じページに戻る
    return render(request, 'html/index.html')



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
    emo_detector = FER(mtcnn=True)

    # 感情認識の実行
    captured_emotions = emo_detector.detect_emotions(image)
    dominant_emotion, score = emo_detector.top_emotion(image)

    # 結果を辞書としてまとめる
    result = {
        "captured_emotions": captured_emotions,
        "dominant_emotion": dominant_emotion,
        "emotion_score": score,
    }
    return result


def show_image(request):    
    # アップロードディレクトリの取得
    uploads_directory = os.path.join(settings.MEDIA_ROOT, 'uploads')
    images = os.listdir(uploads_directory)

    if not images:
        raise FileNotFoundError("No images found in the uploads directory.")

    images = sorted(
    images,
    key=lambda x: os.path.getmtime(os.path.join(uploads_directory, x)),
    reverse=True)

    # 最初の画像のURLを生成
    image_url = settings.MEDIA_URL + 'uploads/' + images[0]


    result_file_path = os.path.join(settings.MEDIA_ROOT, 'json', 'emotion_result.json')
    if not os.path.exists(result_file_path):
        raise FileNotFoundError(f"Result file not found: {result_file_path}")
    
    with open(result_file_path, 'r') as f:
        emotion_result = json.load(f)
    
    return render(request, 'html/show.html', {
        'image_url': image_url,
        'emotion': emotion_result.get('dominant_emotion', 'unknown'),
        'score': emotion_result.get('emotion_score', 0),
    })