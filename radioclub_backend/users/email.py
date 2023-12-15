from djoser import email


class CustomActivationEmail(email.ActivationEmail):
    """Class for creating custom e-mail. For Djoser."""
    template_name = 'users/activation-email.html'
