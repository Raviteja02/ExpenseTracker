from django.db import models
from datetime import date
from django.utils import timezone
# Create your models here.


class Group(models.Model):

    GroupName = models.CharField(max_length=20)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.GroupName


class ExpenseCategory(models.Model):

    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class GroupMembers(models.Model):

    GroupId = models.ForeignKey(Group, on_delete=models.CASCADE)
    Name = models.CharField(max_length=30)
    Email = models.EmailField()

    def __str__(self):
        return self.Name


class Expense(models.Model):

    description = models.CharField(max_length=1000)
    amount = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    lent = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    date = models.DateField(timezone.now())
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)
    paidby = models.ForeignKey(GroupMembers,on_delete=models.CASCADE)
    GroupId = models.ForeignKey(Group,on_delete=models.CASCADE)

    def __str__(self):
        return self.description


class ShareBill(models.Model):
    bill_id = models.ForeignKey(Expense,on_delete=models.CASCADE)
    GroupId = models.ForeignKey(Group, on_delete=models.CASCADE)
    PersonId = models.ForeignKey(GroupMembers,on_delete=models.CASCADE)
    share = models.DecimalField(max_digits=18, decimal_places=2, default=0)

