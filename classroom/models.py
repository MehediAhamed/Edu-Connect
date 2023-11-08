from django.db import models
from django.contrib.auth.models import AbstractUser
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
import misaka
# Create your models here.

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)


class Attendance(models.Model):
    roll_no = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

class Student(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True,related_name='Student')
    name=models.CharField(max_length=250)
    roll_no = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    phone = models.IntegerField()
    student_profile_pic = models.ImageField(upload_to="classroom/student_profile_pic",blank=True)

    def get_absolute_url(self):
        return reverse('classroom:student_detail',kwargs={'pk':self.pk})

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['roll_no']

class Teacher(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True,related_name='Teacher')
    name = models.CharField(max_length=250)
    subject_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=254)
    phone = models.IntegerField()
    teacher_profile_pic = models.ImageField(upload_to="classroom/teacher_profile_pic",blank=True)
    class_students = models.ManyToManyField(Student,through="StudentsInClass")

    def get_absolute_url(self):
        return reverse('classroom:teacher_detail',kwargs={'pk':self.pk})

    def __str__(self):
        return self.name

class StudentMarks(models.Model):
    teacher = models.ForeignKey(Teacher,related_name='given_marks',on_delete=models.CASCADE)
    student = models.ForeignKey(Student,related_name="marks",on_delete=models.CASCADE)
    subject_name = models.CharField(max_length=250)
    marks_obtained = models.IntegerField()
    maximum_marks = models.IntegerField()

    def __str__(self):
        return self.subject_name

class StudentsInClass(models.Model):
    teacher = models.ForeignKey(Teacher,related_name="class_teacher",on_delete=models.CASCADE)
    student = models.ForeignKey(Student,related_name="user_student_name",on_delete=models.CASCADE)

    def __str__(self):
        return self.student.name

    class Meta:
        unique_together = ('teacher','student')

# class MessageToTeacher(models.Model):
#     student = models.ForeignKey(Student,related_name='student',on_delete=models.CASCADE)
#     teacher = models.ForeignKey(Teacher,related_name='messages',on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now=True)
#     message = models.TextField()
#     message_html = models.TextField(editable=False)

#     def __str__(self):
#         return self.message

#     def save(self,*args,**kwargs):
#         self.message_html = misaka.html(self.message)
#         super().save(*args,**kwargs)

#     class Meta:
#         ordering = ['-created_at']
#         unique_together = ['student','message']


class MessageToTeacher(models.Model):
    student = models.ForeignKey(Student,related_name='student',on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher,related_name='messages',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    message_html = models.TextField(editable=False)
    reply = models.TextField(blank=True, null=True)  # To store the teacher's reply

    def __str__(self):
        return self.message

    # def save(self, *args, **kwargs):
    #     self.message_html = misaka.html(self.message)
    #     super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.reply:
        # If there's a reply, update the message and set the reply column
            self.message = self.reply
            self.reply = None
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['student','message']

    def send_reply(self, reply_message):
        self.reply = reply_message
        self.save()


def reply_to_message(request):
    if request.method == "POST":
        message_id = request.POST.get("message_id")
        reply_text = request.POST.get("reply")

        message = MessageToTeacher.objects.get(id=message_id)
        message.send_reply(reply_text)

   # Send a notification to the student
        notification = Notification.objects.create(
            message="Your teacher has replied to your message.",
            user=self.student
    )
        notification.send()



    
class ClassNotice(models.Model):
    teacher = models.ForeignKey(Teacher,related_name='teacher',on_delete=models.CASCADE)
    students = models.ManyToManyField(Student,related_name='class_notice')
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    message_html = models.TextField(editable=False)

    def __str__(self):
        return self.message

    def save(self,*args,**kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args,**kwargs)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['teacher','message']


class ClassAssignment(models.Model):
    student = models.ManyToManyField(Student,related_name='student_assignment')
    teacher = models.ForeignKey(Teacher,related_name='teacher_assignment',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    assignment_name = models.CharField(max_length=250)
    assignment = models.FileField(upload_to='assignments')

    def __str__(self):
        return self.assignment_name

    class Meta:
        ordering = ['-created_at']

class SubmitAssignment(models.Model):
    student = models.ForeignKey(Student,related_name='student_submit',on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher,related_name='teacher_submit',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    submitted_assignment = models.ForeignKey(ClassAssignment,related_name='submission_for_assignment',on_delete=models.CASCADE)
    submit = models.FileField(upload_to='Submission')

    def __str__(self):
        return "Submitted"+str(self.submitted_assignment.assignment_name)

    class Meta:
        ordering = ['-created_at']
