from django.urls import path
from .views import (
    CourseCategoryListCreateAPIView,CourseCategorydetailAPIView,
    LearnerBenefitListCreateAPIView,LearnerBenefitDetailAPIView,
    TestimonialListCreateAPIView,TestimonialDetailAPIView,
    FAQListCreateAPIView,FAQDetailAPIView,
    CourseReviewListCreateAPIView,CourseReviewDetailAPIView,
    TrendingCourseListAPIView,TopNewCourseListAPIView,
    CourseListCreateAPIView,CourseDetailAPIView,CourseArchiveAPIView,
    AuthorListCreateAPIView,AuthorDetailAPIView
    )

urlpatterns=[
    path('categories/',CourseCategoryListCreateAPIView.as_view(),name='category-list-create'),
    path('categories/<int:pk>/',CourseCategorydetailAPIView.as_view(),name='category-detail'),

    path('learner-benefits/',LearnerBenefitListCreateAPIView.as_view(),name='learner-benefit-list-create'),
    path('learner-benefits/<int:pk>/',LearnerBenefitDetailAPIView.as_view(),name='learner-benefit-detail'),

    path('reviews/',TestimonialListCreateAPIView.as_view(),name='review-list-create'),
    path('reviews/<int:pk>/',TestimonialDetailAPIView.as_view(),name='review-detail'),

    path('faqs/',FAQListCreateAPIView.as_view(),name='faq-list-create'),
    path('faqs/<int:pk>/',FAQDetailAPIView.as_view(),name='faq-detail'),

    path('course-reviews/',CourseReviewListCreateAPIView.as_view(),name='course-review-list-create'),
    path('course-reviews/<int:pk>/',CourseReviewDetailAPIView.as_view(),name='course-review-detail'),

    path('trending/',TrendingCourseListAPIView.as_view(),name='trending-courses'),
    path('top-new/',TopNewCourseListAPIView.as_view(),name='top-new-courses'),

    path('courses/',CourseListCreateAPIView.as_view(),name='course-list-create'),
    path('courses/<int:pk>/',CourseDetailAPIView.as_view(),name='course-detail'),

    path('courses/<int:pk>/archive/',CourseArchiveAPIView.as_view(),name='course-archive'),

    path('authors/',AuthorListCreateAPIView.as_view(),name="author-list-create"),
    path('authors/<int:pk>/',AuthorDetailAPIView.as_view(),name='author-detail'),


]
