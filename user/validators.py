# validators.py
import re
import string
from allauth.account.adapter import DefaultAccountAdapter
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.forms import ValidationError

custom_username_validators = [UnicodeUsernameValidator()]  # ASCIIUsernameValidator에서 변경 for kakao


def contains_special_character(value):
    for char in value:
        if char in string.punctuation:  # string.punctuation로 특수문자 filtering
            return True
    return False


class CustomPasswordValidator:
    def validate(self, password, user=None):
        if (
                # 정규식으로 8자 이상 알파벳 소문자, 대문자, 특수문자 포함하는지 체크
                not re.match(r"^(?=.*[\d])(?=.*[a-zA-Z])(?=.*[@#$!~%^&*])[\w\d@#$!~%^&*]{8,}$", password)
        ):
            raise ValidationError("8자 이상의 영문 대/소문자, 숫자, 특수문자로 조합해주세요.")

    def get_help_text(self):
        return "8자 이상의 영문 대/소문자, 숫자, 특수문자 조합으로 비밀번호를 만들어주세요."


class UsernameMaxAdapter(DefaultAccountAdapter):
    def clean_username(self, username):
        if len(username) > 12:
            raise ValidationError('닉네임이 너무 깁니다. 다시 설정해주세요.')

        # For other default validations.
        return DefaultAccountAdapter.clean_username(self, username)
