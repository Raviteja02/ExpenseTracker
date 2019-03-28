from django.shortcuts import render, redirect
from .models import Group, GroupMembers, ExpenseCategory, Expense, ShareBill, Register
from django.contrib import messages
from django.http import HttpResponse
import json


def Registration(request):
    if request.method == "POST":
        Email = request.POST['email']
        pwd = request.POST['Password1']
        pwd2 = request.POST['Password2']
        try:
            email = Register.objects.get(Email=Email)
            if email:
                messages.add_message(request, messages.INFO, 'Email Already Exists You Can Try A Different One')
                return redirect('Registration')
        except:
            if pwd == pwd2:
                reg = Register(Email=Email, Password= pwd)
                reg.save()
                request.session['Email'] = Email
                return redirect('index')
            else:
                messages.add_message(request, messages.INFO, 'Please Ensure That You have Entered All The Fields Correctly')
                return redirect('Registration')

    return render(request, 'register.html')


def login(request):
    if request.method == "POST":
        Email = request.POST['email']
        Password = request.POST['password']
        try:
            x = Register.objects.get(Email=Email)
            pwd = x.Password
            if pwd == Password:
                request.session['Email'] = Email
                return redirect('UserGroup')
        except:
            messages.add_message(request, messages.INFO, 'Wrong UserName/Password')
            return render(request, 'login.html')
    return render(request, 'login.html')


def logout(request):
    if request.session.has_key('Email'):
        request.session.flush()
        return redirect('Register')
    return render(request, 'register.html')


def index(request):
    if request.session.has_key('Email'):
        Email = request.session['Email']
        return render(request, 'home.html', {'Email': Email})
    return render(request, 'register.html')


def CreateGroup(request):
    if request.session.has_key('Email'):
        Email = request.session['Email']
        x = Register.objects.get(Email=Email)
        if request.method == "POST":
            GroupName = request.POST['GroupName']
            try:
                group = Group.objects.get(GroupName=GroupName)
                if group:
                    messages.add_message(request, messages.INFO, 'Group Name Already taken You Can Try Different One.')
                    return redirect('index')
            except:
                GroupName = request.POST['GroupName']
                group = Group(GroupName=GroupName, email_id=x)
                group.save()

                count = int(request.POST['czContainer_czMore_txtCount'])
                i = 1
                while i <= count:
                    MemberName = request.POST['Member_' + str(i) + '_Name']
                    MemberEmail = request.POST['Member_' + str(i) + '_Email']

                    Members = GroupMembers(GroupId=group, Name=MemberName, Email=MemberEmail)
                    Members.save()

                    i += 1

                messages.add_message(request, messages.INFO, 'Group Created Successfully.')
                return redirect('UserGroup')
    return redirect('index')


def UserGroup(request):
    if request.session.has_key('Email'):
        Email = request.session['Email']
        x = Register.objects.get(Email=Email)
        group = Group.objects.get(email_id=x)
        groupname = group.GroupName
        id = group.id
        Members = GroupMembers.objects.filter(GroupId=id)
        categories = ExpenseCategory.objects.all()
        Expen = Expense.objects.filter(GroupId_id=id)

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
            lents = Expense.objects.filter(GroupId_id=id, paidby_id=Pid)
            r = 0.0
            for lent in lents:
                l = lent.lent
                r = r + l
            sum = round(r - sum,2)


            owes[owe.Name] = sum


        return render(request, 'UserGroup.html',{'name': groupname,'members': Members,
                                                  'categories': categories, 'Expen':Expen,'owes':owes})

    return render(request, 'home.html')


def AddMember(request):
    if request.session.has_key('Email'):
        Email = request.session['Email']
        x = Register.objects.get(Email=Email)
        if request.method == 'POST':
            Name = request.POST['Name']
            Email = request.POST['email']
            group = Group.objects.get(email_id=x)
            id = group.id
            Member = GroupMembers(GroupId_id=id,Name=Name,Email=Email)
            Member.save()
            messages.add_message(request, messages.INFO, 'Member Added Successfully')
            return redirect('UserGroup')
    return render(request, 'home.html')


def AddBill(request):
    if request.session.has_key('Email'):
        Email = request.session['Email']
        x = Register.objects.get(Email=Email)
        if request.method == 'POST':
            Category = request.POST['Category']
            Amount = int(request.POST['amount'])
            PaidBy =request.POST['PaidBy']
            Date = request.POST['date']

            category = ExpenseCategory.objects.get(name=Category)
            categoryid = category.id

            group = Group.objects.get(email_id=x)
            groupid = group.id

            paid = GroupMembers.objects.get(Name=PaidBy, GroupId=groupid)
            paidby = paid.id

            shares = GroupMembers.objects.filter(GroupId=groupid).count()
            share = round(Amount / shares, 2)
            lent = round(Amount - share, 2)

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
            return redirect('UserGroup')
    return render(request, 'home.html')


def filter(request):
    if request.session.has_key('Email'):
        Email = request.session['Email']
        x = Register.objects.get(Email=Email)
        group = Group.objects.get(email_id=x)
        groupid = group.id
        if request.method == "POST":
            Name = request.POST['Name']
            Month = request.POST['Month']
            Member = GroupMembers.objects.get(GroupId_id=groupid,Name=Name)
            memid = Member.id
            e = Expense.objects.filter(paidby_id=memid,date__month=Month)
            catlist = []
            catspent = []
            for i in e:
                id = i.category_id
                if id not in catlist:
                    catlist.append(id)

            for a in catlist:
                spe = Expense.objects.filter(paidby_id=memid, date__month=Month,category_id= a)
                sum = 0
                for k in spe:
                    t = k.lent
                    sum = sum+(t/2)
                catspent.append(sum)

            total = 0
            for b in catspent:
                total = total+b

            categoryname = []
            for c in catlist:
                x = ExpenseCategory.objects.get(id=c)
                catname = x.name
                categoryname.append(catname)

    return render(request,'Groups.html',{'Expen':e,'total':total,'Name':Name,'categories':json.dumps(categoryname),'spent':json.dumps(catspent)})
