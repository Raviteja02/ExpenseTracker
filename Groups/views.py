from django.shortcuts import render
from .models import Group,GroupMembers,ExpenseCategory,Expense,ShareBill
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
import decimal
# Create your views here.


def index(request):
    return render(request,'home.html')


def CreateGroup(request):
    if request.method =="POST":
        GroupName = request.POST['GroupName']
        group = Group(GroupName=GroupName)
        group.save()

        count = int(request.POST['czContainer_czMore_txtCount'])
        i = 1
        while i <= count:
            MemberName = request.POST['Member_' + str(i) + '_Name']
            MemberEmail = request.POST['Member_' + str(i) + '_Email']

            Members =GroupMembers(GroupId=group,Name=MemberName,Email=MemberEmail)
            Members.save()

            i+=1
        messages.add_message(request, messages.INFO, 'Group Created Successfully, You Can Now Navigate to Groups and Continue With Your Group.')
        return render(request,'home.html')


def Groups(request):
    if request.method == 'POST':
        pass

    Groups = Group.objects.all()
    return render(request,'Groups.html',{'Groups':Groups})


def UserGroup(request):
    if request.method == 'POST':
        GroupName= request.POST['GroupName']
        group = Group.objects.get(GroupName=GroupName)
        groupname = group.GroupName
        id = group.id
        Members = GroupMembers.objects.filter(GroupId=id)
        categories = ExpenseCategory.objects.all()
        Expen = Expense.objects.filter(GroupId_id=id)

        for x in Expen:
            bill_id = x.id
            bills = ShareBill.objects.filter(bill_id=bill_id)
            persons = bills.values_list('PersonId', flat=True).distinct()
            for y in persons:
                share = ShareBill.objects.get(bill_id=bill_id, PersonId=y)
                TotalShare = share.share
                print(TotalShare)
            print("------")

        AllBills = ShareBill.objects.filter(GroupId_id=id)
        Pids = AllBills.values_list('PersonId', flat=True).distinct()
        owes = {}
        for Pid in Pids:
            bills = ShareBill.objects.filter(PersonId=Pid)
            sum = 0.0
            for bill in bills:
                t = bill.share
                sum = sum + t
                owe = GroupMembers.objects.get(GroupId_id=id, id=Pid)
            owes[owe.Name] = sum
        print(owes)

        return render(request, 'UserGroup.html',{'name': groupname,'members': Members,
                                                  'categories': categories, 'Expen':Expen,'owes':owes})
    return render(request, 'home.html')


def AddMember(request):
    if request.method == 'POST':
        Name = request.POST['Name']
        Email = request.POST['email']
        GroupId = request.POST['GroupId']

        group = Group.objects.get(GroupName=GroupId)
        groupname = group.GroupName
        id = group.id
        Member = GroupMembers(GroupId_id=id,Name=Name,Email=Email)
        Member.save()
        messages.add_message(request, messages.INFO, 'Member Added Successfully')
        Members = GroupMembers.objects.filter(GroupId=id)
        categories = ExpenseCategory.objects.all()
        Expen = Expense.objects.filter(GroupId_id=id)

        for x in Expen:
            bill_id = x.id
            bills = ShareBill.objects.filter(bill_id=bill_id)
            persons = bills.values_list('PersonId', flat=True).distinct()
            for y in persons:
                share = ShareBill.objects.get(bill_id=bill_id, PersonId=y)
                TotalShare = share.share
                print(TotalShare)
            print("------")

        AllBills = ShareBill.objects.filter(GroupId_id=id)
        Pids = AllBills.values_list('PersonId', flat=True).distinct()
        owes = {}
        for Pid in Pids:
            bills = ShareBill.objects.filter(PersonId=Pid)
            sum = 0.0
            for bill in bills:
                t = bill.share
                sum = sum + t
                owe = GroupMembers.objects.get(GroupId_id=id, id=Pid)
            owes[owe.Name] = sum
        print(owes)

        return render(request, 'UserGroup.html', owes,{'name': groupname, 'members': Members,
                                                  'categories': categories, 'Expen': Expen})
    return render(request, 'home.html')


def AddBill(request):
    if request.method == 'POST':

        Category = request.POST['Category']
        Amount = int(request.POST['amount'])
        PaidBy =request.POST['PaidBy']
        Date = request.POST['date']
        GroupId = request.POST['GroupId']

        category = ExpenseCategory.objects.get(name=Category)
        categoryid = category.id

        group = Group.objects.get(GroupName=GroupId)
        groupid = group.id
        groupname = group.GroupName

        paid = GroupMembers.objects.get(Name=PaidBy, GroupId=groupid)
        paidby = paid.id

        shares = GroupMembers.objects.filter(GroupId=groupid).count()
        share = round(Amount / shares,2)
        lent = Amount - share

        Expenses = Expense(GroupId_id=groupid,description=Category,amount=Amount,paidby_id=paidby,category_id=categoryid,
                           date=Date,lent=lent)

        Expenses.save()


        friends = GroupMembers.objects.filter(GroupId=groupid)

        for x in friends:
            if x.id == paid.id:
                pass
            else:
                id = x.id
                split = ShareBill(bill_id=Expenses,GroupId_id=groupid,PersonId_id=id,share=share)
                split.save()

        messages.add_message(request, messages.INFO, 'Bill Added Successfully')
        Members = GroupMembers.objects.filter(GroupId=groupid)
        categories = ExpenseCategory.objects.all()
        Expen = Expense.objects.filter(GroupId_id=groupid)

        for x in Expen:
            bill_id = x.id
            bills = ShareBill.objects.filter(bill_id=bill_id)
            persons = bills.values_list('PersonId', flat=True).distinct()
            for y in persons:
                share = ShareBill.objects.get(bill_id=bill_id, PersonId=y)
                TotalShare = share.share
                print(TotalShare)
            print("------")

        AllBills = ShareBill.objects.filter(GroupId_id=groupid)
        Pids = AllBills.values_list('PersonId', flat=True).distinct()
        owes = {}
        for Pid in Pids:
            bills = ShareBill.objects.filter(PersonId=Pid)
            sum = 0.0
            for bill in bills:
                t = bill.share
                sum = sum + t
                owe = GroupMembers.objects.get(GroupId_id=groupid, id=Pid)
            owes[owe.Name] = sum
        print(owes)

        return render(request,'UserGroup.html', owes,{'name': groupname,'members':Members,
                                                 'categories': categories,'Expen':Expen})
    return render(request, 'home.html')



def Sharing(request):
    groupid = 1
    Expen = Expense.objects.filter(GroupId_id=groupid)
    for x in Expen:
        bill_id = x.id
        bills = ShareBill.objects.filter(bill_id=bill_id)
        persons = bills.values_list('PersonId', flat=True).distinct()
        for y in persons:
            share = ShareBill.objects.get(bill_id=bill_id,PersonId=y)
            TotalShare = share.share
            print(TotalShare)
        print("------")


    AllBills = ShareBill.objects.filter(GroupId_id=groupid)
    Pids = AllBills.values_list('PersonId', flat=True).distinct()
    owes = {}
    for Pid in Pids:
        bills = ShareBill.objects.filter(PersonId=Pid)
        sum = 0.0
        for bill in bills:
            t = bill.share
            sum = sum+t
            owe = GroupMembers.objects.get(GroupId_id=groupid,id=Pid)
        owes[owe.Name] =sum
    print(owes)
    print("****")


    return None