from django.shortcuts import render,get_object_or_404
from rest_framework import generics,permissions,status
from django.utils import timezone
from datetime import timedelta
from .models import (
    CourseCategory,LearnerBenefit,Testimonial,FAQ,CourseReview,Course,Author
)
from .serializers import (
    CourseCategorySerializer,LearnerBenefitSerializer,TestimonialSerializer,FAQSerializer,CourseReviewSerializer,
    CourseListSerializer,CourseDetailSerializer,AuthorSerializer
)
from .permissions import IsCourseManager,IsAdminUser,canArchiveCourse,canDeleteCourse
from rest_framework.views import APIView
from rest_framework.response import Response

class CourseCategoryListCreateAPIView(APIView):
    def get(self,request):
        categories=CourseCategory.objects.filter(is_active=True)
        serializer=CourseCategorySerializer(categories,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer=CourseCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=201)
        return Response(serializer.errors,status=400)
    
class CourseCategorydetailAPIView(APIView):
    def get_object(self,pk):
        try:
            return CourseCategory.objects.get(pk=pk)
        except CourseCategory.DoesNotExist:
            return None
        
    def get(self,request,pk):
        category=self.get_object(pk)
        if not category:
            return Response({'error':'Category not found'},status=404)
        serializer=CourseCategorySerializer(category)
        return Response(serializer.data)
    
    def put(self,request,pk):
        category=self.get_object(pk)
        if not category:
            return Response({'error':'Category not found'},status=404)
        serializer=CourseCategorySerializer(category,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=400)
    
    def delete(self,request,pk):
        category=self.get_object(pk)
        if not category:
            return Response({'error':'Category not found'},status=404)
        category.delete()
        return Response({'message':'Category deleted'},status=204)
    
class LearnerBenefitListCreateAPIView(generics.ListCreateAPIView):
    queryset=LearnerBenefit.objects.filter(is_active=True)
    serializer_class=LearnerBenefitSerializer
    permission_classes=[permissions.IsAuthenticatedOrReadOnly]

class LearnerBenefitDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset=LearnerBenefit.objects.all()
    serializer_class=LearnerBenefitSerializer
    permission_classes=[permissions.IsAuthenticated]

class TestimonialListCreateAPIView(generics.ListCreateAPIView):
    queryset=Testimonial.objects.filter(is_active=True)
    serializer_class=TestimonialSerializer
    permission_classes=[permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
    
class TestimonialDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Testimonial.objects.all()
    serializer_class=TestimonialSerializer
    permission_classes=[permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        return serializer.save(user=self.request.user)

class FAQListCreateAPIView(generics.ListCreateAPIView):
    queryset=FAQ.objects.filter(is_active=True)
    serializer_class=FAQSerializer
    permission_classes=[permissions.IsAuthenticatedOrReadOnly]

class FAQDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset=FAQ.objects.all()
    serializer_class=FAQSerializer
    permission_classes=[permissions.IsAuthenticatedOrReadOnly]

class CourseReviewListCreateAPIView(generics.ListCreateAPIView):
    queryset=CourseReview.objects.all()
    serializer_class=CourseReviewSerializer
    permission_classes=[permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self,serializer):
        serializer.save(user=self.request.user)

class CourseReviewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset=CourseReview.objects.all()
    serializer_class=CourseReviewSerializer
    permission_classes=[permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self,serializer):
        serializer.save(user=self.request.user)

class CourseListCreateAPIView(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def get(self,request):
        courses=Course.objects.filter(is_archived=False)
        serializer=CourseListSerializer(courses,many=True,context={'request':request})
        return Response(serializer.data)
    
    def post(self,request):
        if not IsCourseManager().has_permission(request,self):
            return Response({'error':'You do not have permission to create courses.'},status=403)
        
        serializer=CourseDetailSerializer(data=request.data,context={'request':request})
        if serializer.is_valid():
            course=serializer.save(created_by=request.user)
            return Response(CourseDetailSerializer(course,context={'request':request}).data,status=201)
        return Response(serializer.errors,status=400)
    
class CourseDetailAPIView(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def get_object(self,pk):
        return get_object_or_404(Course,pk=pk)
    
    def get(self,request,pk):
        course=self.get_object(pk)
        serializer=CourseDetailSerializer(course,context={'request':request})
        return Response(serializer.data)
    
    def put(self,request,pk):
        course=self.get_object(pk)
        if not IsCourseManager().has_permission(request,self):
            return Response({'error':'You do not have permission to edit courses.'},status=403)
        serializer=CourseDetailSerializer(course,data=request.data,context={'request':request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=400)
    
    def patch(self,request,pk):
        course=self.get_object(pk)

        if not IsCourseManager().has_permission(request,self):
            return Response({'error':'You do not have permission to edit courses.'},status=403)
        
        serializer=CourseDetailSerializer(course,data=request.data,partial=True,context={'request':request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=400)
    
    def delete(self,request,pk):
        course=self.get_object(pk)
        if not canDeleteCourse().has_object_permission(request,self,course):
            return Response({'error':'You are not allowed to delete this course.'},status=403)
        course.delete()
        return Response({'detail':'Course deleted successfully'},status=204)
    
class CourseArchiveAPIView(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def post(self,request,pk):
        course=get_object_or_404(Course,pk)
        if not canArchiveCourse().has_object_permission(request,self,course):
            return Response({'error':'You are not allowed to archive this course.'},status=403)
        
        course.is_archived=True
        course.save()
        return Response({'message':'Course archived successfully.'})


class TrendingCourseListAPIView(generics.ListAPIView):
    queryset=Course.objects.filter(is_trending=True,is_archived=False).order_by('-average_rating','-created_at')
    serializer_class=CourseListSerializer

class TopNewCourseListAPIView(generics.ListAPIView):
    serializer_class=CourseListSerializer

    def get_queryset(self):
        thirty_days_ago=timezone.now()-timedelta(days=30)
        return Course.objects.filter(
            created_at__gte=thirty_days_ago,is_archived=False).order_by('-average_rating','-created_at')
    

class AuthorListCreateAPIView(generics.ListCreateAPIView):
    queryset=Author.objects.all()
    serializer_class=AuthorSerializer
    permission_classes=[permissions.IsAuthenticated,permissions.IsAdminUser]

class AuthorDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Author.objects.all()
    serializer_class=AuthorSerializer
    permission_classes=[permissions.IsAuthenticated,permissions.IsAdminUser]
