from django import forms
from .models import ImageUpload


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageUpload
        fields = ['image']  # アップロードするフィールド



class MoodAndImageForm(forms.Form):
    gender = forms.ChoiceField(
        label='性別',
        choices=[('男性', '男性'), ('女性', '女性'), ('その他', 'その他')],
    )
    age = forms.IntegerField(label='年齢', min_value=0, max_value=120)
    hobby = forms.CharField(label='趣味', max_length=200, required=False)
    mood = forms.CharField(label="備考", max_length=100, required=True)