import json

from django.db.models import Q
from django.views.generic import TemplateView
from health_check.views import MainView
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response

from translate.service.models import Translation
from translate.service.paginations import TranslateClientPagination
from translate.service.serializers import (
    LivelinessCheckSerializer,
    ReadinessCheckSerializer,
    TranslationRequestSerializer,
    TranslationSerializer,
    TranslationSerializerV2,
)


class TranslationsAPIView(ListAPIView):
    """
    This view should return a list of translations
    for provided language
    """

    serializer_class = TranslationSerializer
    pagination_class = TranslateClientPagination
    queryset = Translation.objects

    def get(self, request, *args, **kwargs):
        data = {
            "language": kwargs.get("language", None),
            "views": self.request.GET.getlist("views"),
            "occurrences": self.request.GET.getlist("occurrences"),
            "snake_keys": self.request.GET.getlist("snake_keys"),
            "page": self.request.GET.get("page"),
            "page_size": self.request.GET.get("page_size"),
        }

        req_serializer = TranslationRequestSerializer(data=data)

        req_serializer.is_valid(raise_exception=True)
        validated_params = req_serializer.validated_data

        query = Q(language__lang_info=validated_params.get("language").get("code"))

        view_names = validated_params.get("views")
        if view_names:
            query &= Q(key__views__contains=view_names)

        occurrences = validated_params.get("occurrences")
        if occurrences:
            query &= Q(key__occurrences__contains=occurrences)

        snake_keys = validated_params.get("snake_keys")
        if snake_keys:
            query &= Q(key__snake_name__in=snake_keys)

        qs = self.queryset.filter(query).order_by("-modified")
        data = self.paginate_queryset(qs)

        tran_serializer = TranslationSerializer(data, many=True)
        paginated_response = self.get_paginated_response(tran_serializer.data)

        return paginated_response


class TranslationsAPIViewV2(ListAPIView):
    """
    This view should return a list of translations
    for provided language
    """

    serializer_class = TranslationSerializerV2
    pagination_class = TranslateClientPagination
    queryset = Translation.objects

    def get(self, request, *args, **kwargs):

        data = {
            "language": kwargs.get("language", None),
            "views": self.request.GET.getlist("views"),
            "snake_keys": self.request.GET.getlist("snake_keys"),
            "page": self.request.GET.get("page"),
            "page_size": self.request.GET.get("page_size"),
        }

        req_serializer = TranslationRequestSerializer(data=data)

        req_serializer.is_valid(raise_exception=True)
        validated_params = req_serializer.validated_data

        query = Q(language__lang_info=validated_params.get("language").get("code"))

        view_names = [item for item in validated_params.get("views") if item and item.strip() != ""]
        if view_names:
            _query = Q()
            for q_object in view_names:
                _query |= Q(key__views__contains=[q_object])
            query &= _query
            query &= Q(key__views__isnull=False)

        qs = self.queryset.filter(query).order_by("-modified")
        data = self.paginate_queryset(qs)

        tran_serializer = TranslationSerializerV2(data, many=True)
        paginated_response = self.get_paginated_response(tran_serializer.data)

        return paginated_response


class LivelinessCheckView(GenericAPIView):
    """Liveliness check view."""

    serializer_class = LivelinessCheckSerializer

    def get(self, request, *args, **kwargs):
        """Returns liveliness check response."""
        return Response(self.get_serializer().data, status=status.HTTP_200_OK)


class ReadinessCheckView(MainView, GenericAPIView):
    """Readiness check view."""

    serializer_class = ReadinessCheckSerializer

    def get(self, request, *args, **kwargs):
        """Return readiness check response."""
        request.GET = request.GET.copy()
        request.GET["format"] = "json"

        parent = super().get(request, *args, **kwargs)
        data = json.loads(parent.getvalue())

        return Response(self.get_serializer(data).data, status=parent.status_code)


class HomeView(TemplateView):
    template_name = "index.html"
