from rest_framework import serializers
from apps.detection.models import Prediction, Explanation, CredibilityAnalysis


class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = [
            "id", "advertisement", "model_version", "predicted_class",
            "fraud_probability", "confidence", "uncertainty", "defer_flag", "created_at",
        ]


class ExplanationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Explanation
        fields = ["id", "prediction", "explanation_json", "evidence_summary", "created_at"]


class CredibilityAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = CredibilityAnalysis
        fields = ["id", "advertisement", "feature_json", "indicator_summary", "created_at"]
