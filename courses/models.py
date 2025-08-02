from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator,MaxValueValidator
from django.utils import timezone
from datetime import timedelta

class CourseCategory(models.Model):
    name=models.CharField(max_length=100,unique=True)
    description=models.TextField(blank=True)
    image=models.ImageField(upload_to='category_images/',null=True,blank=True)
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Author(models.Model):
    name=models.CharField()
    bio=models.TextField()
    rating=models.PositiveIntegerField(default=0)
    total_reviews=models.PositiveIntegerField(default=0)
    profile_image=models.ImageField(upload_to="author_images/",null=True,blank=True)
    organization=models.CharField(max_length=255,null=True,blank=True)
    
class Course(models.Model):
    category=models.ForeignKey(CourseCategory,related_name='courses',on_delete=models.CASCADE,null=True,blank=True)
    title=models.CharField(max_length=255)

    short_description=models.CharField(max_length=255,null=True)
    long_description=models.TextField(null=True,blank=True)

    assignment_count=models.PositiveIntegerField(default=0)
    certificate_of_achievement=models.BooleanField(default=True)
    lifetime_access=models.BooleanField(default=True)
    live_record_session=models.BooleanField(default=True)

    author_name=models.ForeignKey(Author,related_name='courses',on_delete=models.SET_NULL,null=True)
    duration=models.CharField(max_length=50)
    
    original_price=models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    discounted_price=models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    discounted_percentage=models.PositiveIntegerField(null=True,blank=True)
    discount_end_date=models.DateTimeField(null=True,blank=True)

    average_rating=models.FloatField(default=0.0)
    review_count=models.PositiveIntegerField(default=0)
    image=models.ImageField(upload_to="course_images/",blank=True,null=True)

    is_top_author=models.BooleanField(default=False)
    is_editor_choice=models.BooleanField(default=False)
    is_best_seller=models.BooleanField(default=False)

    is_trending = models.BooleanField(default=False)
    is_new = models.BooleanField(default=True)

    is_archived=models.BooleanField(default=False)
    created_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def update_rating_stats(self):
        reviews=self.reviews.all()
        self.review_count=reviews.count()
        self.average_rating=reviews.aggregate(models.Avg('rating'))['rating__avg'] or 0
        self.save()

    def is_discount_active(self):
        return self.discount_end_date and timezone.now() < self.discount_end_date
    
    def get_time_left_for_discount(self):
        if self.discount_end_date and timezone.now() < self.discount_end_date:
            return self.discount_end_date-timezone.now()
        return timedelta(0)
    
    def get_discount_days_left_text(self):
        if self.discount_end_date and timezone.now() < self.discount_end_date:
            days_left=(self.discount_end_date.date()-timezone.now().date()).days

            if days_left==1:
                return "1 day left"
            elif days_left>1:
                return f"{days_left} days left"
            return "Offer Expired"
        
    def save(self,*args,**kwargs):
        if self.discounted_percentage and self.original_price:
            self.discounted_price=self.original_price * (1-self.discounted_percentage/100)
            super().save(*args,**kwargs)

    def __str__(self):
        return self.title
    
class LearningOutcome(models.Model):
    course=models.ForeignKey(Course,related_name='outcomes',on_delete=models.CASCADE)
    point=models.CharField(max_length=255)

class CourseInclude(models.Model):
    course=models.ForeignKey(Course,related_name='includes',on_delete=models.CASCADE)
    icon=models.CharField(max_length=100,help_text="Enter a Font Awesome icon class (e.g., 'fa-certificate')") # name of icon or type
    label=models.CharField(max_length=255)

class CourseMaterial(models.Model):
    course=models.ForeignKey(Course,related_name='materials',on_delete=models.CASCADE)
    title=models.CharField(max_length=255)
    content=models.TextField(null=True,blank=True)
    file=models.FileField(upload_to='course_materials/',blank=True,null=True)

class LearnerBenefit(models.Model):
    title=models.CharField(max_length=100)
    description=models.TextField()
    icon=models.ImageField(upload_to='benefit_icons/',null=True,blank=True)

    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Testimonial(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    role=models.CharField(max_length=100)
    comment=models.TextField()
    photo=models.ImageField(upload_to='testimonial_photos/',null=True,blank=True)
    rating=models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)],default=5)

    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.full_name} - {self.role}"

class FAQ(models.Model):
    question=models.CharField(max_length=255)
    answer=models.TextField()
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question
    
class CourseReview(models.Model):
    course=models.ForeignKey('Course',related_name='reviews',on_delete=models.CASCADE)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    rating=models.IntegerField(choices=[(i,i) for i in range(1,6)])
    comment=models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.course} - {self.rating}"
