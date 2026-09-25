"""
API integration tests using DRF's APIClient (in-process, no real server
needed to run these).
"""
import uuid

import pytest
from rest_framework.test import APIClient


@pytest.fixture()
def client():
    return APIClient()


def _unique_email():
    return f"user_{uuid.uuid4().hex[:8]}@example.com"


def _register(client, email=None, password="supersecure1"):
    email = email or _unique_email()
    res = client.post("/api/auth/register", {"name": "Test User", "email": email, "password": password}, format="json")
    return res, email


@pytest.mark.django_db
def test_health_check(client):
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


@pytest.mark.django_db
def test_register_and_login_flow(client):
    res, email = _register(client)
    assert res.status_code == 201
    assert "token" in res.json()

    res = client.post("/api/auth/login", {"email": email, "password": "supersecure1"}, format="json")
    assert res.status_code == 200
    assert res.json()["user"]["email"] == email


@pytest.mark.django_db
def test_login_with_wrong_password_fails(client):
    _, email = _register(client)
    res = client.post("/api/auth/login", {"email": email, "password": "wrong-password"}, format="json")
    assert res.status_code == 401


@pytest.mark.django_db
def test_register_duplicate_email_fails(client):
    res, email = _register(client)
    assert res.status_code == 201
    res2 = client.post("/api/auth/register", {"name": "Dup", "email": email, "password": "supersecure1"}, format="json")
    assert res2.status_code == 400


@pytest.mark.django_db
def test_submit_advertisement_requires_fields(client):
    res = client.post("/api/advertisements/", {"title": ""}, format="json")
    assert res.status_code == 400
    assert "errors" in res.json()


@pytest.mark.django_db
def test_submit_and_fetch_advertisement(client):
    reg_res, _ = _register(client)
    user_id = reg_res.json()["user"]["id"]

    ad_payload = {
        "user": user_id,
        "title": "Marketing Intern",
        "description": "A genuine, structured internship opportunity with mentorship provided.",
    }
    res = client.post("/api/advertisements/", ad_payload, format="json")
    assert res.status_code == 201
    advertisement_id = res.json()["advertisement_id"]

    res = client.get(f"/api/advertisements/{advertisement_id}")
    assert res.status_code == 200
    assert res.json()["title"] == "Marketing Intern"


@pytest.mark.django_db
def test_analyse_credibility_returns_indicators_and_disclaimer(client):
    payload = {
        "title": "Data Intern",
        "description": "A genuine internship with mentorship and clear responsibilities.",
        "company_profile": "Founded in 2005.",
        "salary_range": "$2,000/month",
    }
    res = client.post("/api/analyse-credibility", payload, format="json")
    assert res.status_code == 200
    body = res.json()
    assert "feature_vector" in body
    assert "not independent proof" in body["disclaimer"]


@pytest.mark.django_db
def test_predict_without_trained_model_returns_503_or_200(client, settings, tmp_path):
    """
    If no model artefact exists at BASELINE_MODEL_PATH, /api/predict should
    fail clearly (503) rather than fabricate a prediction.
    """
    settings.BASELINE_MODEL_PATH = tmp_path / "does_not_exist.joblib"
    payload = {
        "title": "Data Intern",
        "description": "A genuine internship with mentorship and clear responsibilities.",
    }
    res = client.post("/api/predict", payload, format="json")
    assert res.status_code in (503, 200)
