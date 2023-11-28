from django.shortcuts import render,get_object_or_404,redirect
from django.views import generic
from django.views.generic import  (View,TemplateView,
                                  ListView,DetailView,
                                  CreateView,UpdateView,
                                  DeleteView)
from django import forms
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from django.views import generic
from .models import Student, StudentsInClass
from django.shortcuts import render
from django.db.models import Q
from .models import StudentsInClass, Student
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from classroom.forms import UserForm,TeacherProfileForm,StudentProfileForm,MarksForm,MessageForm,NoticeForm,AssignmentForm,MaterialForm,SubmitForm,TeacherProfileUpdateForm,StudentProfileUpdateForm,MeetForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout,update_session_auth_hash
from django.http import HttpResponseRedirect,HttpResponse
from classroom import models
from classroom.models import StudentsInClass,StudentMarks,ClassAssignment,SubmitAssignment,Student,Teacher,Attendance,ClassMaterial
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Q
from django.core.mail import send_mail
from django.shortcuts import render, HttpResponse  


from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from urllib.parse import urlencode
from .models import Classroom, Teacher, MessageToTeacher,MeetLink
from .forms import ClassroomCreationForm, MessageForm



from django.core.cache import cache
from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib import messages

from django.core.cache import cache
from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Classroom
from django.shortcuts import render, redirect
from .models import MessageToTeacher

from django.contrib.auth.decorators import login_required
from functools import wraps
from django.http import HttpResponseForbidden

from django.contrib import messages


# For Teacher Sign Up
def TeacherSignUp(request):
    user_type = 'teacher'
    registered = False

    if request.method == "POST":
        user_form = UserForm(data = request.POST)
        teacher_profile_form = TeacherProfileForm(data = request.POST)

        if user_form.is_valid() and teacher_profile_form.is_valid():

            user = user_form.save()
            user.is_teacher = True
            user.save()

            profile = teacher_profile_form.save(commit=False)
            profile.user = user
            profile.save()

            registered = True
        else:
            print(user_form.errors,teacher_profile_form.errors)
    else:
        user_form = UserForm()
        teacher_profile_form = TeacherProfileForm()

    return render(request,'classroom/teacher_signup.html',{'user_form':user_form,'teacher_profile_form':teacher_profile_form,'registered':registered,'user_type':user_type})


###  For Student Sign Up
def StudentSignUp(request):
    user_type = 'student'
    registered = False

    if request.method == "POST":
        user_form = UserForm(data = request.POST)
        student_profile_form = StudentProfileForm(data = request.POST)

        if user_form.is_valid() and student_profile_form.is_valid():

            user = user_form.save()
            user.is_student = True
            user.save()

            profile = student_profile_form.save(commit=False)
            profile.user = user
            profile.save()

            registered = True
        else:
            print(user_form.errors,student_profile_form.errors)
    else:
        user_form = UserForm()
        student_profile_form = StudentProfileForm()

    return render(request,'classroom/student_signup.html',{'user_form':user_form,'student_profile_form':student_profile_form,'registered':registered,'user_type':user_type})

## Sign Up page which will ask whether you are teacher or student.
def SignUp(request):
    return render(request,'classroom/signup.html',{})

## login view.
def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('home'))

            else:
                return HttpResponse("Account not active")

        else:
            messages.error(request, "Invalid Details")
            return redirect('classroom:login')
    else:
        return render(request,'classroom/login.html',{})

## logout view.
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

## User Profile of student.
class StudentDetailView(LoginRequiredMixin,DetailView):
    context_object_name = "student"
    model = models.Student
    template_name = 'classroom/student_detail_page.html'

## User Profile for teacher.
class TeacherDetailView(LoginRequiredMixin,DetailView):
    context_object_name = "teacher"
    model = models.Teacher
    template_name = 'classroom/teacher_detail_page.html'

## Profile update for students.
@login_required
def StudentUpdateView(request,pk):
    profile_updated = False
    student = get_object_or_404(models.Student,pk=pk)
    if request.method == "POST":
        form = StudentProfileUpdateForm(request.POST,instance=student)
        if form.is_valid():
            profile = form.save(commit=False)
            if 'student_profile_pic' in request.FILES:
                profile.student_profile_pic = request.FILES['student_profile_pic']
            profile.save()
            profile_updated = True
    else:
        form = StudentProfileUpdateForm(request.POST or None,instance=student)
    return render(request,'classroom/student_update_page.html',{'profile_updated':profile_updated,'form':form})

## Profile update for teachers.
@login_required
def TeacherUpdateView(request,pk):
    profile_updated = False
    teacher = get_object_or_404(models.Teacher,pk=pk)
    if request.method == "POST":
        form = TeacherProfileUpdateForm(request.POST,instance=teacher)
        if form.is_valid():
            profile = form.save(commit=False)
            if 'teacher_profile_pic' in request.FILES:
                profile.teacher_profile_pic = request.FILES['teacher_profile_pic']
            profile.save()
            profile_updated = True
    else:
        form = TeacherProfileUpdateForm(request.POST or None,instance=teacher)
    return render(request,'classroom/teacher_update_page.html',{'profile_updated':profile_updated,'form':form})

## List of all students that teacher has added in their class.


def class_students_list(request):
    query = request.GET.get("q", "")
    selected_subject = request.GET.get("subject", "")
    teacher = request.user.Teacher

    # Get subjects associated with the logged-in teacher
    teacher_subjects = StudentsInClass.objects.filter(teacher=teacher).values_list('subject_name', flat=True).distinct()

    # Get students added by the teacher for the selected subject
    students_in_class = StudentsInClass.objects.filter(teacher=teacher)

    # If a subject is selected, filter students based on the selected subject
    if selected_subject:
        students_in_class = students_in_class.filter(subject_name=selected_subject)

    # Get the list of student IDs based on the filter criteria
    student_ids = students_in_class.values_list('student', flat=True)

    # Filter students based on the search query and those added by the teacher
    students = Student.objects.filter(
        Q(name__icontains=query) if query else Q(),
        pk__in=student_ids
    )

    context = {
        "class_students_list": students,
        "teacher_subjects": teacher_subjects,
        "selected_subject": selected_subject,
    }
    template = "classroom/class_students_list.html"
    return render(request, template, context)


def attendance_list(request):
    query = request.GET.get("q", None)
    students = StudentsInClass.objects.filter(teacher=request.user.Teacher)
    students_list = [x.student for x in students]
    qs = Attendance.objects.all()

    if query is not None:
        qs = qs.filter(Q(name__icontains=query))

    # Get today's date
    today = timezone.now().date()

    # Use sets to store unique attendance records
    today_data_set = set()
    past_data_set = set()

    # Filter attendance for students in the class
    for student in students_list:
        attendance_for_student = qs.filter(roll_no=student.roll_no)

        for attendance in attendance_for_student:
            att_date = attendance.timestamp.date()

            if att_date == today:
                today_data_set.add((attendance, student))
            else:
                past_data_set.add((attendance, student))

    # Convert sets back to lists for further processing
    today_data = [{'attendance': att, 'info': info} for att, info in today_data_set]
    past_data = [{'attendance': att, 'info': info} for att, info in past_data_set]

    # Sort the data based on timestamp in descending order
    today_data = sorted(today_data, key=lambda x: x['attendance'].timestamp, reverse=True)
    past_data = sorted(past_data, key=lambda x: x['attendance'].timestamp, reverse=True)

    context = {
        "today_data": today_data,
        "past_data": past_data,
    }
    template = "classroom/attendance_list.html"
    return render(request, template, context)


class ClassStudentsListView(LoginRequiredMixin,DetailView):
    model = models.Teacher
    template_name = "classroom/class_students_list.html"
    context_object_name = "teacher"

class AttendanceView(LoginRequiredMixin,DetailView):
    model = models.Teacher
    template_name = "classroom/attendance_list.html"
    context_object_name = "teacher"



## For Marks obtained by the student in all subjects.
class StudentAllMarksList(LoginRequiredMixin,DetailView):
    model = models.Student
    template_name = "classroom/student_allmarks_list.html"
    context_object_name = "student"

## To give marks to a student.
@login_required
def add_marks(request,pk,subject):
    marks_given = False
    student = get_object_or_404(models.Student,pk=pk)
    if request.method == "POST":
        form = MarksForm(request.POST)
        if form.is_valid():
            marks = form.save(commit=False)
            marks.student = student
            marks.teacher = request.user.Teacher
            marks.subject_name=subject
            marks.save()
            messages.success(request,'Marks uploaded successfully!')
            return redirect('classroom:submit_list')
    else:
        form = MarksForm()
    return render(request,'classroom/add_marks.html',{'form':form,'student':student,'marks_given':marks_given, 'subject': subject})

## For updating marks.
@login_required
def update_marks(request,pk):
    marks_updated = False
    obj = get_object_or_404(StudentMarks,pk=pk)
    if request.method == "POST":
        form = MarksForm(request.POST,instance=obj)
        if form.is_valid():
            marks = form.save(commit=False)
            marks.save()
            marks_updated = True
    else:
        form = MarksForm(request.POST or None,instance=obj)
    return render(request,'classroom/update_marks.html',{'form':form,'marks_updated':marks_updated})

## For writing notice which will be sent to all class students.
@login_required
def add_notice(request):
    notice_sent = False
    teacher = request.user.Teacher
    students = StudentsInClass.objects.filter(teacher=teacher)
    students_list = [x.student for x in students]

    if request.method == "POST":
        notice = NoticeForm(request.POST)
        if notice.is_valid():
            object = notice.save(commit=False)
            object.teacher = teacher
            object.save()
            object.students.add(*students_list)
            notice_sent = True
    else:
        notice = NoticeForm()
    return render(request,'classroom/write_notice.html',{'notice':notice,'notice_sent':notice_sent})


## For sending meet link which will be sent to all class students.
@login_required
def add_meet(request):
    Link_sent = False
    teacher = request.user.Teacher
    students = StudentsInClass.objects.filter(teacher=teacher)
    students_list = [x.student for x in students]

    if request.method == "POST":
        meet = MeetForm(request.POST)
        if meet.is_valid():
            object = meet.save(commit=False)
            object.teacher = teacher
            object.save()
            object.students.add(*students_list)
            Link_sent = True
    else:
        meet = MeetForm()
    return render(request,'classroom/write_link.html',{'meeting':meet,'meeting_sent':Link_sent})

## For student writing message to teacher.
@login_required


def write_message(request, pk):
    message_sent = False
    teacher = get_object_or_404(Teacher, pk=pk)

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            mssg = form.save(commit=False)
            mssg.teacher = teacher
            mssg.student = request.user.Student
            mssg.save()
            message_sent = True

            # Capture the current URL
            current_url = request.get_full_path()
            # Create a dictionary with query parameters
            query_parameters = request.GET.dict()
            if query_parameters:
                current_url += "?" + urlencode(query_parameters)

            # Redirect to the captured URL
            return HttpResponseRedirect(current_url)
    else:
        form = MessageForm()
    
    messages_history = teacher.messages.order_by('-created_at')[::-1]
    print(messages_history)
    return render(request, 'classroom/write_message.html', {
        'form': form,
        'teacher': teacher,
        'message_sent': message_sent,
        'messages': messages_history,
    })



## For the list of all the messages teacher have received.
@login_required
def messages_list(request,pk):
    teacher = get_object_or_404(models.Teacher,pk=pk)
    return render(request,'classroom/messages_list.html',{'teacher':teacher})






## Student can see all notice given by their teacher.
@login_required
def class_notice(request,pk):
    student = get_object_or_404(models.Student,pk=pk)
    return render(request,'classroom/class_notice_list.html',{'student':student})

## To see the list of all the marks given by the techer to a specific student.
@login_required
def student_marks_list(request,pk):
    error = True
    student = get_object_or_404(models.Student,pk=pk)
    teacher = request.user.Teacher
    given_marks = StudentMarks.objects.filter(teacher=teacher,student=student)
    return render(request,'classroom/student_marks_list.html',{'student':student,'given_marks':given_marks})

## To add student in the class.from django.contrib import messages


class AddStudentForm(forms.Form):
    subject_name = forms.CharField(max_length=255)

class add_student(LoginRequiredMixin, generic.RedirectView):
    form_class = AddStudentForm

    def get_redirect_url(self, *args, **kwargs):
        return reverse('classroom:students_list')

    def post(self, request, *args, **kwargs):
        student = get_object_or_404(Student, pk=self.kwargs.get('pk'))
        form = self.form_class(request.POST)

        if form.is_valid():
            subject_name = form.cleaned_data['subject_name']

            try:
                StudentsInClass.objects.create(
                    teacher=self.request.user.Teacher,
                    student=student,
                    subject_name=subject_name
                )
                messages.success(request, '{} successfully added to {}!'.format(student.name, subject_name))
            except:
                messages.warning(request, 'Warning, Student already in class for {}!'.format(subject_name))
        else:
            messages.warning(request, 'Invalid form data. Please provide a subject name.')

        return super().get(request, *args, **kwargs)



@login_required
def student_added(request):
    return render(request,'classroom/student_added.html',{})

# List of students which are not added by teacher in their class.

def students_list(request):
    query = request.GET.get('q')
    if query:
        students = Student.objects.filter(name__icontains=query)
    else:
        students = Student.objects.all()

    classrooms = Classroom.objects.all()  # Fetch all classrooms
    subjects = classrooms.values_list('subject_name', flat=True).distinct()

    context = {
        'students_list': students,
        'query': query,
        'subjects': subjects,
    }
    return render(request, 'classroom/students_list.html', context)

## List of all the teacher present in the portal.
def teachers_list(request):
    query = request.GET.get("q", None)
    qs = Teacher.objects.all()
    if query is not None:
        qs = qs.filter(
                Q(name__icontains=query)
                )

    context = {
        "teachers_list": qs,
    }
    template = "classroom/teachers_list.html"
    return render(request, template, context)




@transaction.atomic
@login_required
def upload_assignment(request):
    assignment_uploaded = False
    teacher = request.user.Teacher
    students = Student.objects.filter(user_student_name__teacher=request.user.Teacher)

    created_classrooms = teacher.created_classrooms.all()

    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.teacher = teacher
            upload.deadline = request.POST['deadline']  # Assuming 'deadline' is the name attribute in your form

            # Retrieve the subject_id from the form data
            subject_id = request.POST.get('classroom_select')

            # Retrieve the subject name from the Classroom table
            try:
                selected_classroom = Classroom.objects.get(id=subject_id)
                subject_name = selected_classroom.subject_name
            except Classroom.DoesNotExist:
                subject_name = ''

            # Assign the subject to the form's subject field
            upload.subject = subject_name
            print(subject_name)
            # Save the assignment
            upload.save()

            # Add students to the assignment
            upload.student.add(*students)

            assignment_uploaded = True
    else:
        form = AssignmentForm()

    return render(request, 'classroom/upload_assignment.html', {'form': form, 'assignment_uploaded': assignment_uploaded, 'created_classrooms': created_classrooms})

#material upload
@transaction.atomic
@login_required
def upload_material(request):
    material_uploaded = False
    teacher = request.user.Teacher
    students = Student.objects.filter(user_student_name__teacher=request.user.Teacher)

    created_classrooms = teacher.created_classrooms.all()

    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.teacher = teacher

            # Retrieve the subject_id from the form data
            subject_id = request.POST.get('classroom_select')

            # Retrieve the subject name from the Classroom table
            try:
                selected_classroom = Classroom.objects.get(id=subject_id)
                subject_name = selected_classroom.subject_name
            except Classroom.DoesNotExist:
                subject_name = ''

            # Assign the subject to the form's subject field
            upload.subject = subject_name
            print(subject_name)
            # Save the assignment
            upload.save()

            # Add students to the assignment
            upload.student.add(*students)

            material_uploaded = True
    else:
        form = MaterialForm()

    return render(request, 'classroom/upload_material.html', {'form': form, 'material_uploaded':material_uploaded, 'created_classrooms': created_classrooms})











## Students getting the list of all the assignments uploaded by their teacher.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import SubmitAssignment

@login_required
def class_assignment(request):
    student = request.user.Student
    assignments = student.student_assignment.all().order_by('subject', 'deadline')
    
    submitted_assignments = [x.submitted_assignment for x in SubmitAssignment.objects.filter(student=student)]

    return render(request, 'classroom/class_assignment.html', {
    'student': student,
    'assignments': assignments,
    'submitted_assignments': submitted_assignments,
})





## Students getting the list of all the materials uploaded by their teacher.
@login_required
def class_material(request):
    student = request.user.Student
    material = SubmitAssignment.objects.filter(student=student)
    material_list = [x.submitted_assignment for x in material]
    return render(request,'classroom/class_material.html',{'student':student,'material_list':material_list})
## List of all the assignments uploaded by the teacher himself.
@login_required
def assignment_list(request):
    teacher = request.user.Teacher
    return render(request,'classroom/assignment_list.html',{'teacher':teacher})


## List of all the materials uploaded by the teacher himself.
@login_required
def material_list(request):
    teacher = request.user.Teacher
    return render(request,'classroom/material_list.html',{'teacher':teacher})


## For updating the assignments later.
@login_required
def update_assignment(request,id=None):
    obj = get_object_or_404(ClassAssignment, id=id)
    form = AssignmentForm(request.POST or None, instance=obj)
    context = {
        "form": form
    }
    if form.is_valid():
        obj = form.save(commit=False)
        if 'assignment' in request.FILES:
            obj.assignment = request.FILES['assignment']
        new_deadline = request.POST['new_deadline']
        if new_deadline:
            obj.deadline = new_deadline

        obj.save()
        return redirect('classroom:assignment_list')
    template = "classroom/update_assignment.html"
    return render(request, template, context)



## For updating the material later.@login_required

def update_material(request,id=None):
    obj = get_object_or_404(ClassMaterial, id=id)
    form = MaterialForm(request.POST or None, instance=obj)
    context = {
        "form": form
    }
    if form.is_valid():
        obj = form.save(commit=False)
        if 'material' in request.FILES:
            obj.material = request.FILES['material']
       

        obj.save()
        return redirect('classroom:material_list')
    template = "classroom/update_material.html"
    return render(request, template, context)





## For deleting the assignment.
@login_required
def assignment_delete(request, id=None):
    obj = get_object_or_404(ClassAssignment, id=id)
    if request.method == "POST":
        obj.delete()
        return redirect('classroom:assignment_list')
    context = {
        "object": obj,
    }
    template = "classroom/assignment_delete.html"
    return render(request, template, context)



## For deleting the material.
@login_required
def material_delete(request, id=None):
    obj = get_object_or_404(ClassMaterial, id=id)
    if request.method == "POST":
        obj.delete()
        return redirect('classroom:material_list')
    context = {
        "object": obj,
    }
    template = "classroom/material_delete.html"
    return render(request, template, context)




## For students submitting their assignment.
@login_required
def submit_assignment(request, id=None):
    student = request.user.Student
    assignment = get_object_or_404(ClassAssignment, id=id)
    teacher = assignment.teacher
    if request.method == 'POST':
        form = SubmitForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.teacher = teacher
            upload.student = student
            upload.submitted_assignment = assignment
            upload.save()
            return redirect('classroom:class_assignment')
    else:
        form = SubmitForm()
    return render(request,'classroom/submit_assignment.html',{'form':form,})

## To see all the submissions done by the students.
from django.shortcuts import render
from .models import SubmitAssignment

@login_required
def submit_list(request):
    teacher = request.user.Teacher

    # Get the subjects related to the submitted assignments
    submitted_assignments = SubmitAssignment.objects.filter(teacher=teacher)
    subjects = submitted_assignments.values_list('submitted_assignment__subject', flat=True).distinct()

    return render(request, 'classroom/submit_list.html', {'teacher': teacher, 'subjects': subjects})


##################################################################################################

## For changing password.
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST , user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Password changed")
            return redirect('home')
        else:
            return redirect('classroom:change_password')
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form':form}
        return render(request,'classroom/change_password.html',args)


def index(request):

	if request.method == 'POST':
		name = request.POST['name']
		email = request.POST['email']
		subject = request.POST['subject']
		message = request.POST['message']

		message = name + " with the email, " + email + ", sent the following message:\n\n" + message;

		send_mail(subject,
		 message,
        'tawsiftashwar@iut-dhaka.edu',
		#  'anirudha.17me010@sode-edu.in', 
		#  ['ab8055shetty@gmail.com'],
           ['tawsifdipto17@gmail.com'],
		 fail_silently=False)
	return render(request, 'classroom/index.html')



def video_meet_view(request):
    return render(request, 'classroom/video_meet.html')



# Your other imports and views...

def reply_to_message(request):
    if request.method == "POST":
        message_id = request.POST.get("message_id")
        reply_text = request.POST.get("reply_text")
        print('hereeeee' + message_id)
        # Retrieve the message instance from the database
        message = MessageToTeacher.objects.get(id=message_id)

        # Set the teacher's reply and save the message
        message.reply = reply_text
        message.save_rp()

        # You may want to add additional logic here, such as sending notifications to the student

        return redirect('classroom:messages_list', pk=message.teacher.pk)

    # Handle GET requests or other cases as needed
    # You can render a template or return a response
    # to show the message reply form.

    return render(request, "classroom/messages_list.html")


def meeting_schedule_list(request):
    # Retrieve meeting schedules from the database
    meeting_schedules = MeetLink.objects.all()

    context = {
        'meeting_schedules': meeting_schedules,
    }

    return render(request, 'classroom/meeting_schedule_list.html', context)



def teacher_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Check if the user is authenticated and associated with a teacher
        print(f"User: {request.user}")
        print(f"Is Authenticated: {request.user.is_authenticated}")
        print(f"Has Teacher Attribute: {hasattr(request.user, 'teacher')}")
        
        if request.user.is_authenticated and hasattr(request.user, 'teacher'):
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("You don't have permission to access this page.")

    return _wrapped_view


@login_required


def create_classroom(request):
    print("Entering create_classroom view")  # Check if the view is being accessed
    if request.method == 'POST':
        form = ClassroomCreationForm(request.POST)
        if form.is_valid():
            # Save the classroom and associate it with the teacher
            print("Form is valid")
            classroom = form.save(commit=False)

            # Query the Teacher model based on the current user
            teacher = Teacher.objects.get(user=request.user)

            classroom.teacher = teacher
            classroom.save()
            teacher.created_classrooms.add(classroom)
            print("Classroom saved successfully")
            messages.success(request, 'Classroom created successfully!')

            # Redirect to the same page with the success message
            return redirect('classroom:create_classroom')
        else:
            print(form.errors)  # Print form errors to the console
    else:
        form = ClassroomCreationForm()

    return render(request, 'classroom/create_classroom.html', {'form': form})


@login_required

# views.py
@login_required
def select_classroom(request):
    # Retrieve the teacher based on the current user
    teacher = Teacher.objects.get(user=request.user)
    
    # Get the classrooms created by the teacher
    created_classrooms = teacher.created_classrooms.all()

    if request.method == 'POST':
        # Get the selected classroom ID from the form
        selected_classroom_id = request.POST.get('classroom_select')

        # Save the selected classroom ID in the cache
        cache.set('selected_classroom_id', selected_classroom_id)

        # Redirect to the selected classroom's detail view or any other desired page
        return render(request, 'classroom/base.html')

    return render(request, 'classroom/select_classroom.html', {'created_classrooms': created_classrooms})


# Scan Arduino
def scan_view(request):
    return render(request, 'classroom/scan.html')



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db import connection


@csrf_exempt
def receive_data(request):
    if request.method == 'POST':
        try:
            data = request.POST.get('data', '')
            timestamp = timezone.now()  # Set the timestamp here
            
            
            
            # Store data in the SQLite database
            with connection.cursor() as cursor:
                if data != 'Error: Buffer overflow detected!':
                    if len(data) == 7:
                        print(data)
            # Use parameterized query to prevent SQL injection
                        cursor.execute("INSERT INTO classroom_attendance (roll_no, timestamp) VALUES (?, ?)", (data, timestamp))
                        
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})