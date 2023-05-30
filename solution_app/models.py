from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Calendar(models.Model):
    """Represents the user's calendar"""
    name = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    # end function __str__()
# end class Calendar
    
class Event(models.Model):
    """Represents an event withn a user's calendar"""
    title = models.CharField(max_length=255)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    location = models.CharField(max_length=255)
    description = models.TextField()
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    # end function __str__()
# end class Event

class UserCalendar(models.Model):
    """Store user-specific calendar data"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Tokens obtained during OAuth process for accessing the calendar
    accessToken = models.CharField(max_length=255)
    refreshToken = models.CharField(max_length=255)
    tokenExpiry = models.DateTimeField()

    def __str__(self):
        return self.user.username
    # end function __str__()
# end class UserCalendar