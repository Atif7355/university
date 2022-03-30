from django.contrib import admin
from django.urls import path, include
from .import views,AdminHODviews, Staffviews, Studentviews
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.views.static import serve
from .Staffviews import (
AssignmentCreateView,
AssignmentView,
AssignmentSubmissionListView
)
from .Studentviews import(
	AssignmentView1,
AssignmentSubmissionView,
)



app_name = "UMS_app"

urlpatterns = [
	path("", views.index, name="index"),
	path('contact/', views.contact, name="contact"),
	path('logi', views.logi, name="logi"),
	path('doLogin', views.doLogin, name="doLogin"),
	path('logout_user', views.logout_user, name="logout_user"),
	path('signup/',views.signup,name="signup"),
    path('dosignup',views.dosignup,name="dosignup"),
	path('feedback',views.feedback,name="feedback"),
	url(r'^download/(?P<path>.^)$',serve,{'document_root':settings.MEDIA_ROOT}),
	
	# URLS for Student
	path('student_home1/', Studentviews.student_home1, name="student_home1"),
    path('student_home2/', Studentviews.student_home2, name="student_home2"),
	path('student_view_attendance/', Studentviews.student_view_attendance, name="student_view_attendance"),
    path('student_view_attendance_post/', Studentviews.student_view_attendance_post, name="student_view_attendance_post"),
	path('student_apply_leave/', Studentviews.student_apply_leave, name="student_apply_leave"),
	path('student_apply_leave_save/', Studentviews.student_apply_leave_save, name="student_apply_leave_save"),
	path('student_view_result/', Studentviews.student_view_result, name="student_view_result"),
	path('exams/', Studentviews.exams, name='exams'),
    path('attempt_exam/', Studentviews.attempt_exam, name='attempt_exam'),
    path('approved_exams/', Studentviews.approved_exams, name='approved_exams'),
    path('verify/', Studentviews.verify, name='verify'),
    path('progress/', Studentviews.progress, name='progress'),
    path('answer_key/', Studentviews.answer_key, name='answer_key'),


	# URLS for Staff
	path('staff_home1/', Staffviews.staff_home1, name="staff_home1"),
	path('staff_home2/', Staffviews.staff_home2, name="staff_home2"),
	path('staff_home3/', Staffviews.staff_home3, name="staff_home3"),
	path('staff_home4/', Staffviews.staff_home4, name="staff_home4"),
	path('staff_take_attendance/', Staffviews.staff_take_attendance, name="staff_take_attendance"),
	path('get_students/', Staffviews.get_students, name="get_students"),
    path('save_attendance_data/', Staffviews.save_attendance_data, name="save_attendance_data"),
    path('staff_update_attendance/', Staffviews.staff_update_attendance, name="staff_update_attendance"),
    path('get_attendance_dates/', Staffviews.get_attendance_dates, name="get_attendance_dates"),
    path('get_attendance_student/', Staffviews.get_attendance_student, name="get_attendance_student"),
    path('save_updateattendance_data', Staffviews.save_updateattendance_data, name="save_updateattendance_data"),
	path('staff_apply_leave/', Staffviews.staff_apply_leave, name="staff_apply_leave"),
	path('staff_apply_leave_save/', Staffviews.staff_apply_leave_save, name="staff_apply_leave_save"),
	path('staff_add_result/', Staffviews.staff_add_result, name="staff_add_result"),
	path('staff_add_result_save/', Staffviews.staff_add_result_save, name="staff_add_result_save"),
	path('fetch_result_student',Staffviews.fetch_result_student,name="fetch_result_student"),
	path('add_exam/', Staffviews.add_exam, name='add_exam'),
	path('modify_exam/', Staffviews.modify_exam, name='modify_exam'),
	path('update_exam/', Staffviews.update_exam, name='update_exam'),
	path('view_exam/', Staffviews.view_exam, name='view_exam'),
	path('add_question/', Staffviews.add_question, name='add_question'),
	path('modify_question/', Staffviews.modify_question, name='modify_question'),
	path('update_question/', Staffviews.update_question, name='update_question'),
	path('view_question/', Staffviews.view_question, name='view_question'),
	path('get_exams_by_course/', Staffviews.get_exams_by_course, name='get_exams_by_course'),
	path('evaluate/', Staffviews.evaluate, name='evaluate'),
	path('manual_evaluate/', Staffviews.manual_evaluate, name='manual_evaluate'),
	path('exam_registrations/', Staffviews.exam_registrations, name='exam_registrations'),
	path('register_evaluate/', Staffviews.register_evaluate, name='register_evaluate'),
	#path('verify/', Staffviews.verify, name='verify'),
	
	# URL for Admin
	path('admin_home/', AdminHODviews.admin_home, name="admin_home"),
	path('add_staff/', AdminHODviews.add_staff, name="add_staff"),
	path('add_staff_save/', AdminHODviews.add_staff_save, name="add_staff_save"),
	path('add_course/', AdminHODviews.add_course, name="add_course"),
	path('add_course_save/', AdminHODviews.add_course_save, name="add_course_save"),
	path('add_session/', AdminHODviews.add_session, name="add_session"),
	path('add_session_save/', AdminHODviews.add_session_save, name="add_session_save"),
	path('add_student/', AdminHODviews.add_student, name="add_student"),
	path('add_student_save/', AdminHODviews.add_student_save, name="add_student_save"),
	path('add_subject/', AdminHODviews.add_subject, name="add_subject"),
	path('add_subject_save/', AdminHODviews.add_subject_save, name="add_subject_save"),
	path('check_email_exist/', AdminHODviews.check_email_exist, name="check_email_exist"),
	path('check_username_exist/', AdminHODviews.check_username_exist, name="check_username_exist"),
	path('student_leave_view/', AdminHODviews.student_leave_view, name="student_leave_view"),
	path('student_leave_approve/<leave_id>/', AdminHODviews.student_leave_approve, name="student_leave_approve"),
	path('student_leave_reject/<leave_id>/', AdminHODviews.student_leave_reject, name="student_leave_reject"),
	path('staff_leave_view/', AdminHODviews.staff_leave_view, name="staff_leave_view"),
	path('staff_leave_approve/<leave_id>/', AdminHODviews.staff_leave_approve, name="staff_leave_approve"),
	path('staff_leave_reject/<leave_id>/', AdminHODviews.staff_leave_reject, name="staff_leave_reject"),


	path('assignment-create/', AssignmentCreateView.as_view(), name='assignment-create'),
                  path('assignment/', AssignmentView.as_view(), name='assignment-list'),
				  path('assignment1/', AssignmentView1.as_view(), name='assignment-list1'),
				  path('assignment-submission/', AssignmentSubmissionView.as_view(), name='assignment-submission'),
                  path('assignment-submission-list/', AssignmentSubmissionListView.as_view(), name='assignment-submission-list'),
	
]   + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

