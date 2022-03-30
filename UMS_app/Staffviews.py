from django.shortcuts import render, redirect
from django.http import HttpResponse,Http404, HttpResponseRedirect, JsonResponse,HttpResponseNotFound
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
import datetime
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, CreateView, ListView, DeleteView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse  
from pathlib import Path,os
from django.conf import settings
from django.utils import timezone
from django.db.models import Sum
from .forms import AssignmentCreateForm
from .models import CustomUser,exam_detail,Assignment,AssignmentSubmission,result,registration,question_bank,question_type,level,option,answer,MatchTheColumns, Staffs, Subjects,Courses, Students, SessionYearModel, LeaveReportStaff, StudentResult,Attendance, AttendanceReport




def staff_home1(request):
    return render(request, "staffhome.html")

def staff_home2(request):
    return render(request, "staffhome.html")
    
def staff_home3(request):
    context={'file':AssignmentSubmission.objects.all()}
    return render(request, "staffhome.html")


def staff_home4(request):
    return render(request, "staffhome.html")


def staff_apply_leave(request):
	print(request.user.id)
	staff_obj = Staffs.objects.get(admin=request.user.id)
	leave_data = LeaveReportStaff.objects.filter(staff_id=staff_obj)
	context = {
		"leave_data": leave_data
	}
	return render(request, "staffapplyleave.html", context)


def staff_apply_leave_save(request):
	if request.method != "POST":
		messages.error(request, "Invalid Method")
		return redirect('UMS_app:staff_apply_leave')
	else:
		leave_date = request.POST.get('leave_date')
		leave_message = request.POST.get('leave_message')

		staff_obj = Staffs.objects.get(admin=request.user.id)
		try:
			leave_report = LeaveReportStaff(staff_id=staff_obj,
											leave_date=leave_date,
											leave_message=leave_message,
											leave_status=0)
			leave_report.save()
			messages.success(request, "Applied for Leave.")
			return redirect('UMS_app:staff_apply_leave')
		except:
			messages.error(request, "Failed to Apply Leave")
			return redirect('UMS_app:staff_apply_leave')



@csrf_exempt
def get_students(request):
	
	subject_id = request.POST.get("subject")
	session_year = request.POST.get("session_year")

	# Students enroll to Course, Course has Subjects
	# Getting all data from subject model based on subject_id
	subject_model = Subjects.objects.get(id=subject_id)

	session_model = SessionYearModel.object.get(id=session_year)

	students = Students.objects.filter(course_id=subject_model.course_id,
									session_year_id=session_model)

	# Only Passing Student Id and Student Name Only
	list_data = []

	for student in students:
		data_small={"id":student.admin.id,
					"name":student.admin.first_name+" "+student.admin.last_name}
		list_data.append(data_small)

	return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


def staff_take_attendance(request):
    subjects=Subjects.objects.filter(staff_id=request.user.id)
    session_years=SessionYearModel.object.all()
    return render(request,"staff_take_attendance.html",{"subjects":subjects,"session_years":session_years})

@csrf_exempt
def save_attendance_data(request):
    student_ids=request.POST.get("student_ids")
    subject_id=request.POST.get("subject_id")
    attendance_date=request.POST.get("attendance_date")
    session_year_id=request.POST.get("session_year_id")

    subject_model=Subjects.objects.get(id=subject_id)
    session_model=SessionYearModel.object.get(id=session_year_id)
    json_sstudent=json.loads(student_ids)
    #print(data[0]['id'])


    try:
        attendance=Attendance(subject_id=subject_model,attendance_date=attendance_date,session_year_id=session_model)
        attendance.save()

        for stud in json_sstudent:
             student=Students.objects.get(admin=stud['id'])
             attendance_report=AttendanceReport(student_id=student,attendance_id=attendance,status=stud['status'])
             attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")

def staff_update_attendance(request):
    subjects=Subjects.objects.filter(staff_id=request.user.id)
    session_year_id=SessionYearModel.object.all()
    return render(request,"staff_update_attendance.html",{"subjects":subjects,"session_year_id":session_year_id})

@csrf_exempt
def get_attendance_dates(request):
    subject=request.POST.get("subject")
    session_year_id=request.POST.get("session_year_id")
    subject_obj=Subjects.objects.get(id=subject)
    session_year_obj=SessionYearModel.object.get(id=session_year_id)
    attendance=Attendance.objects.filter(subject_id=subject_obj,session_year_id=session_year_obj)
    attendance_obj=[]
    for attendance_single in attendance:
        data={"id":attendance_single.id,"attendance_date":str(attendance_single.attendance_date),"session_year_id":attendance_single.session_year_id.id}
        attendance_obj.append(data)

    return JsonResponse(json.dumps(attendance_obj),safe=False)

@csrf_exempt
def get_attendance_student(request):
    attendance_date=request.POST.get("attendance_date")
    attendance=Attendance.objects.get(id=attendance_date)

    attendance_data=AttendanceReport.objects.filter(attendance_id=attendance)
    list_data=[]

    for student in attendance_data:
        data_small={"id":student.student_id.admin.id,"name":student.student_id.admin.first_name+" "+student.student_id.admin.last_name,"status":student.status}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)

@csrf_exempt
def save_updateattendance_data(request):
    student_ids=request.POST.get("student_ids")
    attendance_date=request.POST.get("attendance_date")
    attendance=Attendance.objects.get(id=attendance_date)

    json_sstudent=json.loads(student_ids)


    try:
        for stud in json_sstudent:
             student=Students.objects.get(admin=stud['id'])
             attendance_report=AttendanceReport.objects.get(student_id=student,attendance_id=attendance)
             attendance_report.status=stud['status']
             attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")


def staff_add_result(request):
	subjects = Subjects.objects.filter(staff_id=request.user.id)
	session_years = SessionYearModel.object.all()
	context = {
		"subjects": subjects,
		"session_years": session_years,
	}
	return render(request, "staffaddresult.html", context)


@csrf_exempt
def update_attendance_data(request):
    student_ids = request.POST.get("student_ids")
 
    attendance_date = request.POST.get("attendance_date")
    attendance = Attendance.objects.get(id=attendance_date)
 
    json_student = json.loads(student_ids)
 
    try:
         
        for stud in json_student:
           
            # Attendance of Individual Student saved on AttendanceReport Model
            student = Students.objects.get(admin=stud['id'])
 
            attendance_report = AttendanceReport.objects.get(student_id=student,
                                                             attendance_id=attendance)
            attendance_report.status=stud['status']
 
            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("Error")

def staff_add_result_save(request):
	if request.method != "POST":
		messages.error(request, "Invalid Method")
		return redirect('UMS_app:staff_add_result')
	else:
		student_admin_id = request.POST.get('student_list')
		assignment_marks = request.POST.get('assignment_marks')
		exam_marks = request.POST.get('exam_marks')
		subject_id = request.POST.get('subject')

		student_obj = Students.objects.filter(admin=student_admin_id).first()
		subject_obj = Subjects.objects.filter(id=subject_id).first()

		try:
			# Check if Students Result Already Exists or not
			check_exist = StudentResult.objects.filter(subject_id=subject_obj,
													student_id=student_obj).exists()
			if check_exist:
				result = StudentResult.objects.get(subject_id=subject_obj,
												student_id=student_obj)
				result.subject_assignment_marks = assignment_marks
				result.subject_exam_marks = exam_marks
				result.save()
				messages.success(request, "Result Updated Successfully!")
				return redirect('staff_add_result')
			else:
				result = StudentResult(student_id=student_obj,
									subject_id=subject_obj,
									subject_exam_marks=exam_marks,
									subject_assignment_marks=assignment_marks)
				result.save()
				messages.success(request, "Result Added Successfully!")
				return redirect('UMS_app:staff_add_result')
		except:
			messages.error(request, "Failed to Add Result!")
			return redirect('UMS_app:staff_add_result')

def fetch_result_student(request):
	subject_id=request.POST.get('subject_id')
	student_id=request.POST.get('student_id')
	student_obj=Students.objects.get(admin=student_id)
	result=StudentResult.objects.filter(student_id=student_id,subject_id=subject_id).exists()
	if result:
		result=StudentResult.objects.get(student_id=student_id,subject_id=subject_id)
		result_data={"exam_marks":result.subject_exam_marks,"assign_marks":result.subject_assignment_marks}
		return HttpResponse(json.dumps(result_data))
	else:
		return HttpResponse("False")

def download(request,path):
    file_path=os.path.join(settings.MEDIA_ROOT,path)
    if os.path.exists(file_path):
        with open(file_path,'rb')as fh:
            response=HttpResponse(fh.read(),content_type="application/file")
            response['Content-Disposition']='inline;filename='+os.path.basename(file_path)
            return response

    raise Http404




@csrf_exempt
def add_exam(request):
        if(request.POST.get('exam_name', False) != False and request.POST.get('description', False) != False and request.POST.get('subject_id', False) != False and request.POST.get('year', False) != False and request.POST.get('status', False) != False and request.POST.get('startDate', False) != False and request.POST.get('endDate', False) != False and request.POST.get('startTime', False) != False and request.POST.get('endTime', False) != False and request.POST.get('pass_percentage', False) != False and request.POST.get('no_of_questions', False) != False and request.POST.get('attempts_allowed', False) != False):
            temp = exam_detail()
            temp.exam_name = request.POST['exam_name']
            temp.description = request.POST['description']
            temp.subject_id = Subjects.objects.get(id=request.POST['subject_id'])
            temp.year = request.POST['year']
            temp.status = request.POST['status']
            temp.start_time = request.POST['startDate']+" "+request.POST['startTime']
            temp.end_time = request.POST['endDate']+" "+request.POST['endTime']
            temp.pass_percentage = request.POST['pass_percentage']
            temp.no_of_questions = request.POST['no_of_questions']
            temp.attempts_allowed = request.POST['attempts_allowed']
            if(exam_detail.objects.filter(exam_name=temp.exam_name, subject_id = temp.subject_id, year = temp.year).count() == 0):
                temp.save()
                print("saved")
                message = "Examination was successfully added!"
                return render(request ,'template1/assignments/exam_create.html', {"message":message})
            else:
                wrong_message = "Sorry, exam already exists!"
                return render(request ,'template1/assignments/exam_create.html', {"wrong_message":wrong_message})
        else:
            print("else entered")
            return render(request ,'template1/assignments/exam_create.html', {"subjects":Subjects.objects.filter(staff_id=request.user.id)})


@csrf_exempt
def modify_exam(request):
        if(request.POST.get('id', False) != False and request.POST.get('exam_name', False) != False and request.POST.get('exam_name', False) != False and request.POST.get('description', False) != False and request.POST.get('subject_id', False) != False and request.POST.get('year', False) != False and request.POST.get('status', False) != False and request.POST.get('startDate', False) != False and request.POST.get('endDate', False) != False and request.POST.get('startTime', False) != False and request.POST.get('endTime', False) != False and request.POST.get('pass_percentage', False) != False and request.POST.get('no_of_questions', False) != False and request.POST.get('attempts_allowed', False) != False):
            #if request.method == 'POST':
            temp = exam_detail()
            print("if entered")
            temp.id = request.POST['id']
            temp.exam_name = request.POST['exam_name']
            temp.description = request.POST['description']
            temp.subject_id = Subjects.objects.get(pk=request.POST['subject_id'])
            temp.year = request.POST['year']
            temp.status = request.POST['status']
            temp.start_time = request.POST['startDate']+" "+request.POST['startTime']
            temp.end_time = request.POST['endDate']+" "+request.POST['endTime']
            temp.pass_percentage = request.POST['pass_percentage']
            temp.no_of_questions = request.POST['no_of_questions']
            temp.attempts_allowed = request.POST['attempts_allowed']
            if(exam_detail.objects.filter(exam_name=temp.exam_name, subject_id = temp.subject_id, year = temp.year).count() == 0):
                exam_detail.objects.filter(id=temp.id).update(exam_name=temp.exam_name, description=temp.description, subject_id=temp.subject_id, year=temp.year, status=temp.status, start_time=temp.start_time, end_time=temp.end_time, pass_percentage=temp.pass_percentage, no_of_questions=temp.no_of_questions, attempts_allowed=temp.attempts_allowed, modified=datetime.datetime.now())
                message = "Examination was successfully updated!"
                return render(request ,'online_exam/faculty_modify_exam.html', {"message":message, "exams": exam_detail.objects.all()})
            elif(exam_detail.objects.filter(exam_name=temp.exam_name, subject_id = temp.subject_id, year = temp.year).count() == 1 and list(exam_detail.objects.filter(exam_name=temp.exam_name, subject_id = temp.subject_id, year = temp.year).values("id"))[0]['id'] == int(request.POST['id'])):
                exam_detail.objects.filter(id=temp.id).update(exam_name=temp.exam_name, description=temp.description, subject_id=temp.subject_id, year=temp.year, status=temp.status, start_time=temp.start_time, end_time=temp.end_time, pass_percentage=temp.pass_percentage, no_of_questions=temp.no_of_questions, attempts_allowed=temp.attempts_allowed, modified=datetime.datetime.now())
                message = "Examination was successfully updated!"
                return render(request ,'template1/assignments/modify_exam.html', {"message":message, "exams": exam_detail.objects.all()})
            else:
                wrong_message = "Sorry, exam already exists!"
                return render(request ,'template1/assignments/modify_exam.html', {"wrong_message":wrong_message, "exams": exam_detail.objects.all()})
        else:
            print("else entered")
            return render(request ,'template1/assignments/modify_exam.html', {"exams":exam_detail.objects.all()})


@csrf_exempt
def update_exam(request):
        result = exam_detail.objects.get(pk= int(request.POST['id']))
        start_date = ((str(result.start_time).split())[0])
        end_date = ((str(result.end_time).split())[0])
        start_time = ((str(result.start_time).split())[1]).split("+")[0]
        end_time = ((str(result.end_time).split())[1]).split("+")[0]
        return render(request ,'template1/assignments/update_exam.html', {"result": result, "subjects":Subjects.objects.filter(staff_id=request.user.id)
, "start_date":start_date, "end_date":end_date, "start_time":start_time, "end_time":end_time})
        #print("id---------------------------------------------------------", int(request.POST['id']))

@csrf_exempt
def view_exam(request):
        data = exam_detail.objects.all()
        #print(data)
        return render(request ,'template1/assignments/view_exam.html', {"exams":exam_detail.objects.all()})


def add_question(request):
        """print(request.POST.get("question", False))
        print(request.POST.get("description", False))
        print(request.POST.get("question_type", False))
        print(request.POST.get("subtopic", False))
        print(request.POST.get("level", False))
        print(request.POST.get("exam", False))
        print(request.POST.get("score", False))
        print(request.POST.get("status", False))"""
        if(request.method == "POST" and request.POST.get("question", False) != False and request.POST.get("description", False) != False and request.POST.get("question_type", False) != False and request.POST.get("level", False) != False and request.POST.get("exam", False) != False and request.POST.get("score", False) != False and request.POST.get("status", False) != False):
            temp = question_bank()
            temp.question =request.POST["question"] 
            temp.description = request.POST["description"]
            temp.question_type = question_type.objects.get(pk=request.POST["question_type"])
            temp.level_id = level.objects.get(pk =request.POST["level"])
            temp.exam_id = exam_detail.objects.get(pk =request.POST["exam"])
            temp.score = request.POST["score"]
            temp.status = request.POST["status"]
            if(question_bank.objects.filter(question = temp.question).exists() == False):
                temp.save()
                question_id = question_bank.objects.get(question = temp.question)
                #print(temp)
                #print(temp.question_type.q_type)
                if(temp.question_type.q_type == "Multiple Choice Single Answer" or temp.question_type.q_type == "Multiple Choice Multiple Answer"):
                    for i in range(1, int(request.POST["options_number"])+1):
                        new_option = option()
                        new_option.question_id = question_id
                        new_option.option_no = i
                        new_option.option_value = request.POST["option"+str(i)]
                        new_option.save()
                    if(temp.question_type.q_type == "Multiple Choice Single Answer"):
                        temp_answer = answer()
                        temp_answer.question_id = question_id
                        temp_answer.answer = request.POST['options']
                        temp_answer.save()
                    elif(temp.question_type.q_type == "Multiple Choice Multiple Answer"):
                        answers = request.POST.getlist('options[]')
                        for i in answers:
                            new_answer = answer()
                            new_answer.question_id = question_id
                            new_answer.answer = i
                            new_answer.save()
                elif(temp.question_type.q_type == "Match the Column"):
                    for i in range(1, int(request.POST["questions_number"])+1):
                        new_row = MatchTheColumns()
                        new_row.question_id = question_id
                        new_row.question = request.POST["matchQues" + str(i)]
                        new_row.answer = request.POST["matchAns" + str(i)]
                        new_row.save()
                else:
                    temp_answer = answer()
                    temp_answer.question_id = question_id
                    temp_answer.answer = request.POST['answer']
                    temp_answer.save()
                message = "Question was successfully created!!"
                return render(request ,'template1/assignments/create_question.html',  {"subjects":Subjects.objects.filter(staff_id=request.user.id),"levels": level.objects.all(), "question_type":question_type.objects.all(),"exams":exam_detail.objects.all(), "message":message})
            else:
                wrong_message = "Sorry, question already exists under the subtopic!!"
                return render(request ,'template1/assignments/create_question.html', {"subjects":Subjects.objects.filter(staff_id=request.user.id),"levels": level.objects.all(), "question_type":question_type.objects.all(),"exams":exam_detail.objects.all(), "wrong_message":wrong_message})   
        else:
            return render(request ,'template1/assignments/create_question.html', {"subjects":Subjects.objects.filter(staff_id=request.user.id),"levels": level.objects.all(), "question_type":question_type.objects.all(),"exams":exam_detail.objects.all()})


def get_exams_by_course(request):
        exams = dict()
        j = 0
        for i in (exam_detail.objects.filter(subject_id=Subjects.objects.filter(staff_id=request.user.id).all()).values("id", "exam_name")):
            exams[i['id']] = i['exam_name']
            j += 1
        return HttpResponse(json.dumps(exams))



def modify_question(request):
        Final = dict()
        if(request.method == "POST" and request.POST.get("id", False) != False and request.POST.get("question", False) != False and request.POST.get("description", False) != False and request.POST.get("question_type", False) != False and request.POST.get("level", False) != False and request.POST.get("exam", False) != False and request.POST.get("score", False) != False and request.POST.get("status", False) != False):
            temp = question_bank()
            id = request.POST["id"]
            temp.question =request.POST["question"] 
            temp.description = request.POST["description"]
            temp.question_type = question_type.objects.get(pk=request.POST["question_type"])
            temp.level_id = level.objects.get(pk =request.POST["level"])
            temp.exam_id = exam_detail.objects.get(pk =request.POST["exam"])
            temp.score = request.POST["score"]
            temp.status = request.POST["status"]
            if(question_bank.objects.filter(question = temp.question).exists() == False or (question_bank.objects.filter(question = temp.question).count() == 1 and question_bank.objects.get(question = temp.question).id == int(request.POST['id']))):
                question_bank.objects.filter(pk = int(request.POST["id"])).update(question = temp.question, description = temp.description, question_type = temp.question_type, level_id = temp.level_id, exam_id = temp.exam_id, score = temp.score, status = temp.status, modified = datetime.datetime.now())
                question_id = question_bank.objects.get(id = int(request.POST["id"]))
                if(temp.question_type.q_type == "Multiple Choice Single Answer" or temp.question_type.q_type == "Multiple Choice Multiple Answer"):
                    option.objects.filter(question_id=question_id).delete()
                    answer.objects.filter(question_id=question_id).delete()
                    for i in range(1, int(request.POST["options_number"])+1):
                        new_option = option()
                        new_option.question_id = question_id
                        new_option.option_no = i
                        new_option.option_value = request.POST["option"+str(i)]
                        new_option.save()
                    if(temp.question_type.q_type == "Multiple Choice Single Answer"):
                        temp_answer = answer()
                        temp_answer.question_id = question_id
                        temp_answer.answer = request.POST['options']
                        temp_answer.save()
                    elif(temp.question_type.q_type == "Multiple Choice Multiple Answer"):
                        answers = request.POST.getlist('options[]')
                        for i in answers:
                            new_answer = answer()
                            new_answer.question_id = question_id
                            new_answer.answer = i
                            new_answer.save()
                elif(temp.question_type.q_type == "Match the Column"):
                    MatchTheColumns.objects.filter(question_id=question_id).delete()
                    for i in range(1, int(request.POST["questions_number"])+1):
                        new_row = MatchTheColumns()
                        new_row.question_id = question_id
                        new_row.question = request.POST["matchQues" + str(i)]
                        new_row.answer = request.POST["matchAns" + str(i)]
                        new_row.save()
                else:
                    answer.objects.filter(question_id = question_id).update(answer = request.POST['answer'])
                message = "Question was successfully modified!!"
                Final = {"message":message}
            else:
                wrong_message = "Sorry, question already exists under the subtopic!!"
                Final = {"wrong_message":wrong_message}
        V=[]
        for i in question_bank.objects.all():
            A = dict()
            A['id'] = i.id
            A['question'] = i.question
            A['description'] = i.description
            A['question_type'] = i.question_type.q_type
            if(A['question_type']  == "Multiple Choice Single Answer" or A['question_type'] == "Multiple Choice Multiple Answer"):
                options = ""
                for j in option.objects.filter(question_id = i).all():
                    options += (j.option_value + "; ")
                A['options'] = options
                answers = ""
                for j in answer.objects.filter(question_id = i).all():
                    answers += (option.objects.get(question_id = i, option_no=j.answer).option_value + "; ")
                A['answers'] = answers
            elif(A['question_type'] == "Match the Column"):
                A['options'] = "None"
                A['answers'] = ""
                for j in MatchTheColumns.objects.filter(question_id = i).all():
                    A['answers'] += j.question + " - " + j.answer + "; "
            else:
                A['options'] = "None"
                solution = answer.objects.get(question_id = i)
                A['answers'] = solution.answer
            A['level'] = i.level_id.level_name
            A['exam'] = i.exam_id.exam_name
            A['score'] = i.score
            A['created'] = i.created
            A['modified'] = i.modified
            A['status'] = i.status
            V.append(A)
            Final["questions"] = V
        return render(request ,'template1/assignments/modify_question.html', Final)


def update_question(request):
        if(request.method == "POST" and request.POST.get('id', False) != False):
            query = question_bank.objects.get(pk = int(request.POST['id']))
            ques = dict()
            ques['id'] = query.id
            ques['question'] = query.question
            ques['description'] = query.description
            ques['question_type'] = query.question_type.q_type
            ques['numbers'] = range(2, 11)
            if(ques['question_type']  == "Multiple Choice Single Answer" or ques['question_type'] == "Multiple Choice Multiple Answer"):
                ques['options'] = []
                for i in option.objects.filter(question_id = query).all():
                    if answer.objects.filter(question_id = query, answer = i.option_no).count() == 1:
                        ques['options'].append({"option_desig":chr(i.option_no+96), "option_no":i.option_no, "option_value":i.option_value, "answer": 1})
                    elif answer.objects.filter(question_id = query, answer = i.option_no).count() == 0:
                        ques['options'].append({"option_desig":chr(i.option_no+96), "option_no":i.option_no, "option_value":i.option_value, "answer": 0})               
                ques['options_number'] = option.objects.filter(question_id = query).count()
            elif(ques['question_type'] == "Match the Column"):
                ques['answers'] = []
                j = 1
                for i in MatchTheColumns.objects.filter(question_id = query).all():
                    ques['answers'].append({"ques_no": chr(96+j), "ques_value":i.question, "ans_no": j, "ans_value":i.answer})
                    j += 1
                ques['questions_number'] = MatchTheColumns.objects.filter(question_id = query).count()
            else:
                solution = answer.objects.get(question_id = query)
                ques['answers'] = solution.answer
            ques['level'] = query.level_id.id
            ques['exam'] = query.exam_id.id
            ques['subject'] = query.exam_id.subject_id.id
            ques['score'] = query.score
            ques['created'] = query.created
            ques['modified'] = query.modified
            ques['status'] = query.status
            ques['subjects'] = Subjects.objects.filter(staff_id=request.user.id)
            ques['exams'] = exam_detail.objects.filter(subject_id=query.exam_id.subject_id).all()
            ques['question_types'] = question_type.objects.all()
            ques['levels'] = level.objects.all()
        return render(request ,'template1/assignments/update_question.html', ques)


def view_question(request):
        V=[]
        for i in question_bank.objects.all():
            A = dict()
            A['question'] = i.question
            A['description'] = i.description
            A['question_type'] = i.question_type.q_type
            if(A['question_type']  == "Multiple Choice Single Answer" or A['question_type'] == "Multiple Choice Multiple Answer"):
                options = ""
                for j in option.objects.filter(question_id = i).all():
                    options += (j.option_value + "; ")
                A['options'] = options
                answers = ""
                for j in answer.objects.filter(question_id = i).all():
                    answers += (option.objects.get(question_id = i, option_no=j.answer).option_value + "; ")
                A['answers'] = answers
            elif(A['question_type'] == "Match the Column"):
                A['options'] = "None"
                A['answers'] = ""
                for j in MatchTheColumns.objects.filter(question_id = i).all():
                    A['answers'] += j.question + " - " + j.answer + "; "
            else:
                A['options'] = "None" 
                A['answers'] = answer.objects.get(question_id = i).answer
            A['level'] = i.level_id.level_name
            A['exam'] = i.exam_id.exam_name
            A['score'] = i.score
            A['created'] = i.created
            A['modified'] = i.modified
            A['status'] = i.status
            V.append(A)
        return render(request ,'template1/assignments/view_question.html',{"questions":V})


def evaluate(request):
        temp = exam_detail.objects.all()
        data=[]
        for t in temp:
            data1={}
            data1['exam_id'] = t.id
            data1['exam_name']=t.exam_name
            data1['subject'] = t.subject_id.subject_name
            data1['year'] = t.year
            data1['description']=t.description
            data1['no_of_questions']=t.no_of_questions
            data1['pass_percentage']=t.pass_percentage
            data1['duration']=t.end_time - t.start_time
            data.append(data1)
        return render(request ,'template1/assignments/evaluate.html', {"data":data})


def exam_registrations(request):
        if request.method=='POST':
            temp=registration.objects.get(pk=request.POST['user_exam_attempt_id'])
            temp.registered=1-temp.registered
            temp.save()
            return HttpResponse(temp.registered)
        temp=registration.objects.all()
        data=[]
        for i in temp:
            data1={}
            data1['first_name']=(i.user_id).first_name
            data1['last_name']=(i.user_id).last_name
            data1['email']=(i.user_id).email
            data1['exam_name']=(i.exam_id).exam_name
            data1['attempt_no']=i.attempt_no
            data1['registered']=i.registered
            data1['registered_time']=i.registered_time
            data1['exam_id']=i.id;
            data.append(data1)
        return render(request ,'template1/assignments/exam_registrations.html',{"data":data})



def register_evaluate(request):
        if(request.method == "POST" and request.POST.get("registration_id", False) != False):
            ans = registration.objects.get(pk = int(request.POST["registration_id"])).view_answers
            ans = 1 - int(ans)
            registration.objects.filter(pk = int(request.POST["registration_id"])).update(view_answers = ans)
            return HttpResponse(ans)
        query = []
        for i in registration.objects.filter(exam_id = exam_detail.objects.get(pk = request.POST["exam_id"]), answered = 1).all():
            subquery = dict()
            subquery["first_name"] = i.user_id.first_name
            subquery["last_name"] = i.user_id.last_name
            subquery["attempt_no"] = i.attempt_no
            subquery["subject"] = i.exam_id.subject_id.subject_name
            subquery["year"] = i.exam_id.year
            subquery["exam_id"] = i.exam_id.id
            subquery["id"] = i.id
            if(result.objects.filter(registration_id = i).count() == result.objects.filter(registration_id = i, verify = 1).count()):
                subquery["verify"] = 1
            else:
                subquery["verify"] = 0
            subquery["view_answers"] = i.view_answers
            subquery["score"] = result.objects.filter(registration_id = i).aggregate(Sum('score'))
            if(subquery["score"]["score__sum"] == None):
                subquery["score"] = 0
            else:
                subquery["score"] = int(subquery["score"]["score__sum"])
            query.append(subquery)
        return render(request ,'template1/assignments/register_evaluate.html', {"registrations": query})

def verify(request):
        attempted = json.loads(request.POST.get("answer", False))
        registration.objects.filter(id = request.POST["registration_id"]).update(answered = 1)
        marks = 0
        for i in attempted.keys():
            attempted_answer = dict(attempted[i])
            print(attempted_answer['answers'])
            #print(attempted_answer['question_id'])
            ans = dict()
            ques = question_bank.objects.get(pk = attempted_answer['question_id'])
            ques_type = ques.question_type.q_type
            if(ques_type == "Multiple Choice Single Answer" or ques_type == "Multiple Choice Multiple Answer"):
                for j in answer.objects.filter(question_id = ques).all():
                    opt = option.objects.get(question_id = ques, option_no=j.answer)
                    ans[opt.option_no] = opt.option_value
                temp = result()
                temp.registration_id = registration.objects.get(pk = int(request.POST["registration_id"]))
                temp.question_id = ques
                temp.answer = ""
                for j in attempted_answer["answers"].keys():
                    temp.answer += attempted_answer["answers"][j] + "; "
                if(json.dumps(ans) == json.dumps(attempted_answer['answers'])):
                    temp.score = int(attempted_answer['score'])
                else:
                    temp.score = 0
                marks += temp.score
                temp.verify = 1
                temp.save()
            elif(ques_type == "Match the Column"):
                for j in MatchTheColumns.objects.filter(question_id = ques).all():
                    ans[j.question] = j.answer
                temp = result()
                temp.question_id = ques
                temp.registration_id = registration.objects.get(pk = int(request.POST["registration_id"]))
                temp.answer = ""
                for j in attempted_answer["answers"].keys():
                    temp.answer += j + " - " + attempted_answer["answers"][j] + "; "
                if(json.dumps(ans) == json.dumps(attempted_answer['answers'])):
                    temp.score = int(attempted_answer['score'])
                else:
                    temp.score = 0
                marks += temp.score
                temp.verify = 1
                temp.save()
            else:
                temp = result()
                temp.registration_id = registration.objects.get(pk = int(request.POST["registration_id"]))
                temp.question_id = ques
                temp.answer = dict(attempted_answer['answers'])
                temp.answer = temp.answer['1']
                temp.score = 0
                temp.verify = 0
                temp.save()                 
        return HttpResponse(marks)


def manual_evaluate(request):
        if request.method == "POST":
            if request.POST.get('result_id', False) != False and request.POST.get('check', False) != False and request.POST.get('score', False) != False: 
                if(int(request.POST['check']) == 1):
                    result.objects.filter(pk = int(request.POST['result_id'])).update(score = int(request.POST['score']), verify = 1)
                elif(int(request.POST['check']) == 0):
                    result.objects.filter(pk = int(request.POST['result_id'])).update(score = 0, verify = 1)
                data = dict()
                z = 1
                for i in result.objects.filter(registration_id = registration.objects.get(pk = request.POST["user_exam_attempt_id"])).all():
                    subdata = dict()
                    subdata['question_id'] = i.question_id.id
                    subdata['question'] = i.question_id.question
                    subdata['question_type'] = i.question_id.question_type.q_type
                    if(i.question_id.question_type.id == 1 or i.question_id.question_type.id == 2):
                        opt_dict = dict()
                        for k in option.objects.filter(question_id = i.question_id.id):
                            opt_dict[k.option_no] = k.option_value
                        subdata['options'] = opt_dict
                    else:
                        subdata['options'] = ""
                    subdata["result_id"] = i.id
                    if(subdata['question_type']  == "Multiple Choice Single Answer" or subdata['question_type'] == "Multiple Choice Multiple Answer"):
                        answers = ""
                        for j in answer.objects.filter(question_id = i.question_id).all():
                            answers += (option.objects.get(question_id = i.question_id, option_no=j.answer).option_value + "; ")
                        subdata['answer'] = answers
                    elif(subdata['question_type'] == "Match the Column"):
                        subdata['answer'] = ""
                        for j in MatchTheColumns.objects.filter(question_id = i.question_id).all():
                            subdata['answer'] += j.question + " - " + j.answer + "; "
                    else: 
                        subdata['answer'] = answer.objects.get(question_id = i.question_id).answer
                    subdata['level'] = i.question_id.level_id.level_name
                    subdata['score'] = i.question_id.score
                    subdata['gained_score'] = i.score
                    subdata['your_answers'] = i.answer
                    subdata['verify'] = i.verify
                    data[z] = subdata
                    z += 1
                data = json.dumps(data)
                return HttpResponse(data)
            data = dict()
            z = 1
            for i in result.objects.filter(registration_id = registration.objects.get(pk = int(request.POST['registration_id']))).all():
                subdata = dict()
                subdata['question_id'] = i.question_id.id
                subdata['question'] = i.question_id.question
                subdata['question_type'] = i.question_id.question_type.q_type
                if(i.question_id.question_type.id == 1 or i.question_id.question_type.id == 2):
                    opt_dict = dict()
                    for k in option.objects.filter(question_id = i.question_id.id):
                        opt_dict[k.option_no] = k.option_value
                    subdata['options'] = opt_dict
                else:
                    subdata['options'] = ""
                subdata["result_id"] = i.id
                if(subdata['question_type']  == "Multiple Choice Single Answer" or subdata['question_type'] == "Multiple Choice Multiple Answer"):
                    answers = ""
                    for j in answer.objects.filter(question_id = i.question_id).all():
                        answers += (option.objects.get(question_id = i.question_id, option_no=j.answer).option_value + "; ")
                    subdata['answer'] = answers
                elif(subdata['question_type'] == "Match the Column"):
                    subdata['answer'] = ""
                    for j in MatchTheColumns.objects.filter(question_id = i.question_id).all():
                        subdata['answer'] += j.question + " - " + j.answer + "; "
                else: 
                    subdata['answer'] = answer.objects.get(question_id = i.question_id).answer
                subdata['level'] = i.question_id.level_id.level_name
                subdata['score'] = i.question_id.score
                subdata['gained_score'] = i.score
                subdata['your_answers'] = i.answer
                subdata['verify'] = i.verify
                data[z] = subdata
                z += 1
            data = json.dumps(data)
            return render(request ,'template1/assignments/manual_evaluate.html', {"data":data, "exam_id":1, "registration_id":1})


class AssignmentCreateView(CreateView):
    template_name = 'template1/assignments/assignment_create.html'
    form_class = AssignmentCreateForm
    extra_context = {
        'title': 'New Course'
    }
    success_url = reverse_lazy('UMS_app:assignment-list')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy('login')
        if self.request.user.is_authenticated and self.request.user.role != 'staff':
            return reverse_lazy('login')
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AssignmentCreateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


# VIEW FOR ASSIGNMENT LIST
class AssignmentView(ListView):
    model = Assignment
    template_name = 'template1/assignments/assignments.html'
    context_object_name = 'assignment'

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    # @method_decorator(user_is_student, user_is_instructor)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.all()  # filter(user_id=self.request.user.id).order_by('-id')


class AssignmentSubmissionListView(ListView):
    model = AssignmentSubmission
    template_name = 'template1/assignments/assignment_submission_list.html'
    context_object_name = 'assignment_submission'

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    # @method_decorator(user_is_instructor, user_is_student)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.all().order_by('-id')  # filter(user_id=self.request.user.id).order_by('-id')

