from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    pass


account_activation_token = AccountActivationTokenGenerator()


def build_activation_link(request, user):
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)
    path = f"/activate/{uidb64}/{token}/"
    return request.build_absolute_uri(path)