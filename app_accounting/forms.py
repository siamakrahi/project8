from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, PasswordChangeForm, AuthenticationForm
from django.core.mail import EmailMessage
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from app_accounting.models import User, MessagingModel, ConsultingModel


class CustomUserCreationForm(UserCreationForm):
    """
    Custom form for user registration.
    """
    password1 = forms.CharField(
        label="رمز عبور",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور خود را وارد کنید'
        }),
        help_text="""
        <ul class="password-help-text">
            <li>رمز عبور باید حداقل 8 کاراکتر داشته باشد</li>
            <li>نباید شبیه اطلاعات شخصی شما باشد</li>
            <li>نباید از پسوردهای رایج استفاده کنید</li>
            <li>باید شامل حروف و اعداد باشد</li>
        </ul>
        """
    )
    
    password2 = forms.CharField(
        label="تکرار رمز عبور",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور خود را مجدداً وارد کنید'
        }),
        help_text="برای تأیید، رمز عبور قبلی را دوباره وارد کنید"
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
        labels = {
            'username': 'نام کاربری',
            'email': 'ایمیل'
        }
        
        help_texts = {
            'username': 'حداقل 4 کاراکتر، فقط حروف، اعداد و @/./+/-/_ مجاز هستند',
            'email': 'لطفاً یک ایمیل معتبر وارد کنید'
        }
        
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام کاربری خود را وارد کنید'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ایمیل خود را وارد کنید'}),
        }

    def clean_email(self):
        """
        Validate email uniqueness.
        """
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("این ایمیل قبلاً استفاده شده است.")
        return email
        

class MyPasswordChangeForm(PasswordChangeForm):
    """
    Custom password change form.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ["old_password", "new_password1", "new_password2"]:
            self.fields[field_name].widget = forms.PasswordInput()


class MessagingForm(forms.ModelForm):
    """
    Form for user messaging submissions.
    """
    class Meta:
        model = MessagingModel
        fields = ["name", "email", "phone_number", "your_comment"]
        labels = {
            "name": "نام",
            "email": "ایمیل",
            "phone_number": "شماره تماس",
            "your_comment": "پیام شما",
        }


class ConsultingForm(forms.ModelForm):
    """
    Form for user consulting submissions.
    """
    class Meta:
        model = ConsultingModel
        fields = ["name", "email", "phone_number"]
        labels = {
            "name": "نام",
            "email": "ایمیل",
            "phone_number": "شماره تماس",
        }


class CustomPasswordResetForm(PasswordResetForm):
    """
    Custom password reset form with email sending functionality.
    """
    def send_mail(self, subject_template_name, email_template_name, context, from_email, to_email, html_email_template_name=None):
        subject = render_to_string(subject_template_name, context).strip()  
        body = render_to_string(email_template_name, context) 
        email_message = EmailMessage(subject, body, from_email, [to_email])
        email_message.send()
  
      
class ProfileForm(forms.ModelForm):
    """
    Form for updating user profile.
    """
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "avatar", "about"]
        labels = {
            "first_name": "نام",
            "last_name": "نام خانوادگی",
            "email": "ایمیل",
            "avatar": "عکس پروفایل",
            "about": "درباره من",
        }
        widgets = {
            "about": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }
