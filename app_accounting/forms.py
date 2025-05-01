from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, PasswordChangeForm, AuthenticationForm
from django.core.mail import EmailMessage
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from app_accounting.models import User, MessagingModel, ConsultingModel
from django_otp.forms import OTPTokenForm
from django import forms
from .models import User
import phonenumbers
from django.core.exceptions import ValidationError


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


class TwoFactorMethodForm(forms.Form):
    TWO_FACTOR_CHOICES = [
        ('sms', 'ارسال کد تأیید via SMS'),
        ('totp', 'برنامه احراز هویت (مانند Google Authenticator)'),
    ]
    
    method = forms.ChoiceField(
        choices=TWO_FACTOR_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input'
        }),
        label="روش احراز هویت دو مرحله‌ای",
        help_text="لطفاً روش مورد نظر خود برای دریافت کد تأیید را انتخاب کنید"
    )
    
    phone_number = forms.CharField(
        required=False,
        label="شماره تلفن همراه",
        help_text="شماره تلفن همراه معتبر با پیش‌شماره ایران (مثال: 09123456789)",
        widget=forms.TextInput(attrs={
            'placeholder': '09123456789',
            'class': 'form-control',
            'data-required-if': 'sms'
        }),
        validators=[]
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # اگر کاربر شماره تلفن دارد، به عنوان مقدار اولیه قرار دهید
        if self.user and self.user.phone_number:
            self.fields['phone_number'].initial = self.user.phone_number

    def clean_phone_number(self):
        """اعتبارسنجی شماره تلفن"""
        phone = self.cleaned_data.get('phone_number')
        method = self.cleaned_data.get('method')
        
        if method == 'sms':
            if not phone:
                raise ValidationError("برای روش SMS، شماره تلفن الزامی است.")
            
            try:
                parsed = phonenumbers.parse(phone, 'IR')
                if not phonenumbers.is_valid_number(parsed):
                    raise ValidationError("شماره تلفن وارد شده معتبر نیست.")
                
                return phonenumbers.format_number(
                    parsed, 
                    phonenumbers.PhoneNumberFormat.E164
                )
            except phonenumbers.phonenumberutil.NumberParseException:
                raise ValidationError("فرمت شماره تلفن صحیح نیست. مثال صحیح: 09123456789")
        
        return phone

    def clean(self):
        cleaned_data = super().clean()
        method = cleaned_data.get('method')
        
        # اگر کاربر انتخاب کرده است، اطلاعات را ذخیره کنید
        if self.user and method:
            self.user.two_factor_method = method
            if method == 'sms':
                self.user.phone_number = cleaned_data.get('phone_number')
            self.user.save()
        
        return cleaned_data