from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from .models import AcademicExperience, Company, CompanyAnswer, CompanyQuestion, Resume, User, Opportunity, \
    Saved, CompanyReview, Language, WorkExperience, AcademicExperience, CompanyQuestion, CompanyAnswer, Application

# User

class UserCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username', 'first_name', 'last_name', 'email', 'password')

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data.pop('password'))
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username', 'first_name', 'last_name', 'email', 'phone_number', 'location')


# Company

class CompanySerializer(serializers.ModelSerializer):
    review_count = serializers.ReadOnlyField()
    review_avg = serializers.ReadOnlyField()

    class Meta:
        model = Company
        fields = ('id', 'name', 'industry', 'description', 'image_url', 'review_count', 'review_avg')


class CompanyReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyReview
        fields = ('id', 'user', 'company', 'identification', 'score', 'review', 'timestamp')

    def create(self, validated_data):
        review = super().create(validated_data)
        review.user = User.objects.get(id = self.context['request'].user.id)
        review.save()
        return review


# Opportunity

class OpportunitySerializer(serializers.ModelSerializer):
    company_name = serializers.SerializerMethodField('get_company_name')

    def get_company_name(self, obj):
        return obj.company.name

    class Meta:
        model = Opportunity
        fields = ('id', 'user', 'company', 'company_name', 'position', 'location', 'description', 'image_url', 'question_1', \
            'question_2', 'question_3', 'question_4', 'question_5', 'is_active', 'applicant_count', 'timestamp')

    def create(self, validated_data):
        opportunity = super().create(validated_data)
        user = User.objects.get(id = self.context['request'].user.id)
        opportunity.user = user
        opportunity.save()
        return opportunity


# Saved

class SavedOpportunitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Saved
        fields = ('id', 'user', 'opportunity', 'timestamp')

    def create(self, validated_data):
        if validated_data['user'].id == self.context['request'].user.id:
            favorite = super().create(validated_data)
            favorite.save()
            return favorite
        else: 
            raise serializers.ValidationError("Error manipulating record")
            

class SavedOpportunitiesExpandedSerializer(serializers.ModelSerializer):
    opportunity = OpportunitySerializer()

    class Meta:
        model = Saved
        fields = ('id', 'user', 'opportunity', 'timestamp')


# Questions and Answers

class CompanyQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyQuestion
        fields = ('id', 'company', 'user', 'question', 'timestamp')

    def create(self, validated_data):
        question = super().create(validated_data)
        question.user = User.objects.get(id = self.context['request'].user.id)
        question.save()
        return question


class CompanyAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyAnswer
        fields = ('id', 'company_question', 'user', 'answer', 'timestamp')

    def create(self, validated_data):
        answer = super().create(validated_data)
        answer.user = User.objects.get(id = self.context['request'].user.id)
        answer.save()
        return answer


# Resume

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ('id', 'user', 'name', 'summary', 'other')

    def create(self, validated_data):
        resume = super().create(validated_data)
        resume.user = User.objects.get(id = self.context['request'].user.id)
        resume.save()
        return resume


class WorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = ('id', 'resume', 'company', 'position', 'location', 'industry', 'start_date', 'end_date', 'description')        

    def create(self, validated_data):
        # Check if resume creator is user logged in
        resumeUser = Resume.objects.get(id = validated_data['resume'].id).user.id

        if resumeUser == self.context['request'].user.id :
            workExperience = super().create(validated_data)
            workExperience.save()
            return workExperience
        raise serializers.ValidationError("Access denied")


class AcademicExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicExperience
        fields = ('id', 'resume', 'school', 'field', 'course', 'location', 'start_date', 'end_date', 'description')

    def create(self, validated_data):
        # Check if resume creator is user logged in
        resumeUser = Resume.objects.get(id = validated_data['resume'].id).user.id

        if resumeUser == self.context['request'].user.id :
            academicExperience = super().create(validated_data)
            academicExperience.save()
            return academicExperience
        raise serializers.ValidationError("Access denied")


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ('id', 'resume', 'name', 'level')

    def create(self, validated_data):
        # Check if resume creator is user logged in
        resumeUser = Resume.objects.get(id = validated_data['resume'].id).user.id

        if resumeUser == self.context['request'].user.id :
            language = super().create(validated_data)
            language.save()
            return language
        raise serializers.ValidationError("Access denied")


class FullResumeSerializer(serializers.ModelSerializer):
    work_experiences = WorkExperienceSerializer(source="wk_experience_resume", many=True, read_only=True)
    academic_experiences = AcademicExperienceSerializer(source="ac_experience_resume", many=True, read_only=True)
    languages = LanguageSerializer(source="language_resume", many=True, read_only=True)

    class Meta:
        model = Resume
        fields = ('id', 'user', 'name', 'summary', 'work_experiences', 'academic_experiences', 'languages', 'other')


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ('id', 'user', 'opportunity', 'resume', 'timestamp', 'answer_1', 'answer_2', 'answer_3', 'answer_4', 'answer_5')

    def create(self, validated_data):
        # Check if user is the one who posted the opportunity
        userDidPost = Opportunity.objects.filter(id = validated_data['opportunity'].id, user__id = self.context['request'].user.id)
        if userDidPost:
            raise serializers.ValidationError("A user cannot apply to an opportunity they have created.")

        # Check if user has already applied
        instance = Application.objects.filter(user__id = self.context['request'].user.id, \
            opportunity__id = validated_data['opportunity'].id)
        if not instance :
            application = super().create(validated_data)
            user = User.objects.get(id = self.context['request'].user.id)
            application.user = user
            application.save()
            return application
        
        raise serializers.ValidationError("Record already exists")

class FullApplicationSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Application
        fields = ('id', 'user', 'opportunity', 'resume', 'timestamp', 'answer_1', 'answer_2', 'answer_3', 'answer_4', 'answer_5')



class AppliedListSerializer(serializers.ModelSerializer):
    opportunity = OpportunitySerializer()
    class Meta:
        model = Application
        fields = ('id', 'user', 'opportunity', 'resume', 'timestamp', 'answer_1', 'answer_2', 'answer_3', 'answer_4', 'answer_5')