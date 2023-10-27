from djoser import email


class CustomActivationEmail(email.ActivationEmail):
    template_name = 'users/activation-email.html'