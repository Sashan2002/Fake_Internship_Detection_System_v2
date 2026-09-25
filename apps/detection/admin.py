from django.contrib import admin
from apps.detection.models import CredibilityAnalysis, Prediction, Explanation, ModelVersion

admin.site.register(CredibilityAnalysis)
admin.site.register(Prediction)
admin.site.register(Explanation)
admin.site.register(ModelVersion)
