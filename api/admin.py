from django.contrib import admin
from .models import User, Company, CompanyReview, Saved, CompanyQuestion, CompanyAnswer, Resume, WorkExperience, \
    AcademicExperience, Language, Opportunity, Application

admin.site.register(User)
admin.site.register(Company)
admin.site.register(CompanyReview)
admin.site.register(Opportunity)
admin.site.register(Application)
admin.site.register(Saved)
admin.site.register(CompanyQuestion)
admin.site.register(CompanyAnswer)
admin.site.register(Resume)
admin.site.register(WorkExperience)
admin.site.register(AcademicExperience)
admin.site.register(Language)