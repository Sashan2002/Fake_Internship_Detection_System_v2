"""
`advertisements` table (Section 5 / Table 2), via Django ORM instead of
raw schema.sql (Django migrations are the source of truth for schema in
this build - see docs/system_architecture.md).
"""
from django.conf import settings
from django.db import models


class Advertisement(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="advertisements")
    title = models.CharField(max_length=500)
    description = models.TextField()
    requirements = models.TextField(blank=True, null=True)
    benefits = models.TextField(blank=True, null=True)
    company_profile = models.TextField(blank=True, null=True)
    employer_name = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    department = models.CharField(max_length=255, blank=True, null=True)
    salary_range = models.CharField(max_length=255, blank=True, null=True)
    employment_type = models.CharField(max_length=100, blank=True, null=True)
    required_experience = models.CharField(max_length=100, blank=True, null=True)
    required_education = models.CharField(max_length=100, blank=True, null=True)
    industry = models.CharField(max_length=255, blank=True, null=True)
    function_field = models.CharField(max_length=255, blank=True, null=True)
    telecommuting = models.BooleanField(default=False)
    has_company_logo = models.BooleanField(default=False)
    has_questions = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def to_ml_record(self) -> dict:
        """
        Shape this row into the field set ml/backend preprocessing expects
        (mirrors backend/utils/preprocessing.build_advertisement_record
        from the Flask build).
        """
        return {
            "title": self.title,
            "location": self.location,
            "department": self.department,
            "salary_range": self.salary_range,
            "company_profile": self.company_profile,
            "description": self.description,
            "requirements": self.requirements,
            "benefits": self.benefits,
            "telecommuting": int(bool(self.telecommuting)),
            "has_company_logo": int(bool(self.has_company_logo)),
            "has_questions": int(bool(self.has_questions)),
            "employment_type": self.employment_type,
            "required_experience": self.required_experience,
            "required_education": self.required_education,
            "industry": self.industry,
            "function_field": self.function_field,
            "employer_name": self.employer_name,
        }
