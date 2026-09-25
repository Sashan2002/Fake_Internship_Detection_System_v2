from rest_framework import serializers
from apps.advertisements.models import Advertisement


class AdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = [
            "id", "user", "title", "description", "requirements", "benefits",
            "company_profile", "employer_name", "location", "department",
            "salary_range", "employment_type", "required_experience",
            "required_education", "industry", "function_field",
            "telecommuting", "has_company_logo", "has_questions", "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def validate_description(self, value):
        if len(value.strip()) < 20:
            raise serializers.ValidationError(
                "description is too short to analyse meaningfully (min 20 characters)"
            )
        return value
