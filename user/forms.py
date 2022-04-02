import datetime

from allauth.account.forms import PasswordField, SignupForm
from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Fieldset, Layout, Submit
from django import forms
from django.forms import RadioSelect

from .models import User, UserProfile


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.helper = FormHelper()
        # self.helper.layout = Layout(
        #     FloatingField('gender', 'birth_day', 'height', 'weight', 'bio', 'public'),
        # )
        for fieldname, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})

    class Meta:
        model = UserProfile
        fields = ["image", "gender", "birth_day", "height", "weight", "bio", "public"]
        junior_min = (datetime.datetime.today() - datetime.timedelta(days=(365 * 15))).strftime(
            "%Y-%m-%d"
        )  # 15세 이상만 가입

        labels = {
            "image": "프로필 이미지",
            "gender": "성별",
            "birth_day": "생일",
            "height": "키 (cm)",
            "weight": "몸무게 (kg)",
            "bio": "자기소개",
            "public": "계정 공개",
        }
        widgets = {
            "birth_day": forms.DateInput(
                attrs={
                    "type": "date",
                    "id": "b_datepicker",
                    "class": "form-floating",
                    "min": "1900-01-01",
                    "value": "2000-01-01",
                    "max": junior_min,
                }
            ),
            "height": forms.NumberInput(attrs={"min": 50, "max": 230}),
            "weight": forms.NumberInput(attrs={"min": 20, "max": 300}),
            "public": forms.RadioSelect(),
        }


class MyCustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(MyCustomSignupForm, self).__init__(*args, **kwargs)
        self.fields["username"].label = "별명"
        for fieldname, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})
        # self.fields['username'].widget.attrs.update(
        #     {'class': 'form-control', 'placeholder': '유저명'})
        # self.fields['email'].widget.attrs.update(
        #     {'class': 'form-control', 'placeholder': 'example@email.com'})
        # self.fields['password1'].widget.attrs.update(
        #     {'class': 'form-control', 'placeholder': '******'})
        # self.fields['password2'].widget.attrs.update(
        #     {'class': 'form-control', 'placeholder': '******'})

    def save(self, request):
        user = super(MyCustomSignupForm, self).save(request)
        user.save()
        return user


# class UserUpdateForm(forms.ModelForm):
#
#     class Meta:
#         model = User
#         fields = ['image']
#
#     labels = {
#         "image": "이미지",
#     }
