from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, AssignmentForm, SubmissionForm, GradeForm,LoginForm
from .models import CustomUser,Assignment, Submission
from django.http import FileResponse

import os


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # ✅ Redirect based on role
            if hasattr(user, "student"):
                return redirect("student_dashboard")
            elif hasattr(user, "lecturer"):
                return redirect("lecturer_dashboard")
            else:
                # fallback (no role)
                return redirect("index")
        else:
            messages.error(request, "Invalid username or password")
    
    return render(request, "login.html")

    return render(request, "login.html")

def view_scores(request):
    # Fetch all submissions for the logged-in student
    submissions = Submission.objects.filter(student=request.user)

    return render(request, 'view_scores.html', {'submissions': submissions})

@login_required
def grade_submission(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)

    # ✅ Ensure only lecturers can grade
    if request.user.role != 'lecturer':
        messages.error(request, "You are not authorized to grade.")
        return redirect("home")

    if request.method == "POST":
        form = GradeForm(request.POST, instance=submission)
        if form.is_valid():
            form.save()
            messages.success(request, "Grade and feedback submitted successfully!")
            return redirect("lecturer_dashboard")   # ✅ redirect to lecturer dashboard
    else:
        form = GradeForm(instance=submission)

    return render(request, "grade_submission.html", {
        "form": form,
        "submission": submission,
    })

def assignment_detail(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    submissions = Submission.objects.filter(assignment=assignment)
    return render(request, "assignment_detail.html", {
        "assignment": assignment,
        "submissions": submissions
    })

@login_required
def download_assignments(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    return FileResponse(assignment.file.open('rb'), as_attachment=True, filename=os.path.basename(assignment.file.name))

@login_required
def upload_assignment(request):
    if request.method == "POST":
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.lecturer = request.user  # link lecturer
            assignment.save()
            messages.success(request, "✅ Assignment uploaded successfully!")
            return redirect("lecturer_dashboard")  # redirect to dashboard
    else:
        form = AssignmentForm()
    return render(request, "upload_assignment.html", {"form": form})

@login_required
def submit_assignment(request, assignment_id):
    if request.user.role != "student":
        if request.user.role == "lecturer":
            return redirect("lecturer_dashboard")
        else:
            return redirect("student_dashboard")  # fallback

    assignment = get_object_or_404(Assignment, id=assignment_id)

    if request.method == "POST":
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.assignment = assignment
            submission.student = request.user
            submission.save()
            return redirect("student_dashboard")
    else:
        form = SubmissionForm()
    return render(request, "submit_assignment.html", {"form": form, "assignment": assignment})



@login_required
def list_assignments(request):
    assignments = Assignment.objects.all().order_by("-created_at")
    return render(request, "list_assignments.html", {"assignments": assignments})





def index(request):
    # If user is logged in, redirect to their dashboard
   
    # If not logged in, show homepage
    return render(request, "index.html")
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if user.role == "student":
                return redirect("student_dashboard")
            elif user.role == "lecturer":
                return redirect("lecturer_dashboard")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


# portal/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
@login_required
def student_dashboard(request):
    if request.user.role != "student":
        return redirect("index")  

    submissions = Submission.objects.filter(student=request.user)
    return render(request, "student_dashboard.html", {"submissions": submissions})

@login_required
def lecturer_dashboard(request):
    assignments = Assignment.objects.filter(lecturer=request.user)
    submissions = Submission.objects.all()

    context = {
        "assignments": assignments,
        "submissions": submissions
    }
    return render(request, "lecturer_dashboard.html", context)

@login_required
def logout_view(request):
    logout(request)
    return redirect("index")
def give_feedback(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)

    if request.method == 'POST':
        form = GradeForm(request.POST, instance=submission)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Feedback sent successfully!")
            return redirect('lecturer_dashboard')
    else:
        form = GradeForm(instance=submission)

    return render(request, 'give_feedback.html', {'form': form, 'submission': submission})