from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Topic(models.Model):
    """A topic the user is learning about"""
    text = models.CharField(max_length = 200)
    date_added = models.DateTimeField(auto_now_add = True)
    owner = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        """Return a string representation of the model"""
        return self.text


#Creating an Entry Model that can be nested under a Topic
class Entry(models.Model):
    """Something specific learned about a topic"""
    topic = models.ForeignKey(Topic, on_delete = models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add = True)


    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        """Return a simple string representing the entry."""
        if len(self.text) > 50: 
            return f"{self.text[:50]}..."
        
        #The ellipsis (...) is to remind the UI that we're not presenting the entire entry. Well. It shows anyway even if you have less than 50 characters so woops oh well.

        else:
            return f"{self.text}"