from django import forms
from django.forms import DateInput
from .models import User, UserProfile
from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, MultiField
from allauth.account.forms import SignupForm, PasswordField


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['gender', 'birth_day', 'height', 'weight', 'bio']
        # YEARS = [x for x in range(1940, 2021)]

        labels = {
            "gender": "성별",
            "birth_day": "생일",
            "height": "키",
            "weight": "몸무게",
            "bio": "자기소개",
        }
        widgets = {
            "birth_day": forms.DateInput(attrs={'id': 'b_datepicker', 'class': "form-floating"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            FloatingField('gender', 'birth_day', 'height', 'weight', 'bio'),
            ButtonHolder(
                Submit('submit', '업데이트', css_class='btn btn-primary button white')
            )
        )


class MyCustomSignupForm(SignupForm):

    def __init__(self, *args, **kwargs):
        super(MyCustomSignupForm, self).__init__(*args, **kwargs)
        self.fields["username"].label = "별명"
        for fieldname, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control'
            })
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
