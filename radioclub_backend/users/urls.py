from django.urls import path, include


urlpatterns = (
    path('', include('djoser.urls')),
    # JWT-эндпоинты, для управления JWT-токенами:
    path('', include('djoser.urls.jwt')),
)

'''
djoser
/users/ - просмотреть, создать пользователей
/users/activation/ - активировать usera
/users/resend_activation/ - resend activation
/users/me/ - обновить, удалить инфу
/users/set_password/ - поменять пароль

jwt
/jwt/create/ - создать токен
/jwt/refresh/ - обновить токен
/jwt/verify/ - подтвердить токен
'''
