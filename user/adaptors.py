# from allauth.account.adapter import DefaultAccountAdapter
# from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
#
#
# class AccountAdapter(DefaultAccountAdapter):
#     def save_user(self, request, user, form, commit=False):
#         data = form.cleaned_data
#         user.email = data['email']
#         user.first_name = data['first_name']
#         user.last_name = data['last_name']
#         user.FavouriteTeam = data['fav_team']
#         if 'password1' in data:
#             user.set_password(data['password1'])
#         else:
#             user.set_unusable_password()
#         self.populate_username(request, user)
#         user.save()
#         return user
#
#
# class MySocialAccountAdapter(DefaultSocialAccountAdapter):
#
#     def pre_social_login(self, request, sociallogin):
#         """
#         Tasks we're trying to do
#         1. social account already exists, return
#         2. social account has no email, return
#         3. link auth user account to social account
#         """
#         # 1. social account already exists
#         if sociallogin.is_existing:
#             return
#
#         # 2. social account has no email or email is unknown, return
#         if 'email' not in sociallogin.account.extra_data:
#             messages.error(request, 'email is not provided')
#             raise ImmediateHttpResponse(redirect('/accounts/login'))
#
#         # 3. link auth user account to social account
#         try:
#             email = sociallogin.account.extra_data['email']
#             user = User.objects.get(email__iexact=email)
#             sociallogin.connect(request, user)  # linking account
#             user.set_password(None)  # optional, so user can't login with password
#             user.save()
#             return
#
#             # OR you can also Raise Error
#             # messages.error(request, 'user already exit with %s email' % email)
#             # raise ImmediateHttpResponse(redirect('/accounts/login'))
#         except User.DoesNotExist:
#             # if user not found then let allauth to create a new user
#             return