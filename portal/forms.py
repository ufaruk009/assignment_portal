from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser,Assignment, Submission



class GradeForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['grade', 'comment']
        widgets = {
            'grade': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter Grade (A, B, C...)'}),
            'comment': forms.Textarea(attrs={'class': 'form-textarea', 'placeholder': 'Feedback/Comment'}),
        }


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ["title", "description", "file", "deadline"]

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ["submitted_file"]

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            "class": "w-full p-2 border rounded focus:ring-2 focus:ring-green-500",
            "placeholder": "Username"
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "w-full p-2 border rounded focus:ring-2 focus:ring-green-500",
            "placeholder": "Password"
        })
    )


class RegisterForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=CustomUser.ROLE_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'flex gap-4 text-green-700'
        })
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full border rounded-lg p-3 focus:ring-2 focus:ring-green-500 focus:outline-none',
                'placeholder': 'Enter username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full border rounded-lg p-3 focus:ring-2 focus:ring-green-500 focus:outline-none',
                'placeholder': 'Enter email address'
            }),
        }

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        # Remove labels & help_text
        for field in self.fields.values():
            field.label = ""
            field.help_text = ""

        # ✅ Manually style password fields since they aren’t in Meta.widgets
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'class': 'w-full border rounded-lg p-3 focus:ring-2 focus:ring-green-500 focus:outline-none',
            'placeholder': 'Create a strong password'
        })
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'class': 'w-full border rounded-lg p-3 focus:ring-2 focus:ring-green-500 focus:outline-none',
            'placeholder': 'Confirm your password'
        })

