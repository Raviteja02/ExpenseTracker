from django.db import models
from datetime import date
# Create your models here.

class Group(models.Model):
    GroupName = models.CharField(max_length=20)


class GroupMembers(models.Model):
    GroupId = models.ForeignKey(Group, on_delete=models.CASCADE)
    Name = models.CharField(max_length=30)
    Email = models.EmailField()


class ExpenseCategory(models.Model):

    description = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.description



class Expense(models.Model):
    description = models.CharField(max_length=1000)
    amount = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    date = models.DateField(default=date.today())
    category = models.ForeignKey(ExpenseCategory)

    def __str__(self):
        return self.description