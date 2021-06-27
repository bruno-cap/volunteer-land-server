from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.db.models import F
from django.http import Http404

from .serializers import FullResumeSerializer, FullApplicationSerializer, CompanySerializer, CompanyQuestionSerializer, \
    UserSerializer, OpportunitySerializer, SavedOpportunitiesSerializer, SavedOpportunitiesExpandedSerializer, \
    CompanyReviewSerializer, CompanyAnswerSerializer, UserCreationSerializer, ResumeSerializer, WorkExperienceSerializer, \
    AcademicExperienceSerializer, LanguageSerializer, ApplicationSerializer, FullApplicationSerializer, AppliedListSerializer
from .models import Application, CompanyQuestion, User, Company, Opportunity, Saved, CompanyReview, CompanyAnswer, \
    Resume, WorkExperience, AcademicExperience, Language

# Pagination

class CustomLongPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 20


class CustomShortPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 20


# Users

class UserListView(generics.CreateAPIView):
    serializer_class = UserCreationSerializer


class CurrentUserView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(id = self.request.user.id)


class UpdateCurrentUserView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    lookup_url_kwarg = 'user_id'

    def get_queryset(self):
        if self.request.user.id == self.kwargs['user_id']:
            return User.objects.filter(id = self.kwargs['user_id']) 
        else:
            raise Http404


# Companies

class CompanyListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Company.objects.all().order_by('name')
    serializer_class = CompanySerializer
    pagination_class = CustomLongPagination

    def paginate_queryset(self, queryset, view=None):
        if 'page' not in self.request.query_params:
            return None
        return super().paginate_queryset(queryset)


class CompanyDetailsView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CompanySerializer
    lookup_url_kwarg = 'company_id'

    def get_queryset(self):
        return Company.objects.filter(pk = self.kwargs['company_id'])


class CompanySearchResultsView(generics.ListAPIView):
    serializer_class = CompanySerializer
    pagination_class = CustomLongPagination

    def get_queryset(self):
        name = self.kwargs['company_name'] if self.kwargs['company_name'] != "blank" else ""
        return Company.objects.filter(name__icontains = name)


# Opportunities

class OpportunityListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Opportunity.objects.all().filter(is_active = True).order_by('-timestamp')
    serializer_class = OpportunitySerializer
    pagination_class = CustomLongPagination


class OpportunityDetailsView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = OpportunitySerializer
    lookup_url_kwarg = 'opportunity_id'

    def get_queryset(self):
        return Opportunity.objects.filter(id = self.kwargs['opportunity_id'])

    def destroy(self, request, *args, **kwargs):
        checkRecord = Opportunity.objects.get(id = self.kwargs['opportunity_id'])

        # Check if record exists and logged in user.id is the one that created the listing
        if checkRecord and checkRecord.user.id == self.request.user.id :
            self.perform_destroy(Opportunity.objects.filter(id = self.kwargs['opportunity_id']))
            return Response(status=204)
        else:
            raise Http404        


class OpportunitySearchResultsView(generics.ListAPIView):
    serializer_class = OpportunitySerializer
    pagination_class = CustomLongPagination

    def get_queryset(self):
        position = self.kwargs['opportunity_position'] if self.kwargs['opportunity_position'] != "blank" else ""
        location = self.kwargs['opportunity_location'] if self.kwargs['opportunity_location'] != "blank" else ""
        return Opportunity.objects.filter(position__icontains = position, location__icontains = location)


# Saved

class SavedOpportunitiesView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    lookup_field = 'user'
    lookup_url_kwarg = 'user_id'
    pagination_class = CustomLongPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SavedOpportunitiesExpandedSerializer
        return SavedOpportunitiesSerializer

    def get_queryset(self):
        if self.kwargs['user_id'] == self.request.user.id :            
            return Saved.objects.filter(user__id = self.kwargs['user_id']).order_by('-timestamp')
        else:
            raise Http404


class SingleSavedOpportunityView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SavedOpportunitiesSerializer
    lookup_field = 'opportunity_id'

    def get_queryset(self):
        if self.kwargs['user_id'] == self.request.user.id :
            return Saved.objects.filter(opportunity__id = self.kwargs['opportunity_id'], user__id = self.request.user.id)
        else:
            raise Http404


# Applied

class OpportunitiesAppliedListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AppliedListSerializer
    lookup_url_kwarg = 'user_id'
    lookup_field = 'user__id'
    pagination_class = CustomLongPagination

    def get_queryset(self):
        if self.kwargs['user_id'] == self.request.user.id :            
            return Application.objects.filter(user__id = self.kwargs['user_id']).order_by('-timestamp')
        else:
            raise Http404

class SingleAppliedOpportunityView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AppliedListSerializer
    lookup_field = 'opportunity_id'

    def get_queryset(self):
        if self.kwargs['user_id'] == self.request.user.id :
            return Application.objects.filter(opportunity__id = self.kwargs['opportunity_id'], \
                user__id = self.request.user.id)
        else:
            raise Http404


# Posted

class OpportunitiesPostedView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OpportunitySerializer
    lookup_url_kwarg = 'user_id'
    lookup_field = 'user__id'
    pagination_class = CustomLongPagination

    def get_queryset(self):
        if self.kwargs['user_id'] == self.request.user.id :            
            return Opportunity.objects.filter(user__id = self.kwargs['user_id']).order_by('-timestamp')
        else:
            raise Http404


# Company Reviews

class CompanyReviewListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CompanyReviewSerializer
    lookup_url_kwarg = 'company_id'
    pagination_class = CustomShortPagination

    def get_queryset(self):
        return CompanyReview.objects.filter(company__id = self.kwargs['company_id']).order_by('-timestamp')


class SingleCompanyReviewView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CompanyReviewSerializer
    lookup_url_kwarg = 'review_id'

    def get_queryset(self):
        posterId = CompanyReview.objects.get(id = self.kwargs['review_id']).user.id
        if posterId == self.request.user.id :            
            return CompanyReview.objects.filter(id = self.kwargs['review_id'])
        else:
            raise Http404  


# Company Questions

class CompanyQuestionListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CompanyQuestionSerializer
    lookup_url_kwarg = 'company_id'
    pagination_class = CustomShortPagination

    def get_queryset(self):
        return CompanyQuestion.objects.filter(company__id = self.kwargs['company_id']).order_by('-timestamp')


class SingleCompanyQuestionView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CompanyQuestionSerializer
    lookup_url_kwarg = 'question_id'

    def get_queryset(self):
        posterId = CompanyQuestion.objects.get(id = self.kwargs['question_id']).user.id
        if posterId == self.request.user.id :            
            return CompanyQuestion.objects.filter(id = self.kwargs['question_id'])
        else:
            raise Http404


# Company Answers

class CompanyAnswerListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CompanyAnswerSerializer
    lookup_url_kwarg = 'question_id'
    pagination_class = CustomShortPagination

    def get_queryset(self):
        return CompanyAnswer.objects.filter(company_question__id = self.kwargs['question_id']).order_by('-timestamp')



class SingleCompanyAnswerView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CompanyAnswerSerializer
    lookup_url_kwarg = 'answer_id'

    def get_queryset(self):
        posterId = CompanyAnswer.objects.get(id = self.kwargs['answer_id']).user.id
        if posterId == self.request.user.id :            
            return CompanyAnswer.objects.filter(id = self.kwargs['answer_id'])
        else:
            raise Http404


# Resumes

class ResumeListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ResumeSerializer
    lookup_url_kwarg = 'user_id'
    lookup_field = 'user__id'

    def get_queryset(self):
        if self.kwargs['user_id'] == self.request.user.id :
            return Resume.objects.filter(user__id = self.kwargs['user_id'])
        else:
            raise Http404


class SingleResumeView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'resume_id'
    serializer_class = ResumeSerializer

    # def get_serializer_class(self):
    #     if self.request.method == 'GET':
    #         return FullResumeSerializer
    #     return ResumeSerializer

    def get_queryset(self):
        resumeUser = Resume.objects.get(id = self.kwargs['resume_id']).user.id

        if resumeUser == self.request.user.id:
            return Resume.objects.filter(id = self.kwargs['resume_id'])
        else:
            raise Http404

class SingleResumeRecruiterView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FullResumeSerializer
    lookup_url_kwarg = 'resume_id'

    def get_queryset(self):
        opportunityId = Application.objects.get(id = self.kwargs['application_id']).opportunity.id
        posterId = Opportunity.objects.get(id = opportunityId).user.id

        resumeUserId = Resume.objects.get(id = self.kwargs['resume_id']).user.id

        if posterId == self.request.user.id or resumeUserId == self.request.user.id:
            return Resume.objects.filter(id = self.kwargs['resume_id'])
        else:
            raise Http404


# Resumes - Work Experience

class WorkExperienceListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WorkExperienceSerializer
    lookup_url_kwarg = 'resume_id'
    lookup_field = 'resume__id'

    def get_queryset(self):
        resumeUser = Resume.objects.get(id = self.kwargs['resume_id']).user.id
        if resumeUser == self.request.user.id :
            return WorkExperience.objects.filter(resume__id = self.kwargs['resume_id'])\
                .order_by(F('end_date').desc(nulls_first=True), F('start_date').desc())
        else:
            raise Http404

class WorkExperienceListRecruiterView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WorkExperienceSerializer
    lookup_url_kwarg = 'resume_id'
    lookup_field = 'resume__id'

    def get_queryset(self):
        opportunity = Application.objects.get(id = self.kwargs['application_id']).opportunity.id
        poster = Opportunity.objects.get(id = opportunity).user.id        
        resumeUser = Resume.objects.get(id = self.kwargs['resume_id']).user.id

        if poster == self.request.user.id or resumeUser == self.request.user.id :
            return WorkExperience.objects.filter(resume__id = self.kwargs['resume_id'])\
                .order_by(F('end_date').desc(nulls_first=True), F('start_date').desc())
        else:
            raise Http404


class SingleWorkExperienceView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WorkExperienceSerializer
    lookup_url_kwarg = 'work_experience_id'

    def get_queryset(self):
        resumeId = WorkExperience.objects.get(id = self.kwargs['work_experience_id']).resume.id
        resumeCreatorId = Resume.objects.get(id = resumeId).user.id
        
        if resumeCreatorId == self.request.user.id :
            return WorkExperience.objects.filter(id = self.kwargs['work_experience_id'])
        else:
            raise Http404


# Resumes - Academic Experience

class AcademicExperienceListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AcademicExperienceSerializer
    lookup_url_kwarg = 'resume_id'
    lookup_field = 'resume__id'

    def get_queryset(self):
        resumeUser = Resume.objects.get(id = self.kwargs['resume_id']).user.id
        if resumeUser == self.request.user.id :
            return AcademicExperience.objects.filter(resume__id = self.kwargs['resume_id'])\
                .order_by(F('end_date').desc(nulls_first=True), F('start_date').desc())
        else:
            raise Http404



class AcademicExperienceListRecruiterView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AcademicExperienceSerializer
    lookup_url_kwarg = 'resume_id'
    lookup_field = 'resume__id'

    def get_queryset(self):
        opportunity = Application.objects.get(id = self.kwargs['application_id']).opportunity.id
        poster = Opportunity.objects.get(id = opportunity).user.id     
        resumeUser = Resume.objects.get(id = self.kwargs['resume_id']).user.id

        if poster == self.request.user.id or resumeUser == self.request.user.id :
            return AcademicExperience.objects.filter(resume__id = self.kwargs['resume_id'])\
                .order_by(F('end_date').desc(nulls_first=True), F('start_date').desc())
        else:
            raise Http404



class SingleAcademicExperienceView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AcademicExperienceSerializer
    lookup_url_kwarg = 'academic_experience_id'

    def get_queryset(self):
        resumeId = AcademicExperience.objects.get(id = self.kwargs['academic_experience_id']).resume.id
        resumeCreatorId = Resume.objects.get(id = resumeId).user.id
        
        if resumeCreatorId == self.request.user.id :
            return AcademicExperience.objects.filter(id = self.kwargs['academic_experience_id'])
        else:
            raise Http404


# Resumes - Language Experience

class LanguageListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LanguageSerializer
    lookup_url_kwarg = 'resume_id'
    lookup_field = 'resume__id'

    def get_queryset(self):
        resumeUser = Resume.objects.get(id = self.kwargs['resume_id']).user.id
        if resumeUser == self.request.user.id :
            return Language.objects.filter(resume__id = self.kwargs['resume_id'])
        else:
            raise Http404

class LanguageListRecruiterView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LanguageSerializer
    lookup_url_kwarg = 'resume_id'
    lookup_field = 'resume__id'

    def get_queryset(self):
        opportunity = Application.objects.get(id = self.kwargs['application_id']).opportunity.id
        poster = Opportunity.objects.get(id = opportunity).user.id        
        resumeUser = Resume.objects.get(id = self.kwargs['resume_id']).user.id

        if poster == self.request.user.id or resumeUser == self.request.user.id :
            return Language.objects.filter(resume__id = self.kwargs['resume_id'])
        else:
            raise Http404


class SingleLanguageView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LanguageSerializer
    lookup_url_kwarg = 'language_id'

    def get_queryset(self):
        resumeId = Language.objects.get(id = self.kwargs['language_id']).resume.id
        resumeCreatorId = Resume.objects.get(id = resumeId).user.id
        
        if resumeCreatorId == self.request.user.id :
            return Language.objects.filter(id = self.kwargs['language_id'])
        else:
            raise Http404


# Applications

class ApplicationsView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    lookup_field = 'opportunity__id'
    lookup_url_kwarg = 'opportunity_id'

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return FullApplicationSerializer
        return ApplicationSerializer

    def get_queryset(self):
        opportunityCreator = Opportunity.objects.get(id = self.kwargs['opportunity_id']).user.id
        if opportunityCreator == self.request.user.id :   
            return Application.objects.filter(opportunity__id = self.kwargs['opportunity_id']).order_by('-timestamp')
        else:
            raise Http404


class SingleApplicationView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'application_id'

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return FullApplicationSerializer
        return ApplicationSerializer

    def get_queryset(self):
        applicationInstance = Application.objects.get(id = self.kwargs['application_id'])
        opportunityId = applicationInstance.opportunity.id
        opportunityInstance = Opportunity.objects.get(id = opportunityId)

        applicationUser = applicationInstance.user.id
        posterUser = opportunityInstance.user.id

        if self.request.user.id == applicationUser or self.request.user.id == posterUser:
            return Application.objects.filter(id = self.kwargs['application_id'])
        else:
            raise Http404

    def destroy(self, request, *args, **kwargs):
        applicationInstance = Application.objects.get(id = self.kwargs['application_id'])
        applicationUser = applicationInstance.user.id

        if applicationUser == self.request.user.id :
            self.perform_destroy(Application.objects.filter(id = self.kwargs['application_id']))
            return Response(status=204)
        else:
            raise Http404