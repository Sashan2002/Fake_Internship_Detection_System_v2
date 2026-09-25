"""
Service layer wrapping ml/ for use by Django views. Ported from the Flask
build's backend/services/*.py, with config values now read from Django
settings instead of a dataclass-based Config object.
"""
import logging

from django.conf import settings

from apps.detection.preprocessing import build_combined_text
from ml.credibility.credibility_features import build_credibility_vector, summarise_indicators
from ml.uncertainty.uncertainty_estimation import DeferThresholds, classify_with_defer

logger = logging.getLogger(__name__)

DISCLAIMER = (
    "This explanation describes which factors most influenced the model's "
    "own prediction for this specific submission. It is not independent "
    "verification of the employer or proof that the advertisement is "
    "fraudulent."
)


class ModelNotTrainedError(RuntimeError):
    """Raised when a prediction is requested but no trained model artefact exists yet."""


class PredictionService:
    def __init__(self):
        self._baseline_model = None
        self._load_error = None

    def _load_baseline(self):
        if self._baseline_model is not None:
            return self._baseline_model
        if not settings.BASELINE_MODEL_PATH.exists():
            self._load_error = (
                f"No trained baseline model found at {settings.BASELINE_MODEL_PATH}. "
                f"Run `python -m ml.train_baseline` first."
            )
            return None
        from ml.models.baseline_tfidf import TfidfLogRegBaseline
        self._baseline_model = TfidfLogRegBaseline.load(str(settings.BASELINE_MODEL_PATH))
        return self._baseline_model

    def predict(self, advertisement_record: dict) -> dict:
        model = self._load_baseline()
        if model is None:
            raise ModelNotTrainedError(self._load_error)

        text = build_combined_text(advertisement_record)
        fraud_probability = float(model.predict_proba([text])[0])
        return {"fraud_probability": fraud_probability, "model_version": settings.ACTIVE_MODEL_VERSION}


class CredibilityService:
    def analyse(self, advertisement_record: dict) -> dict:
        vector = build_credibility_vector(advertisement_record)
        summary = summarise_indicators(vector)
        return {"feature_vector": vector, "summary": summary}


class UncertaintyService:
    def __init__(self):
        self.thresholds = DeferThresholds(
            low=settings.DEFER_THRESHOLD_LOW, high=settings.DEFER_THRESHOLD_HIGH
        )

    def assess(self, fraud_probability: float) -> dict:
        return classify_with_defer(fraud_probability, self.thresholds)


class ExplanationService:
    def __init__(self):
        self._lime_explainer = None

    def _get_lime_explainer(self):
        if self._lime_explainer is None:
            if not settings.BASELINE_MODEL_PATH.exists():
                return None
            from ml.models.baseline_tfidf import TfidfLogRegBaseline
            from ml.explainability.lime_explainer import TextLimeExplainer

            model = TfidfLogRegBaseline.load(str(settings.BASELINE_MODEL_PATH))
            self._lime_explainer = TextLimeExplainer(model.pipeline.predict_proba)
        return self._lime_explainer

    def explain_text(self, combined_text: str) -> dict:
        explainer = self._get_lime_explainer()
        if explainer is None:
            return {
                "available": False,
                "reason": "No trained model available yet for explanation generation.",
                "disclaimer": DISCLAIMER,
            }
        try:
            explanation = explainer.explain_instance(combined_text, num_features=8)
            result = explanation.to_dict()
            result["available"] = True
            result["disclaimer"] = DISCLAIMER
            return result
        except Exception as exc:  # pragma: no cover - defensive
            logger.exception("LIME explanation failed")
            return {"available": False, "reason": str(exc), "disclaimer": DISCLAIMER}


prediction_service = PredictionService()
credibility_service = CredibilityService()
uncertainty_service = UncertaintyService()
explanation_service = ExplanationService()
