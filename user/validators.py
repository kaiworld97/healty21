# validators.py
import re
import string
from allauth.account.adapter import DefaultAccountAdapter
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.forms import ValidationError

custom_username_validators = [ASCIIUsernameValidator()]


def contains_special_character(value):
    for char in value:
        if char in string.punctuation:  # string.punctuation로 특수문자 filtering
            return True
    return False


class CustomPasswordValidator:
    def validate(self, password, user=None):
        if (
                not re.match(r"^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$!~%^&*])[\w\d@#$!~%^&*]{8,}$", password)
                # len(password) < 8 or
                # not re.findall('[A-Z]', password) or  # not contains_uppercase
                # not re.findall('[a-z]', password) or  # not contains_lowercase
                # not re.findall('[0-9]', password) or  # not contains_number
                # not contains_uppercase_letter(password) or
                # not contains_lowercase_letter(password) or
                # not contains_number(password) or
                # not contains_special_character(password)
        ):
            raise ValidationError("8자 이상의 영문 대/소문자, 숫자, 특수문자로 조합해주세요.")

    def get_help_text(self):
        return "8자 이상의 영문 대/소문자, 숫자, 특수문자 조합으로 비밀번호를 만들어주세요."


class UsernameMaxAdapter(DefaultAccountAdapter):
    def clean_username(self, username):
        if len(username) > 15:
            raise ValidationError('현재 닉네임이 너무 깁니다.')

        # For other default validations.
        return DefaultAccountAdapter.clean_username(self, username)
