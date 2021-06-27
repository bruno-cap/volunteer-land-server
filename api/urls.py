from django.urls import include, path
from . import views


urlpatterns = [
    # User
    path("newuser", views.UserListView.as_view(), name="new_user"),
    path("currentuser", views.CurrentUserView.as_view(), name="current_user"),
    path("user/<int:user_id>", views.UpdateCurrentUserView.as_view(), name="user_update"),

    # Opportunity
    path("opportunities", views.OpportunityListView.as_view(), name="opportunities"),
    path("opportunity/<int:opportunity_id>", views.OpportunityDetailsView.as_view(), name="single_opportunity"),
    path("opportunitysearch/<str:opportunity_position>/in/<str:opportunity_location>", \
        views.OpportunitySearchResultsView.as_view(), name="opportunity_search_results"),

    # Saved
    path("user/<int:user_id>/opportunitiessaved", views.SavedOpportunitiesView.as_view(), name="saved_opportunities"),
    path("user/<int:user_id>/opportunitysaved/<int:opportunity_id>", views.SingleSavedOpportunityView.as_view(), \
        name="single_saved_opportunity"),
    
    # Posted
    path("user/<int:user_id>/opportunitiesposted", views.OpportunitiesPostedView.as_view(), name="opportunities_posted"),

    # Applied
    path("user/<int:user_id>/opportunitiesapplied", views.OpportunitiesAppliedListView.as_view(), name="opportunities_applied"),
    path("user/<int:user_id>/opportunityapplied/<int:opportunity_id>", views.SingleAppliedOpportunityView.as_view(), \
        name="single_applied_opportunity"),
        
    # Applications
    path("opportunity/<int:opportunity_id>/applications", views.ApplicationsView.as_view(), name="applications"),
    path("application/<int:application_id>", views.SingleApplicationView.as_view(), name="single_application"),

    # Company
    path("companies", views.CompanyListView.as_view(), name="companies"),
    path("company/<int:company_id>", views.CompanyDetailsView.as_view(), name="single_company"),
    path("companysearch/<str:company_name>", views.CompanySearchResultsView.as_view(), name="company_search_results"),

    # Resumes
    path("user/<int:user_id>/resumes", views.ResumeListView.as_view(), name="resume_list"),
    path("resume/<int:resume_id>", views.SingleResumeView.as_view(), name="single_resume"),
    
    # Work Experiences
    path("resume/<int:resume_id>/workexperiences", views.WorkExperienceListView.as_view(), name="work_experiences"),
    path("resume/<int:resume_id>/workexperience/<int:work_experience_id>", views.SingleWorkExperienceView.as_view(), \
        name="single_work_experience"),
    
    # Academic Experiences
    path("resume/<int:resume_id>/academicexperiences", views.AcademicExperienceListView.as_view(), name="academic_experiences"),
    path("resume/<int:resume_id>/academicexperience/<int:academic_experience_id>", views.SingleAcademicExperienceView.as_view(), \
        name="single_academic_experience"),
   
    # Languages
    path("resume/<int:resume_id>/languages", views.LanguageListView.as_view(), name="languages"),
    path("resume/<int:resume_id>/language/<int:language_id>", views.SingleLanguageView.as_view(), name="single_language"),

    # Recruiter views to access resume, work experiences, academic experiences, and languages
    path("application/<int:application_id>/resume/<int:resume_id>", views.SingleResumeRecruiterView.as_view(), name="single_resume_recruiter"),
    path("application/<int:application_id>/resume/<int:resume_id>/workexperiences", views.WorkExperienceListRecruiterView.as_view(), name="work_experience_list_recruiter"),
    path("application/<int:application_id>/resume/<int:resume_id>/academicexperiences", views.AcademicExperienceListRecruiterView.as_view(), name="academic_experience_list_recruiter"),
    path("application/<int:application_id>/resume/<int:resume_id>/languages", views.LanguageListRecruiterView.as_view(), name="language_list_recruiter"),

    # Company Reviews
    path("company/<int:company_id>/reviews", views.CompanyReviewListView.as_view(), name="company_reviews"),
    path("company/<int:company_id>/review/<int:review_id>", views.SingleCompanyReviewView.as_view(), name="single_company_review"),

    # Company Questions
    path("company/<int:company_id>/questions", views.CompanyQuestionListView.as_view(), name="company_questions"),
    path("company/<int:company_id>/question/<int:question_id>", views.SingleCompanyQuestionView.as_view(), \
        name="single_company_question"),

    # Company Answers
    path("question/<int:question_id>/answers", views.CompanyAnswerListView.as_view(), name="company_answers"),
    path("question/<int:question_id>/answer/<int:answer_id>", views.SingleCompanyAnswerView.as_view(), name="single_company_answer"),
]