from django import forms
from .models import User, UserProfile


class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['nickname']

    def signup(self, request, user):
        user.nickname = self.cleaned_data['nickname']  # form에 기입된 데이터를 가져오기 위해 cleaned_data 사용
        user.save()


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        # exclude = ['user', 'req_cal','bmi', 'created_at', 'updated_at']
        fields = ['birth_day', 'height', 'weight', 'bio']
