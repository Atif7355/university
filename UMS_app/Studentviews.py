from django.shortcuts import render, redirect
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from .forms import AssignmentSubmissionForm
import datetime,json,math
from .models import CustomUser,registration,Assignment,AssignmentSubmission,exam_detail,result,answer,question_bank,option,MatchTheColumns, Students,LeaveReportStudent, StudentResult,Subjects,Attendance,AttendanceReport
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, CreateView, ListView, DeleteView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from pathlib import Path,os
from django.conf import settings
from django.utils import timezone
from django.db.models import Sum
from UMS_app import forms





def student_home1(request):
    return render(request, "studenthome.html")
    
def student_home2(request):
    return render(request, "studenthome.html")


def student_apply_leave(request):
	student_obj = Students.objects.get(admin=request.user.id)
	leave_data = LeaveReportStudent.objects.filter(student_id=student_obj)
	context = {
		"leave_data": leave_data
	}
	return render(request, 'studentapplyleave.html', context)


def student_apply_leave_save(request):
	if request.method != "POST":
		messages.error(request, "Invalid Method")
		return redirect('UMS_app:student_apply_leave')
	else:
		leave_date = request.POST.get('leave_date')
		leave_message = request.POST.get('leave_message')

		student_obj = Students.objects.filter(admin=request.user.id).first()
		try:
			leave_report = LeaveReportStudent(student_id=student_obj,
											leave_date=leave_date,
											leave_message=leave_message,
											leave_status=0)
			leave_report.save()
			messages.success(request, "Applied for Leave.")
			return redirect('UMS_app:student_apply_leave')
		except:
			messages.error(request, "Failed to Apply Leave")
			return redirect('UMS_app:student_apply_leave')



def student_view_result(request):
	student = Students.objects.get(admin=request.user.id)
	student_result = StudentResult.objects.filter(student_id=student.id)
	context = {
		"student_result": student_result,
	}
	return render(request, "viewmarks.html", context)

def student_view_attendance(request):
    student=Students.objects.get(admin=request.user.id)
    course=student.course_id
    subjects=Subjects.objects.filter(course_id=course)
    return render(request,"student_view_attendance.html",{"subjects":subjects})

def student_view_attendance_post(request):
    subject_id=request.POST.get("subject")
    start_date=request.POST.get("start_date")
    end_date=request.POST.get("end_date")

    start_data_parse=datetime.datetime.strptime(start_date,"%Y-%m-%d").date()
    end_data_parse=datetime.datetime.strptime(end_date,"%Y-%m-%d").date()
    subject_obj=Subjects.objects.get(id=subject_id)
    user_object=CustomUser.objects.get(id=request.user.id)
    stud_obj=Students.objects.get(admin=user_object)

    attendance=Attendance.objects.filter(attendance_date__range=(start_data_parse,end_data_parse),subject_id=subject_obj)
    attendance_reports=AttendanceReport.objects.filter(attendance_id__in=attendance,student_id=stud_obj)
    return render(request,"student_attendance_data.html",{"attendance_reports":attendance_reports})

def download(request,path):
    file_path=os.path.join(settings.MEDIA_ROOT,path)
    if os.path.exists(file_path):
        with open(file_path,'rb')as fh:
            response=HttpResponse(fh.read(),content_type="application/file")
            response['Content-Disposition']='inline;filename='+os.path.basename(file_path)
            return response

    raise Http404


def exams(request):
        Final = dict()
        if(request.method == "POST" and request.POST.get('exam_id', False) != False):
            temp = registration()
            temp.user_id = CustomUser.objects.get(id = request.user.id)
            temp.exam_id = exam_detail.objects.get(id = int(request.POST['exam_id']))
            temp.attempt_no = registration.objects.filter(user_id = temp.user_id, exam_id = temp.exam_id).count() + 1
            temp.save()
            Final["message"] = "Applied for registration successfully!!"
        exams = []
        for i in exam_detail.objects.filter(status="1").all():
            tmpdct = dict()
            tmpdct["id"] = i.id
            tmpdct["exam_name"] = i.exam_name
            tmpdct["description"] = i.description
            tmpdct["subject_name"] = i.subject_id.subject_name
            tmpdct["year"] = i.year
            user_id = CustomUser.objects.get(id = request.user.id)
            exam_id = i
            tmpdct["attempts_left"] = int(i.attempts_allowed) - registration.objects.filter(user_id = user_id, exam_id = exam_id).count()
            exams.append(tmpdct)
        Final["exams"] = exams
        return render(request, 'template1/students/exams.html', Final)

def attempt_exam(request):
        questions = question_bank.objects.filter(exam_id = exam_detail.objects.get(id = int(request.POST['exam_id']))).all()
        K = dict()
        registration_id = request.POST['registration_id']
        exam_id = ""
        j = 0
        for i in questions:
            L = dict()
            L['question_id'] = i.id
            L['question'] = i.question
            L['question_type'] = i.question_type.q_type
            if(i.question_type.id == 1 or i.question_type.id == 2):
                opt_dict = dict()
                for k in option.objects.filter(question_id = i.id):
                    opt_dict[k.option_no] = k.option_value
                L['options'] = opt_dict
            else:
                L['options'] = ""
            #L['answer'] = dict(answer.objects.filter(question_id = i.id).values("answer"))
            if(i.question_type.id == 5):
                m = 1
                L['mtcQuestions'] = dict()
                L['mtcAnswers'] = dict()
                for l in MatchTheColumns.objects.filter(question_id = i).all():
                    L['mtcQuestions'][m] = l.question    
                    m += 1
                m = 1
                for l in MatchTheColumns.objects.filter(question_id = i).order_by('?').all():
                    L['mtcAnswers'][m] = l.answer    
                    m += 1
            L['level'] = i.level_id.level_name
            L['score'] = i.score
            L['exam'] = i.exam_id.exam_name
            exam_id = i.exam_id.id
            L['subject'] = i.exam_id.subject_id.subject_name
            j += 1
            K[j] = L
        final = json.dumps(K)
        a = datetime.datetime(i.exam_id.start_time.year,i.exam_id.start_time.month,i.exam_id.start_time.day,i.exam_id.start_time.hour,i.exam_id.start_time.minute,i.exam_id.start_time.second)
        b = datetime.datetime(i.exam_id.end_time.year,i.exam_id.end_time.month,i.exam_id.end_time.day,i.exam_id.end_time.hour,i.exam_id.end_time.minute,i.exam_id.end_time.second)
        seconds = math.floor((b-a).total_seconds())
        print(seconds)
        return render(request, 'template1/students/attempt_exam.html', {"myArray":final, "sizeMyArray":j, "exam_id":exam_id, "registration_id":registration_id, "seconds": seconds})


def approved_exams(request):
        Final = []
        for i in registration.objects.filter(user_id = CustomUser.objects.get(pk = int(request.user.id)), registered = 1): 
            exams = dict()
            exams["registration_id"] = i.id
            exams["exam_id"] = i.exam_id.id
            exams["exam_name"] = i.exam_id.exam_name
            exams["start_time"] = i.exam_id.start_time
            exams["end_time"] = i.exam_id.end_time
            exams["subject_name"] = i.exam_id.subject_id.subject_name
            exams["description"] = i.exam_id.description
            exams["attempt_no"] = i.attempt_no
            exams["no_of_questions"] = i.exam_id.no_of_questions
            exams["pass_percentage"] = i.exam_id.pass_percentage
            start_time = i.exam_id.start_time
            end_time = i.exam_id.end_time
            if(start_time <= timezone.now() and end_time >= timezone.now() and i.answered == 0 and i.registered == 1):
                exams["attemptable"] = 1
            else:
                exams["attemptable"] = 0
            Final.append(exams)
        return render(request, 'template1/students/approved_exams.html', {"exams":Final, "current_time":datetime.datetime.now()}) 


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

def progress(request):
        query = []
        for i in registration.objects.filter(user_id = CustomUser.objects.get(pk = request.user.id), answered = 1, view_answers = 1).all():
            subquery = dict()
            subquery["exam_name"] = i.exam_id.exam_name
            subquery["attempt_no"] = i.attempt_no
            subquery["subject"] = i.exam_id.subject_id.subject_name
            subquery["year"] = i.exam_id.year
            subquery["id"] = i.id
            if(result.objects.filter(registration_id = i).count() == result.objects.filter(registration_id = i, verify = 1).count()):
                subquery["verify"] = 1
            else:
                subquery["verify"] = 0
            subquery["view_answers"] = i.view_answers
            subquery["score"] = result.objects.filter(registration_id = i).aggregate(Sum('score'))
            if(subquery["score"] == None):
                subquery["score"] = 0
            else:
                subquery["score"] = int(subquery["score"]["score__sum"])
            query.append(subquery)
        return render(request, 'template1/students/progress.html', {"registrations":query})


def answer_key(request):
        data = []
        for i in result.objects.filter(registration_id = registration.objects.get(pk = request.POST['registration_id'])).all():
            subdata = dict()
            subdata['question_id'] = i.question_id.id
            subdata['question'] = i.question_id.question
            subdata['question_type'] = i.question_id.question_type.q_type
            if(i.question_id.question_type.id == 1 or i.question_id.question_type.id == 2):
                options = ""
                for j in option.objects.filter(question_id = i.question_id.id).all():
                    options += (j.option_value + "; ")
                subdata['options'] = options
            else:
                subdata['options'] = "-"
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
            data.append(subdata)
        return render(request, 'template1/students/answer_key.html', {"data":data})


class AssignmentSubmissionView(CreateView):
    template_name = 'template1/assignments/assignment_submission.html'
    form_class = AssignmentSubmissionForm
    extra_context = {
        'title': 'New Exam'
    }
    success_url = reverse_lazy('UMS_app:student_home1')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy('login')
        if self.request.user.is_authenticated and self.request.user.role != 'student':
            return reverse_lazy('login')
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AssignmentSubmissionView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)




class AssignmentView1(ListView):
    model = Assignment
    template_name = 'template1/assignments/assignment1.html'
    context_object_name = 'assignment'

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    # @method_decorator(user_is_student, user_is_instructor)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.all()  # filter(user_id=self.request.user.id).order_by('-id')
