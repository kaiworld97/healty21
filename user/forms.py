from django import forms
from .models import User


class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['nickname', 'nickname2']

    def signup(self, request, user):
        user.nickname = self.cleaned_data['nickname']  # form에 기입된 데이터를 가져오기 위해 cleaned_data 사용
        user.save()

