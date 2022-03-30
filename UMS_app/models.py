from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
import uuid




class SessionYearModel(models.Model):
	id = models.AutoField(primary_key=True)
	session_start_year = models.DateField()
	session_end_year = models.DateField()
	object = models.Manager()



# Overriding the Default Django Auth
# User and adding One More Field (user_type)
class CustomUser(AbstractUser):
	
	role = models.CharField(max_length=12, error_messages={
        'required': "Role must be provided"
    })

	user_type_data = ((1, "HOD"), (2, "Staff"), (3, "Student"))
	user_type = models.CharField(default=1, choices=user_type_data, max_length=10)

	EMAIL_TO_USER_TYPE_MAP = {
        'hod': '1',
        'staff': '2',
        'student': '3'
    }
    


class AdminHOD(models.Model):
	id = models.AutoField(primary_key=True)
	admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = models.Manager()


class Staffs(models.Model):
	id = models.AutoField(primary_key=True)
	admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
	address = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = models.Manager()



class Courses(models.Model):
	id = models.AutoField(primary_key=True)
	course_name = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = models.Manager()

	


class Subjects(models.Model):
	id =models.AutoField(primary_key=True)
	subject_name = models.CharField(max_length=255)
	# need to give default course
	course_id = models.ForeignKey(Courses, on_delete=models.CASCADE, default=1)
	staff_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = models.Manager()
	

class Students(models.Model):
	id = models.AutoField(primary_key=True)
	admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
	gender = models.CharField(max_length=50)
	address = models.TextField()
	course_id = models.ForeignKey(Courses, on_delete=models.DO_NOTHING, default=1)
	session_year_id = models.ForeignKey(SessionYearModel, null=True,
										on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	fcm_token=models.TextField(default="")
	objects = models.Manager()




class LeaveReportStudent(models.Model):
	id = models.AutoField(primary_key=True)
	student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
	leave_date = models.CharField(max_length=255)
	leave_message = models.TextField()
	leave_status = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = models.Manager()


class LeaveReportStaff(models.Model):
	id = models.AutoField(primary_key=True)
	staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
	leave_date = models.CharField(max_length=255)
	leave_message = models.TextField()
	leave_status = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = models.Manager()



class StudentResult(models.Model):
	id = models.AutoField(primary_key=True)
	student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
	subject_id = models.ForeignKey(Subjects, on_delete=models.CASCADE, default=1)
	subject_exam_marks = models.FloatField(default=0)
	subject_assignment_marks = models.FloatField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = models.Manager()


class Feedback(models.Model):
    uname = models.CharField(max_length=122)
    email = models.CharField(max_length=122)
    experience = models.CharField(max_length=12)
    comments = models.TextField()
    date = models.DateField()

class Contact(models.Model):
    name = models.CharField(max_length=122)
    email = models.CharField(max_length=122)
    phone = models.CharField(max_length=12)
    desc = models.TextField()
    date = models.DateField()

def __str__(self):
  return self.name



class level(models.Model):
    level_name = models.CharField(default = "", max_length = 100)
    def __str__(self):
        return str(self.id) + "; " + str(self.level_name)



class question_type(models.Model):
    q_type = models.CharField(default = "", max_length = 100)
    def __str__(self):
        return str(self.id) + "; " + str(self.q_type)






class Attendance(models.Model):
    id=models.AutoField(primary_key=True)
    subject_id=models.ForeignKey(Subjects,on_delete=models.DO_NOTHING)
    attendance_date=models.DateField()
    created_at=models.DateTimeField(auto_now_add=True)
    session_year_id=models.ForeignKey(SessionYearModel,on_delete=models.CASCADE)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class AttendanceReport(models.Model):
    id=models.AutoField(primary_key=True)
    student_id=models.ForeignKey(Students,on_delete=models.DO_NOTHING)
    attendance_id=models.ForeignKey(Attendance,on_delete=models.CASCADE)
    status=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()




class exam_detail(models.Model):
    exam_name = models.CharField(default = "", max_length = 100)
    description = models.TextField(null="True", blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    no_of_questions = models.IntegerField()
    attempts_allowed = models.IntegerField()
    pass_percentage = models.IntegerField()
    subject_id = models.ForeignKey(Subjects, on_delete = models.CASCADE)
    year = models.IntegerField()
    status = models.IntegerField(default = 1)
    created = models.DateTimeField(default = timezone.now)
    modified = models.DateTimeField(default = timezone.now)
    def __str__(self):
        return str(self.id) + "; " + str(self.exam_name) + "; " + str(self.description) + "; " + str(self.start_time) + "; " + str(self.end_time) + "; " + str(self.no_of_questions) + "; " + str(self.attempts_allowed) + "; " + str(self.pass_percentage) + "; " + str(self.course_id) + "; " + str(self.year) + "; " + str(self.status) + "; " + str(self.created) + "; " + str(self.modified)


class question_bank(models.Model):
    question = models.TextField(null="True", blank=True)
    description = models.TextField(null="True", blank=True)
    question_type = models.ForeignKey(question_type, on_delete = models.CASCADE)
    level_id = models.ForeignKey(level, on_delete = models.CASCADE)
    exam_id = models.ForeignKey(exam_detail, on_delete =models.CASCADE)
    score = models.FloatField()
    status = models.IntegerField(default = 1)
    created = models.DateTimeField(default = timezone.now)
    modified = models.DateTimeField(default = timezone.now)
    def __str__(self):
        return str(self.id) + "; " + str(self.question) + "; " + str(self.description) + "; " + str(self.question_type) + "; " + str(self.subtopic_id) + "; " + str(self.level_id) + "; " + str(self.exam_id) + "; " + str(self.score) + "; " + str(self.status) + "; " +  str(self.created) + "; " + str(self.modified)

class registration(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    exam_id = models.ForeignKey(exam_detail, on_delete = models.CASCADE)
    attempt_no = models.IntegerField()
    registered = models.IntegerField(default = 0)
    view_answers  = models.IntegerField(default = 0)
    answered = models.IntegerField(default = 0)
    registered_time = models.DateTimeField(default = timezone.now)
    def __str__(self):
        return str(self.id) + "; " + str(self.user_id) + "; " + str(self.exam_id) + "; " + str(self.attempt_no) + "; " + str(self.registered) + "; " + str(self.view_answers) + "; " + str(self.answered) + "; " + str(self.registered_time)

class result(models.Model):
    registration_id = models.ForeignKey(registration, on_delete = models.CASCADE)
    question_id = models.ForeignKey(question_bank, on_delete = models.CASCADE)
    answer = models.TextField(null="True", blank=True)
    score = models.FloatField()
    verify = models.IntegerField(default = 0)
    def __str__(self):  
        return str(self.id) + "; " + str(self.registration_id) + "; " + str(self.question_id) + "; " + str(self.answer) + "; " + str(self.score) + "; " + str(self.verify) 

class option(models.Model):
    question_id = models.ForeignKey(question_bank, on_delete=models.CASCADE)
    option_no = models.IntegerField()
    option_value = models.TextField(null="True", blank=True)
    def __str__(self):
        return str(self.id) + "; " + str(self.question_id) + "; " + str(self.option_no) + "; " + str(self.option_value)

class answer(models.Model):
    question_id = models.ForeignKey(question_bank, on_delete=models.CASCADE)
    answer = models.TextField(null="True", blank=True)
    def __str__(self):
        return str(self.id) + "; " + str(self.question_id) + "; " + str(self.answer)

class MatchTheColumns(models.Model):
    question_id = models.ForeignKey(question_bank, on_delete=models.CASCADE)
    question = models.TextField(null="True", blank=True)
    answer = models.TextField(null="True", blank=True)
    def __str__(self):
        return str(self.id) + "; " + str(self.question_id) + "; " + str(self.question) + "; " + str(self.answer)

class Assignment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    file = models.FileField(upload_to='media')
    marks = models.CharField(max_length=20)
    created_at = models.DateTimeField(default=timezone.now())
    due_date = models.DateField()

    def __str__(self):
        return self.title


class AssignmentSubmission(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    university_id = models.CharField(max_length=100)
    content = models.TextField()
    file = models.FileField(upload_to='media')

    def __str__(self):
        return self.university_id
