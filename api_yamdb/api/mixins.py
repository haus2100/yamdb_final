from rest_framework.viewsets import GenericViewSet, mixins


class CreateListDeleteMixinSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
        GenericViewSet):
    pass
