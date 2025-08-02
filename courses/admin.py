from django.contrib import admin
from .models import (
    Course,CourseCategory,LearnerBenefit,Testimonial,FAQ,CourseReview,
    Author,LearningOutcome,CourseInclude,CourseMaterial
)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display=("title","category","discounted_price","is_archived","created_at")
    search_fields=("title",)
    list_filter=("category","is_archived")

admin.site.register(CourseCategory)
admin.site.register(LearnerBenefit)
admin.site.register(Testimonial)
admin.site.register(FAQ)
admin.site.register(CourseReview)
admin.site.register(Author)
admin.site.register(LearningOutcome)
admin.site.register(CourseInclude)
admin.site.register(CourseMaterial)