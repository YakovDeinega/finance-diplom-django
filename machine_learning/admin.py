from django.contrib import admin

from machine_learning.models import MLModel, Prediction

# Register your models here.
admin.site.register(MLModel)
admin.site.register(Prediction)