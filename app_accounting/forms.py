"""
Forms for accounting application.

Contains custom forms for:
- User registration and authentication
- Profile management
- Two-factor authentication setup
- Service-related features
"""
import phonenumbers

from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, PasswordChangeForm, AuthenticationForm
from django.core.mail import EmailMessage
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from app_accounting.models import User, MessagingModel, ConsultingModel
from django_otp.forms import OTPTokenForm
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordResetForm
from django.utils.safestring import mark_safe
from .models import User


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label="نام کاربری",
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'نام کاربری خود را وارد کنید'
        }),
        error_messages={
            'required': 'لطفاً نام کاربری را وارد کنید',
            'unique': 'این نام کاربری قبلاً ثبت شده است',
            'invalid': 'نام کاربری فقط میتواند شامل حروف، اعداد و @/./+/-/_ باشد'
        },
        help_text="""
        حداقل 4 کاراکتر، فقط حروف، اعداد و @/./+/-/_ مجاز هستند
        """
    )
    password1 = forms.CharField(
        label="رمز عبور",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور خود را وارد کنید'
        }),
        error_messages={
            'required': 'لطفاً رمز عبور را وارد کنید',
            'password_too_short': 'رمز عبور باید حداقل ۸ کاراکتر داشته باشد',
            'password_too_common': 'رمز عبور بسیار ساده است',
            'password_entirely_numeric': 'رمز عبور نمی‌تواند فقط عدد باشد'
        },
        help_text=mark_safe("""
        <div class="password-help-text">
            <span> رمز عبور باید حداقل 8 کاراکتر داشته باشد</span>
            <span> نباید شبیه اطلاعات شخصی شما باشد</span>
            <span> نباید از پسوردهای رایج استفاده کنید</span>
            <span> باید شامل حروف و اعداد باشد</span>
        </div>
        """)
    )
    
    password2 = forms.CharField(
        label="تکرار رمز عبور",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور خود را مجدداً وارد کنید'
        }),
        error_messages={
            'required': 'لطفاً تکرار رمز عبور را وارد کنید',
            'password_mismatch': 'رمزهای عبور وارد شده یکسان نیستند'
        }
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
        
        error_messages = {
            'email': {
                'required': 'لطفاً ایمیل را وارد کنید',
                'invalid': 'ایمیل وارد شده معتبر نیست',
                'unique': 'این ایمیل قبلاً ثبت شده است'
            }
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("این ایمیل قبلاً استفاده شده است.")
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise ValidationError("این نام کاربری قبلاً استفاده شده است")
        if len(username) < 4:
            raise ValidationError("نام کاربری باید حداقل 4 کاراکتر باشد")
        return username

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_messages = {
            'password_mismatch': 'رمزهای عبور مطابقت ندارند',
        }
        

class MyPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ["old_password", "new_password1", "new_password2"]:
            self.fields[field_name].widget = forms.PasswordInput()


class MessagingForm(forms.ModelForm):
    class Meta:
        model = MessagingModel
        fields = ["name", "email", "phone_number", "message"] 
        labels = {
            "name": "نام",
            "email": "ایمیل",
            "phone_number": "شماره تماس",
            "message": "پیام شما"
        }

class ConsultingForm(forms.ModelForm):
    class Meta:
        model = ConsultingModel
        fields = ["name", "email", "phone_number"]
        labels = {
            "name": "نام",
            "email": "ایمیل",
            "phone_number": "شماره تماس",
        }


class CustomPasswordResetForm(PasswordResetForm):
    def send_mail(self, subject_template_name, email_template_name, 
                 context, from_email, to_email, html_email_template_name=None):
        
        subject = f"بازنشانی رمز عبور - {context.get('site_name')}"
        body = render_to_string(email_template_name, context)
        
        email = EmailMessage(
            subject,
            body,
            from_email,
            [to_email]
        )
        
        if html_email_template_name:
            html_email = render_to_string(html_email_template_name, context)
            email.content_subtype = "html"
            email.body = html_email
        
        email.send()
  
      
class ProfileForm(forms.ModelForm):
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
        if self.user and method:
            self.user.two_factor_method = method
            if method == 'sms':
                self.user.phone_number = cleaned_data.get('phone_number')
            self.user.save()
        
        return cleaned_data
