from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Problem(models.Model):
    error_name = models.CharField(max_length = 500, default = 'error')
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    pro_lang = models.CharField(max_length=20)
    framework_library = models.CharField(max_length=20)
    count = models.IntegerField(default = 0)
    date_time = models.DateTimeField(default = datetime.now ,blank=False)

        
class Solution(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    problem = models.ForeignKey(Problem, null=True, on_delete=models.SET_NULL)
    solution_link = models.URLField()
    text_sol = models.TextField()
    remark = models.CharField(max_length=500)