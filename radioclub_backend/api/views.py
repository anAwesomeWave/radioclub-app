from rest_framework import mixins, viewsets


class ProfileViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet):
    """ Viewset for viewing user's profile.
        Все пользователи смогут видеть эту страницу, а модераторы править
        что-то, админы также смогут назначать модераторов и других адмминов
        и снимать модеров
    """
    pass
