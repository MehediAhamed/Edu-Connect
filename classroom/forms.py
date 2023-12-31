from django import forms
from django.contrib.auth.forms import UserCreationForm
from classroom.models import Classroom, User,Teacher,Student,StudentMarks,MessageToTeacher,ClassNotice,ClassAssignment,SubmitAssignment,MeetLink,ClassMaterial
from django.db import transaction
from django.forms import ModelForm, Textarea


## User Login Form (Applied in both student and teacher login)
class UserForm(UserCreationForm):
    class Meta():
        model = User
        fields = ['username','password1','password2']
        widgets = {
                'username': forms.EmailInput(attrs={'class':'answer'}),
                'password1': forms.PasswordInput(attrs={'class':'answer'}),
                'password2': forms.PasswordInput(attrs={'class':'answer'}),
                }

## Teacher Registration Form
class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name', 'university_name', 'degree', 'department', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'answer'}),
            'university_name': forms.TextInput(attrs={'class': 'answer'}),
            'degree': forms.NumberInput(attrs={'class': 'answer'}),
            'department': forms.NumberInput(attrs={'class': 'answer'}),
            'email': forms.EmailInput(attrs={'class': 'answer'}),
        }

## Teacher Profile Update Form
class TeacherProfileUpdateForm(forms.ModelForm):
    class Meta():
        model = Teacher
        fields = ['name','university_name','degree', 'department','teacher_profile_pic']

## Student Registration Form
class StudentProfileForm(forms.ModelForm):
    class Meta():
        model =  Student
        fields = ['name','roll_no','email']
        widgets = {
                'name': forms.TextInput(attrs={'class':'answer'}),
                'roll_no': forms.NumberInput(attrs={'class':'answer'}),
                'email': forms.EmailInput(attrs={'class':'answer'}),
                }

## Student profile update form
class StudentProfileUpdateForm(forms.ModelForm):
    class Meta():
        model = Student
        fields = ['name','roll_no','student_profile_pic']

## Form for uploading marks and also for updating it.
class MarksForm(forms.ModelForm):
    class Meta():
        model = StudentMarks
        fields = ['marks_obtained','maximum_marks']

## Writing message to teacher
class MessageForm(forms.ModelForm):
    class Meta():
        model = MessageToTeacher
        fields = ['message']


## Writing notice in the class
class NoticeForm(forms.ModelForm):
    class Meta():
        model = ClassNotice
        fields = ['message']


## Writing notice in the class
class MeetForm(forms.ModelForm):
    class Meta():
        model = MeetLink
        fields = ['message']


## Form for uploading or updating assignment (teachers only)
class AssignmentForm(forms.ModelForm):
    class Meta():
        model = ClassAssignment
        fields = ['assignment_name','assignment']



## Form for uploading or updating material (teachers only)
class MaterialForm(forms.ModelForm):
    class Meta():
        model = ClassMaterial
        fields = ['material_name','material']


## Form for submitting assignment (Students only)
class SubmitForm(forms.ModelForm):
    class Meta():
        model = SubmitAssignment
        fields = ['submit']




class ClassroomCreationForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ['subject_name', 'subject_code']
        widgets = {
            'subject_name': Textarea(attrs={'cols': 10, 'rows': 1}),
            'subject_code': Textarea(attrs={'cols': 10, 'rows': 1}),
        }