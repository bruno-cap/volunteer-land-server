from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models import Avg


class User(AbstractUser):
    location = models.CharField(max_length=50, blank=True)
    phone_number = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f"{self.username}"


class Company(models.Model):
    name = models.CharField(max_length=100, unique=True)
    industry = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    image_url = models.CharField(max_length=200, blank=True)

    @property
    def review_count(self):
        return CompanyReview.objects.filter(company__id=self.id).count(),

    @property
    def review_avg(self):
        return CompanyReview.objects.filter(company__id=self.id).aggregate(Avg('score'))['score__avg']

    def __str__(self):
        return f"{self.name}"


class CompanyReview(models.Model):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="review_company_name")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="review_user", null=True)
    identification = models.CharField(max_length=50)
    score = models.DecimalField(max_digits=2, decimal_places=1)
    review = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Review #{self.id} - {self.company.name}"


class Opportunity(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="opportunity_poster", null=True)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="company_name")
    position = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    image_url = models.CharField(max_length=200)
    question_1 = models.TextField(blank=True)
    question_2 = models.TextField(blank=True)
    question_3 = models.TextField(blank=True)
    question_4 = models.TextField(blank=True)
    question_5 = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def review_count(self):
        return CompanyReview.objects.filter(company__id=self.id).count(),

    @property
    def review_avg(self):
        return CompanyReview.objects.filter(company__id=self.id).aggregate(Avg('score'))['score__avg']

    @property
    def applicant_count(self):
        return Application.objects.filter(opportunity__id=self.id).count(),

    def __str__(self):
        return f"Opportunity #{self.id} - {self.position} at {self.company.name}"


# Saved

class Saved(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="saved_user", null=True)
    opportunity = models.ForeignKey(
        Opportunity, on_delete=models.CASCADE, related_name="saved_opportunity")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Opportunity #{self.id} - Saved by {self.user.username}"


# Questions and Answers

class CompanyQuestion(models.Model):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="company_question_company")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="company_question_user", null=True)
    question = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Question #{self.id} - Asked by {self.user.username}"


class CompanyAnswer(models.Model):
    company_question = models.ForeignKey(
        CompanyQuestion, on_delete=models.CASCADE, related_name="company_answer_question")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="company_answer_user", null=True)
    answer = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer #{self.id} - Answered by {self.user.username}"


# Resumes

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE,
                             related_name="resume_user", null=True)
    name = models.CharField(max_length=1000)
    summary = models.TextField(null=True)
    other = models.TextField(null=True)

    def __str__(self):
        return f"Resume #{self.id} - {self.name} by {self.user.username}"


class Language(models.Model):
    resume = models.ForeignKey(
        Resume, on_delete=CASCADE, related_name="language_resume")
    name = models.CharField(max_length=50)
    level = models.CharField(max_length=20)

    def __str__(self):
        return f"Language #{self.id} -> Resume #{self.resume.id}"


class WorkExperience(models.Model):
    resume = models.ForeignKey(
        Resume, on_delete=models.CASCADE, related_name="wk_experience_resume")
    company = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    industry = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField(null=True)
    description = models.CharField(max_length=500)
    
    def __str__(self):
        return f"Work Experience #{self.id} -> Resume #{self.resume.id}"


class AcademicExperience(models.Model):
    resume = models.ForeignKey(
        Resume, on_delete=models.CASCADE, related_name="ac_experience_resume")
    school = models.CharField(max_length=50)
    field = models.CharField(max_length=50)
    course = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField(null=True)
    description = models.CharField(max_length=500)

    def __str__(self):
        return f"Academic Experience #{self.id} -> Resume #{self.resume.id}"


# Applications

class Application(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="applicant", null=True, blank=True)
    opportunity = models.ForeignKey(
        Opportunity, on_delete=models.CASCADE, related_name="application_opportunity")
    resume = models.ForeignKey(
        Resume, on_delete=models.CASCADE, related_name="application_resume", null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    answer_1 = models.TextField(blank=True)
    answer_2 = models.TextField(blank=True)
    answer_3 = models.TextField(blank=True)
    answer_4 = models.TextField(blank=True)
    answer_5 = models.TextField(blank=True)

    def __str__(self):
        return f"Application #{self.id} by {self.user.username}"