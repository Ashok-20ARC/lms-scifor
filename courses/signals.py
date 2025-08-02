from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from .models import CourseReview

@receiver(post_save,sender=CourseReview)
def update_course_rating_on_save(sender,instance,**kwargs):
    instance.course.update_rating_stats()

@receiver(post_delete,sender=CourseReview)
def update_course_rating_on_delete(sender,instance,**kwargs):
    instance.course.update_rating_stats()