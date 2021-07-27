from django.db import models
from django.contrib.auth.models import User
from courses.models import Course

# Create your models here.

class Messages(models.Model):
    sender = models.ForeignKey(User, related_name="sender", on_delete=models.CASCADE)
    sent_date = models.DateTimeField()
    message = models.TextField()
    course = models.ForeignKey(Course, related_name="course_id", on_delete=models.CASCADE)

    class Meta:
        ordering = ['-sent_date']

    def __str__(self):
        return str(self.sent_date)