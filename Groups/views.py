from django.shortcuts import render
from .models import Group,GroupMembers
from django.http import HttpResponse
from django.contrib import messages
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
        return render(request, 'UserGroup.html', {'name': groupname,'members':Members})

def AddMember(request):
    if request.method == 'POST':
        Name = request.POST['Name']
        Email = request.POST['email']
        GroupId = request.POST['GroupId']

        group = Group.objects.get(GroupName=GroupId)
        groupname = group.GroupName
        print(groupname)
        id = group.id
        print(id)
        Member = GroupMembers(GroupId_id=id,Name=Name,Email=Email)
        Member.save()
        messages.add_message(request, messages.INFO, 'Member Added Successfully')
        Members = GroupMembers.objects.filter(GroupId=id)
        return render(request, 'UserGroup.html', {'name': groupname,'members':Members})