from django import forms
from .models import Courses, SessionYearModel,Assignment,AssignmentSubmission
from UMS_app import models


class DateInput(forms.DateInput):
    input_type = "date"


class AddStudentForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(
        attrs={"class": "form-control"}))
    password = forms.CharField(label="Password", max_length=50,
                               widget=forms.PasswordInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(
        attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(
        attrs={"class": "form-control"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(
        attrs={"class": "form-control"}))
    role = forms.CharField(label="Role", max_length=50, widget=forms.TextInput(
        attrs={"class": "form-control"}))

    # For Displaying Courses
    try:
        courses = Courses.objects.all()
        course_list = []
        for course in courses:
            single_course = (course.id, course.course_name)
            course_list.append(single_course)
    except:
        print("here")
        course_list = []

    # For Displaying Session Years
    try:
        session_years = SessionYearModel.object.all()
        session_year_list = []
        for session_year in session_years:
            single_session_year = (session_year.id, str(
                session_year.session_start_year)+" to "+str(session_year.session_end_year))
            session_year_list.append(single_session_year)

    except:
        session_year_list = []

    gender_list = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )
    course_id = forms.ChoiceField(label="Course",
                                  choices=course_list,
                                  widget=forms.Select(attrs={"class": "form-control"}))
    gender = forms.ChoiceField(label="Gender",
                               choices=gender_list,
                               widget=forms.Select(attrs={"class": "form-control"}))
    session_year_id = forms.ChoiceField(label="Session Year",
                                        choices=session_year_list,
                                        widget=forms.Select(attrs={"class": "form-control"}))

class AssignmentCreateForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'content', 'file', 'marks','due_date', 'duration']

    def __init__(self, *args, **kwargs):
        super(AssignmentCreateForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = "Assignment Name"
        self.fields['content'].label = "Content"
        self.fields['file'].label = " Upload File"
        self.fields['marks'].label = "Marks"
        self.fields['due_date'].label = "Due Date"
        self.fields['duration'].label = "Duration"

        self.fields['title'].widget.attrs.update(
            {
                'placeholder': 'Enter A Name',
            }
        )

        self.fields['content'].widget.attrs.update(
            {
                'placeholder': 'Content',
            }
        )

        self.fields['file'].widget.attrs.update(
            {
                'placeholder': 'Upload Your FILE Here',
            }
        )

        self.fields['marks'].widget.attrs.update(
            {
                'placeholder': 'Enter Marks',
            }
        )

        self.fields['due_date'].widget.attrs.update(
            {
                'placeholder': 'Enter Due Date',
            }
        )

        self.fields['duration'].widget.attrs.update(
            {
                'placeholder': '3 hour, 2 hour etc ...',
            }
        )

    def is_valid(self):
        valid = super(AssignmentCreateForm, self).is_valid()

        # if already valid, then return True
        if valid:
            return valid
        return valid

    def save(self, commit=True):
        course = super(AssignmentCreateForm, self).save(commit=False)
        if commit:
            course.save()
        return course

class AssignmentSubmissionForm(forms.ModelForm):
    class Meta:
        model = AssignmentSubmission
        fields = ['name', 'university_id', 'content', 'file']

    def __init__(self, *args, **kwargs):
        super(AssignmentSubmissionForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = " Name"
        self.fields['university_id'].label = "University Id"
        self.fields['content'].label = "Answer"
        self.fields['file'].label = "Upload File"

        self.fields['name'].widget.attrs.update(
            {
                'placeholder': 'Write Your Name',
            }
        )

        self.fields['university_id'].widget.attrs.update(
            {
                'placeholder': 'Write Your Id',
            }
        )

        self.fields['content'].widget.attrs.update(
            {
                'placeholder': 'Write Your Answer Here',
            }
        )

        self.fields['file'].widget.attrs.update(
            {
                'placeholder': 'Upload Your FILE Here',
            }
        )

    def is_valid(self):
        valid = super(AssignmentSubmissionForm, self).is_valid()

        # if already valid, then return True
        if valid:
            return valid
        return valid

    def save(self, commit=True):
        course = super(AssignmentSubmissionForm, self).save(commit=False)
        if commit:
            course.save()
        return course