"""
`credibility_analysis`, `predictions`, `explanations`, `model_versions`
tables (Section 5 / Table 2), via Django ORM.
"""
from django.db import models
from apps.advertisements.models import Advertisement


class CredibilityAnalysis(models.Model):
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name="credibility_analyses")
    feature_json = models.JSONField()
    indicator_summary = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


class Prediction(models.Model):
    LEGIT = "Potentially Legitimate"
    FRAUD = "Potentially Fraudulent"
    REVIEW = "Requires Review"
    CLASS_CHOICES = [(LEGIT, LEGIT), (FRAUD, FRAUD), (REVIEW, REVIEW)]

    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name="predictions")
    model_version = models.CharField(max_length=100)
    predicted_class = models.CharField(max_length=32, choices=CLASS_CHOICES)
    fraud_probability = models.FloatField()
    confidence = models.FloatField()
    uncertainty = models.FloatField(null=True, blank=True)
    defer_flag = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


class Explanation(models.Model):
    prediction = models.ForeignKey(Prediction, on_delete=models.CASCADE, related_name="explanations")
    explanation_json = models.JSONField()
    evidence_summary = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


class ModelVersion(models.Model):
    model_name = models.CharField(max_length=100)
    version = models.CharField(max_length=50)
    training_dataset = models.CharField(max_length=500, blank=True, null=True)
    metrics_json = models.JSONField(blank=True, null=True)
    file_path = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("model_name", "version")

    def __str__(self):
        return f"{self.model_name}:{self.version}"
