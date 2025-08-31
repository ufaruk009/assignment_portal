from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("student/dashboard/", views.student_dashboard, name="student_dashboard"),
    path("lecturer/dashboard/", views.lecturer_dashboard, name="lecturer_dashboard"),
    path("assignments/", views.list_assignments, name="list_assignments"),
    path("assignments/upload/", views.upload_assignment, name="upload_assignment"),
    path("assignments/<int:assignment_id>/submit/", views.submit_assignment, name="submit_assignment"),
    path("assignments/<int:assignment_id>/download/", views.download_assignments, name="download_assignments"),
    path("submission/<int:submission_id>/grade/", views.grade_submission, name="grade_submission"),
    path("feedback/<int:submission_id>/", views.give_feedback, name="give_feedback"),
    path('student/scores/', views.view_scores, name='view_scores'),
    path("assignment/<int:pk>/", views.assignment_detail, name="assignment_detail"),

]

