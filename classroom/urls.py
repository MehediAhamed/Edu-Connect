from django.urls import path
from classroom import views
from classroom import  models
from django.contrib.auth import views as auth_views

app_name = 'classroom'

urlpatterns =[
    path('', views.index, name="index"),
    path('signup/',views.SignUp,name="signup"),
    path('signup/student_signup/',views.StudentSignUp,name="StudentSignUp"),
    path('signup/teacher_signup/',views.TeacherSignUp,name="TeacherSignUp"),
    path('login/',views.user_login,name="login"),
    path('logout/',views.user_logout,name="logout"),
    path('student/<int:pk>/',views.StudentDetailView.as_view(),name="student_detail"),
    path('teacher/<int:pk>/',views.TeacherDetailView.as_view(),name="teacher_detail"),
    path('update/student/<int:pk>/',views.StudentUpdateView,name="student_update"),
    path('update/teacher/<int:pk>/',views.TeacherUpdateView,name="teacher_update"),
    # path('student/<int:pk>/enter_marks',views.add_marks,name="enter_marks"),

    path('student/<int:pk>/<str:subject>/enter_marks',views.add_marks,name="enter_marks"),
    path('student/<int:pk>/marks_list',views.student_marks_list,name="student_marks_list"),
    path('marks/<int:pk>/update',views.update_marks,name="update_marks"),

path('marks_list/<int:pk>/update/<str:subject>/', views.update_marks_list, name='update_marks_list'),
path('student/<int:pk>/enter_marks/<str:subject>/<int:assignment_id>/', views.add_marks_list, name='enter_marks_list'),




    path('student/<int:pk>/add',views.add_student.as_view(),name="add_student"),
    path('student_added/',views.student_added,name="student_added"),
    path('students_list/',views.students_list,name="students_list"),
    path('teachers_list/',views.teachers_list,name="teachers_list"),
    path('teacher/class_students_list',views.class_students_list,name="class_student_list"),
    path('teacher/attendance_list',views.attendance_list,name="attendance_list"),
    path('student/<int:pk>/all_marks',views.StudentAllMarksList.as_view(),name="all_marks_list"),
    path('student/<int:pk>/message',views.write_message,name="write_message"),
    path('teacher/<int:pk>/messages_list',views.messages_list,name="messages_list"),
    path('teacher/write_notice',views.add_notice,name="write_notice"),
    path('teacher/write_link',views.add_meet,name="write_link"),
    path('student/<int:pk>/class_notice',views.class_notice,name="class_notice"),

    path('upload_assignment/',views.upload_assignment,name="upload_assignment"),
    path('upload_material/',views.upload_material,name="upload_material"),

    
    path('class_assignment/',views.class_assignment,name="class_assignment"),
    path('class_material/',views.class_material,name="class_material"),

    path('assignment_list/',views.assignment_list,name="assignment_list"),
    path('material_list/',views.material_list,name="material_list"),

    path('update_assignment/<int:id>/',views.update_assignment,name="update_assignment"),
    path('update_material/<int:id>/',views.update_material,name="update_material"),

    path('assignment_delete/<int:id>/',views.assignment_delete,name="assignment_delete"),
    path('material_delete/<int:id>/',views.material_delete,name="material_delete"),

    path('submit_assignment/<int:id>/',views.submit_assignment,name="submit_assignment"),
    path('submit_list/',views.submit_list,name="submit_list"),
    
    path('change_password/',views.change_password,name="change_password"),
    # path('password_reset/',views.password_reset,name="password_reset"),
    
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    # path('password_reset/',views.CustomPasswordResetView.as_view(),name='password_reset'),

     
    # path('password_reset/',views.password_reset,name='password_reset'),
    
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),

    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),

    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    
    
    
    
    path('video_meet/', views.video_meet_view, name='video_meet'),
    path('reply_to_message/',views.reply_to_message, name='reply_to_message'),
    path('meeting_schedule_list_teacher/<int:pk>/', views.meeting_schedule_list_teacher, name='meeting_schedule_list_teacher'),

    path('meeting_schedule_list/<int:pk>/', views.meeting_schedule_list, name='meeting_schedule_list'),


    path('create_classroom/', views.create_classroom, name='create_classroom'),

    path('select_classroom/', views.select_classroom, name='select_classroom'),

    path('scan/', views.scan_view, name='scan'),
    path('receive/', views.receive_data, name='receive'),



]
