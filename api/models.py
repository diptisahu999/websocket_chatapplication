from django.db import models

# Create your models here.

# Create your models here.
class chat(models.Model):
    content=models.CharField(max_length=500)
    timestamp=models.DateTimeField(auto_now=True)
    group=models.ForeignKey('Group',on_delete=models.CASCADE)
    

class Group(models.Model):
    name=models.CharField(max_length=1000)

    def __str__(self):
        return self.name
