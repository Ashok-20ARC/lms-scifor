from rest_framework import serializers
from .models import (
    CourseCategory,LearnerBenefit,Testimonial,FAQ,CourseReview,Course,
    Author,LearningOutcome,CourseInclude,CourseMaterial
)

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Author
        fields=["name","bio","rating","total_reviews","profile_image","organization"]

class LearningOutcomeSerializer(serializers.ModelSerializer):
    class Meta:
        model=LearningOutcome
        fields=["point"]
    
class CourseIncludeSerializer(serializers.ModelSerializer):
    class Meta:
        model=CourseInclude
        fields=["icon","label"]

class CourseMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model=CourseMaterial
        fields=["title","content","file"]

class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=CourseCategory
        fields="__all__"

class LearnerBenefitSerializer(serializers.ModelSerializer):
    class Meta:
        model=LearnerBenefit
        fields=['id','title','description','icon','is_active']
    
class TestimonialSerializer(serializers.ModelSerializer):
    name=serializers.SerializerMethodField()

    class Meta:
        model=Testimonial
        fields=['id','name','role','comment','photo','rating','is_active']
        read_only_fields=['name']

    def get_name(self,obj):
        return obj.user.full_name
    
class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model=FAQ
        fields='__all__'

class CourseReviewSerializer(serializers.ModelSerializer):
    user_name=serializers.CharField(source='user.full_name',read_only=True)
    created_at=serializers.DateTimeField(format="%d %b %Y",read_only=True)

    class Meta:
        model=CourseReview
        fields=['user_name','rating','comment','created_at']
        read_only_fields=['user','created_at']

class CourseDetailSerializer(serializers.ModelSerializer):
    author_name=AuthorSerializer(read_only=True)
    includes=CourseIncludeSerializer(many=True,read_only=True)
    materials=CourseMaterialSerializer(many=True,read_only=True)
    outcomes=LearningOutcomeSerializer(many=True,read_only=True)
    reviews=CourseReviewSerializer(many=True,read_only=True,source='reviews.all')
    discount_days_left=serializers.SerializerMethodField()

    class Meta:
        model=Course
        fields=[
            "id","title","category","short_description","long_description",
            "assignment_count","certificate_of_achievement","lifetime_access",
            "live_record_session","author_name","duration",
            "original_price","discounted_price","discounted_percentage",
            "discount_end_date","discount_days_left",
            "average_rating","review_count","image",
            "is_top_author","is_editor_choice","is_best_seller",
            "includes","materials","outcomes","reviews",
        ]
    
    def get_discount_days_left(self,obj):
        return obj.get_discount_days_left_text()

class CourseListSerializer(serializers.ModelSerializer):
    class Meta:
        model=Course
        fields=['id','title','author_name','duration','discounted_price','original_price','average_rating','review_count','is_top_author','is_editor_choice','is_best_seller','image']