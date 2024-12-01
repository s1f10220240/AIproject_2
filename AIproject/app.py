from django.shortcuts import render
from .forms import MoodForm
import openai

# OpenAI APIキーを設定
openai.api_key = "your_openai_api_key"  # 必ず安全に保管してください

def sample(request):
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
