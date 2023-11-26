from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
import misaka

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

class Classroom(models.Model):
    teacher = models.ForeignKey('Teacher', related_name='classrooms', on_delete=models.CASCADE)
    students = models.ManyToManyField('Student', related_name='classrooms', blank=True)
    created_at = models.DateTimeField(auto_now=True)
    subject_name = models.CharField(max_length=250,default='RDBMS')
    subject_code = models.CharField(max_length=50, default='CSE 4508')  # Provide a default value

    assignments = models.ManyToManyField('ClassAssignment', related_name='classrooms', blank=True)
    materials = models.ManyToManyField('ClassMaterial', related_name='classrooms', blank=True)
    meet_links = models.ManyToManyField('MeetLink', related_name='classrooms', blank=True)
    notices = models.ManyToManyField('ClassNotice', related_name='classrooms', blank=True)

    def __str__(self):
        return self.subject_name


    class Meta:
        ordering = ['-created_at']


class Attendance(models.Model):
    roll_no = models.CharField(max_length=255)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='Student')
    name = models.CharField(max_length=250)
    roll_no = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, unique=True)
    student_profile_pic = models.ImageField(upload_to="classroom/student_profile_pic", blank=True)

    def get_absolute_url(self):
        return reverse('classroom:student_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['roll_no']

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='Teacher')
    name = models.CharField(max_length=250)
    university_name = models.CharField(max_length=250)
    degree = models.CharField(max_length=250)
    department = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=254, unique=True)

    teacher_profile_pic = models.ImageField(upload_to="classroom/teacher_profile_pic", blank=True)
    class_students = models.ManyToManyField(Student, through="StudentsInClass")
    created_classrooms = models.ManyToManyField(Classroom, related_name='teachers_created', blank=True)

    def get_absolute_url(self):
        return reverse('classroom:teacher_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name
    
class StudentMarks(models.Model):
    teacher = models.ForeignKey(Teacher, related_name='given_marks', on_delete=models.CASCADE)
    student = models.ForeignKey(Student, related_name="marks", on_delete=models.CASCADE)
    subject_name = models.CharField(max_length=250)
    marks_obtained = models.IntegerField()
    maximum_marks = models.IntegerField()

    def __str__(self):
        return self.subject_name

class StudentsInClass(models.Model):
    teacher = models.ForeignKey(Teacher, related_name="class_teacher", on_delete=models.CASCADE)
    student = models.ForeignKey(Student, related_name="user_student_name", on_delete=models.CASCADE)
    subject_name = models.CharField(max_length=255)  # Add this line to include subject_name

    def __str__(self):
        return f"{self.student.name} in {self.subject_name} taught by {self.teacher.username}"

    class Meta:
        unique_together = ('teacher', 'student','subject_name')

class MessageToTeacher(models.Model):
    student = models.ForeignKey(Student, related_name='student', on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, related_name='messages', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    message_html = models.TextField(editable=False)
    reply = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.message

    def save(self, *args, **kwargs):
        self.message_html = self.message
        super().save(*args, **kwargs)

    def save_rp(self, *args, **kwargs):
        if self.reply:
            super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['student', 'message']

    def send_reply(self, reply_message):
        self.reply = reply_message
        self.save()

class ClassNotice(models.Model):
    id = models.AutoField(primary_key=True)
    teacher = models.ForeignKey(Teacher, related_name='teacher', on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, related_name='class_notice')
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    message_html = models.TextField(editable=False)

    def __str__(self):
        return self.message

    def save(self, *args, **kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['teacher', 'message', 'id']

class MeetLink(models.Model):
    teacher = models.ForeignKey(Teacher, related_name='teacher_meet', on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, related_name='class_meet')
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    message_html = models.TextField(editable=False)

    def __str__(self):
        return self.message

    def save(self, *args, **kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['teacher', 'message']

class ClassAssignment(models.Model):
    student = models.ManyToManyField(Student, related_name='student_assignment')
    teacher = models.ForeignKey(Teacher, related_name='teacher_assignment', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    assignment_name = models.CharField(max_length=250)
    assignment = models.FileField(upload_to='assignments')
    deadline = models.DateTimeField()
    subject = models.TextField()

    def __str__(self):
        return self.assignment_name

    class Meta:
        ordering = ['-created_at']

class ClassMaterial(models.Model):
    student = models.ManyToManyField(Student, related_name='student_material')
    teacher = models.ForeignKey(Teacher, related_name='teacher_material', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    material_name = models.CharField(max_length=250)
    material = models.FileField(upload_to='materials')
    subject = models.TextField()

    def __str__(self):
        return self.material_name

    class Meta:
        ordering = ['-created_at']


class SubmitAssignment(models.Model):
    student = models.ForeignKey(Student, related_name='student_submit', on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, related_name='teacher_submit', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    submitted_assignment = models.ForeignKey(ClassAssignment, related_name='submission_for_assignment', on_delete=models.CASCADE)
    submit = models.FileField(upload_to='Submission')

    def __str__(self):
        return "Submitted" + str(self.submitted_assignment.assignment_name)
    class Meta:
        ordering = ['-created_at']
