from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User





class ImageUpload(models.Model):
    image = models.ImageField(upload_to='uploads/')  # アップロード先を指定
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at'] 