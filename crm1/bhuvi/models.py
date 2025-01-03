from django.db import models
from django.utils import timezone

class Record(models.Model):
	created_at = models.DateTimeField(default=timezone.now)
	first_name = models.CharField(max_length=50)
	last_name =  models.CharField(max_length=50)
	email =  models.CharField(max_length=100)
	phone = models.CharField(max_length=15)
	address =  models.CharField(max_length=100)
	city =  models.CharField(max_length=50)
	state =  models.CharField(max_length=50)
	zipcode =  models.CharField(max_length=20)

	def _str_(self):
		return(f"{self.first_name} {self.last_name}")

from django.db import models
from django.contrib.auth.models import User

class TimeStampedModel(models.Model):
    """Abstract base class that adds created_at and updated_at fields to models."""
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True