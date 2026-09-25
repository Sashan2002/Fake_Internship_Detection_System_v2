"""
Core processing flow, per Section 1:
Internship Advertisement + Employer Information -> Validation -> NLP
Analysis + Employer Credibility Analysis -> Feature/Representation
Integration -> Fraud Classification -> Confidence/Uncertainty Assessment ->
Explainability/Evidence -> Evidence-Based User Result.
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.advertisements.models import Advertisement
from apps.advertisements.serializers import AdvertisementSerializer
from apps.detection.models import Prediction, Explanation, CredibilityAnalysis
from apps.detection.serializers import PredictionSerializer, ExplanationSerializer
from apps.detection.preprocessing import build_combined_text
from apps.detection.services import (
    prediction_service, credibility_service, uncertainty_service, explanation_service,
    ModelNotTrainedError,
)

LEGITIMACY_DISCLAIMER = (
    "'Potentially Legitimate' and 'Potentially Fraudulent' describe model "
    "predictions, not proof of an organisation's legitimacy or fraud."
)
CREDIBILITY_DISCLAIMER = (
    "These are descriptive indicators derived from the submitted "
    "information, not independent proof of employer legitimacy or fraud."
)

REQUIRED_FIELDS = ["title", "description"]


def _record_from_payload(payload: dict) -> dict:
    return {
        "title": (payload.get("title") or "").strip(),
        "location": payload.get("location") or None,
        "department": payload.get("department") or None,
        "salary_range": payload.get("salary_range") or None,
        "company_profile": payload.get("company_profile") or None,
        "description": (payload.get("description") or "").strip(),
        "requirements": payload.get("requirements") or None,
        "benefits": payload.get("benefits") or None,
        "telecommuting": int(bool(payload.get("telecommuting", 0))),
        "has_company_logo": int(bool(payload.get("has_company_logo", 0))),
        "has_questions": int(bool(payload.get("has_questions", 0))),
        "employment_type": payload.get("employment_type") or None,
        "required_experience": payload.get("required_experience") or None,
        "required_education": payload.get("required_education") or None,
        "industry": payload.get("industry") or None,
        "function_field": payload.get("function_field", payload.get("function")) or None,
        "employer_name": payload.get("employer_name") or None,
    }


def _validate_payload(payload: dict) -> list:
    errors = []
    for field in REQUIRED_FIELDS:
        if not str(payload.get(field, "")).strip():
            errors.append(f"{field} is required")
    description = str(payload.get("description", ""))
    if description and len(description) < 20:
        errors.append("description is too short to analyse meaningfully (min 20 characters)")
    return errors


@api_view(["POST"])
@permission_classes([AllowAny])
def analyse_credibility(request):
    payload = request.data
    errors = _validate_payload(payload)
    if errors:
        return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)

    record = _record_from_payload(payload)
    result = credibility_service.analyse(record)

    advertisement_id = payload.get("advertisement_id")
    if advertisement_id and Advertisement.objects.filter(pk=advertisement_id).exists():
        CredibilityAnalysis.objects.create(
            advertisement_id=advertisement_id,
            feature_json=result["feature_vector"],
            indicator_summary=result["summary"],
        )

    result["disclaimer"] = CREDIBILITY_DISCLAIMER
    return Response(result, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def predict(request):
    payload = request.data
    errors = _validate_payload(payload)
    if errors:
        return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)

    record = _record_from_payload(payload)

    try:
        prediction_result = prediction_service.predict(record)
    except ModelNotTrainedError as exc:
        return Response({"errors": [str(exc)]}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    outcome = uncertainty_service.assess(prediction_result["fraud_probability"])
    credibility = credibility_service.analyse(record)

    advertisement_id = payload.get("advertisement_id")
    prediction_id = None
    if advertisement_id and Advertisement.objects.filter(pk=advertisement_id).exists():
        prediction = Prediction.objects.create(
            advertisement_id=advertisement_id,
            model_version=prediction_result["model_version"],
            predicted_class=outcome["predicted_class"],
            fraud_probability=outcome["fraud_probability"],
            confidence=outcome["confidence"],
            uncertainty=outcome["uncertainty"],
            defer_flag=outcome["defer_flag"],
        )
        prediction_id = prediction.id
        CredibilityAnalysis.objects.create(
            advertisement_id=advertisement_id,
            feature_json=credibility["feature_vector"],
            indicator_summary=credibility["summary"],
        )

    response = {
        **outcome,
        "model_version": prediction_result["model_version"],
        "credibility": credibility,
        "prediction_id": prediction_id,
        "disclaimer": LEGITIMACY_DISCLAIMER,
    }
    return Response(response, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_prediction(request, prediction_id):
    try:
        prediction = Prediction.objects.get(pk=prediction_id)
    except Prediction.DoesNotExist:
        return Response({"errors": ["Prediction not found"]}, status=404)
    return Response(PredictionSerializer(prediction).data, status=200)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_explanation(request, prediction_id):
    existing = Explanation.objects.filter(prediction_id=prediction_id).order_by("-created_at").first()
    if existing:
        return Response(existing.explanation_json, status=200)

    try:
        prediction = Prediction.objects.get(pk=prediction_id)
    except Prediction.DoesNotExist:
        return Response({"errors": ["Prediction not found"]}, status=404)

    advertisement = prediction.advertisement
    combined_text = build_combined_text(AdvertisementSerializer(advertisement).data)
    explanation = explanation_service.explain_text(combined_text)

    summary = "; ".join(
        f"{f['token']} ({f['direction']})" for f in explanation.get("top_factors", [])
    ) or "No explanation available yet."
    Explanation.objects.create(
        prediction=prediction, explanation_json=explanation, evidence_summary=summary
    )

    return Response(explanation, status=200)


@api_view(["GET"])
@permission_classes([AllowAny])
def health(request):
    return Response({"status": "ok"}, status=200)
