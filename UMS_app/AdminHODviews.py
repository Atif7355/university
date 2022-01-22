from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json

from .forms import AddStudentForm

from .models import CustomUser,Courses,Staffs, Subjects,Students, SessionYearModel, LeaveReportStudent, LeaveReportStaff,Attendance,AttendanceReport


def admin_home(request):
	return render(request, "hodhome.html")


def add_staff(request):
	return render(request, "addstaff.html")
	
def add_staff_save(request):
	if request.method != "POST":
		messages.error(request, "Invalid Method ")
		return redirect('UMS_app:add_staff')
	else:
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		username = request.POST.get('username')
		email_id = request.POST.get('email')
		password = request.POST.get('password')
		address = request.POST.get('address')
		role = request.POST.get('role')
		username = email_id.split('@')[0].split('.')[0]


		try:
			#user = CustomUser.objects.create_user(username=username,password=password,email=email,first_name=first_name,last_name=last_name,role=role,user_type=2)
			user=CustomUser(user_type=2)
			user.first_name=first_name
			user.last_name=last_name
			user.username=username
			user.email=email_id
			user.password=password
			user.role=role
			user.save()
			Staffs.objects.create(admin=user,address=address)
			messages.success(request, "Staff Added Successfully!")
			return redirect('UMS_app:add_staff')
		except:
			messages.error(request, "Failed to Add Staff!")
			return redirect('UMS_app:add_staff')

def get_user_type_from_email(email_id):

	try:
		email_id = email_id.split('@')[0]
		email_user_type = email_id.split('.')[1]
		return CustomUser.EMAIL_TO_USER_TYPE_MAP[email_user_type]
	except:
		return None



def add_course(request):
	return render(request, "addcourse.html")


def add_course_save(request):
	if request.method != "POST":
		messages.error(request, "Invalid Method!")
		return redirect('UMS_app:add_course')
	else:
		course = request.POST.get('course')
		try:
			course_model = Courses(course_name=course)
			course_model.save()
			messages.success(request, "Course Added Successfully!")
			return redirect('UMS_app:add_course')
		except:
			messages.error(request, "Failed to Add Course!")
			return redirect('UMS_app:add_course')


def add_session(request):
	return render(request, "addsession.html")


def add_session_save(request):
	if request.method != "POST":
		messages.error(request, "Invalid Method")
		return redirect('UMS_app:add_session')
	else:
		session_start_year = request.POST.get('session_start_year')
		session_end_year = request.POST.get('session_end_year')

		try:
			sessionyear = SessionYearModel(session_start_year=session_start_year,
										session_end_year=session_end_year)
			sessionyear.save()
			messages.success(request, "Session Year added Successfully!")
			return redirect("UMS_app:add_session")
		except:
			messages.error(request, "Failed to Add Session Year")
			return redirect("UMS_app:add_session")



def add_student(request):
	form = AddStudentForm()
	context = {
		"form": form
	}
	return render(request, 'addstudent.html', context)




def add_student_save(request):
	if request.method != "POST":
		messages.error(request, "Invalid Method")
		return redirect('UMS_app:add_student')
	else:
		form = AddStudentForm(request.POST)

		if form.is_valid():
			first_name = form.cleaned_data['first_name']
			last_name = form.cleaned_data['last_name']
			email_id = form.cleaned_data['email']
			password = form.cleaned_data['password']
			address = form.cleaned_data['address']
			session_year_id = form.cleaned_data['session_year_id']
			course_id = form.cleaned_data['course_id']
			gender = form.cleaned_data['gender']
			role = form.cleaned_data['role']
			username = email_id.split('@')[0].split('.')[0]
			print(username)


			try:
				#user = CustomUser.objects.create_user(username=username,password=password,email=email,first_name=first_name,last_name=last_name,role=role,user_type=3)
				user =CustomUser(user_type=3)
				user.username=username
				user.first_name=first_name
				user.last_name=last_name
				user.email=email_id
				user.password=password
				user.role=role
				user.save()
				Students.objects.create(admin=user,gender=gender,address=address,course_id=Courses.objects.get(id=course_id),session_year_id=SessionYearModel.object.get(id=session_year_id))
				messages.success(request, "Student Added Successfully!")
				return redirect('UMS_app:add_student')
			except:
				messages.error(request, "Failed to Add Student!")
				return redirect('UMS_app:add_student')
		else:
			return redirect('UMS_app:add_student')


def add_subject(request):
	courses=Courses.objects.all()
	staffs=CustomUser.objects.filter(user_type=2)
	context={
		"staffs": staffs,
		"courses": courses
	}
	return render(request,'addsubject.html',context)


def add_subject_save(request):
	if request.method != "POST":
		messages.error(request, "Method Not Allowed!")
		return redirect('UMS_app:add_subject')
	else:
		subject_name = request.POST.get('subject')

		course_id = request.POST.get('course')
		course = Courses.objects.filter(id=course_id).first()
		staff_id = request.POST.get('staff')

		staff = CustomUser.objects.filter(id=staff_id).first()
		try:
			subject = Subjects(subject_name=subject_name,
							course_id=course,
							staff_id=staff)
			subject.save()
			messages.success(request, "Subject Added Successfully!")
			return redirect('UMS_app:add_subject')
		except:
			messages.error(request, "Failed to Add Subject!")
			return redirect('UMS_app:add_subject')


@csrf_exempt
def check_email_exist(request):
	email = request.POST.get("email")
	user_obj = CustomUser.objects.filter(email=email).exists()
	if user_obj:
		return HttpResponse(True)
	else:
		return HttpResponse(False)


@csrf_exempt
def check_username_exist(request):
	username = request.POST.get("username")
	user_obj = CustomUser.objects.filter(username=username).exists()
	if user_obj:
		return HttpResponse(True)
	else:
		return HttpResponse(False)


def student_leave_view(request):
	leaves = LeaveReportStudent.objects.all()
	context = {
		"leaves": leaves
	}
	return render(request, 'studentleave.html', context)

def student_leave_approve(request, leave_id):
	leave = LeaveReportStudent.objects.get(id=leave_id)
	leave.leave_status = 1
	leave.save()
	return redirect('student_leave_view')


def student_leave_reject(request, leave_id):
	leave = LeaveReportStudent.objects.get(id=leave_id)
	leave.leave_status = 2
	leave.save()
	return redirect('student_leave_view')


def staff_leave_view(request):
	leaves = LeaveReportStaff.objects.all()
	context = {
		"leaves": leaves
	}
	return render(request, 'staffleave.html', context)


def staff_leave_approve(request, leave_id):
	leave = LeaveReportStaff.objects.get(id=leave_id)
	leave.leave_status = 1
	leave.save()
	return redirect('staff_leave_view')


def staff_leave_reject(request, leave_id):
	leave = LeaveReportStaff.objects.get(id=leave_id)
	leave.leave_status = 2
	leave.save()
	return redirect('staff_leave_view')

def staff_profile(request):
	pass


def student_profile(request):
	pass
