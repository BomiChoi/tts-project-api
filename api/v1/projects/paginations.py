from rest_framework.pagination import PageNumberPagination


class AudioPagination(PageNumberPagination):
    page_size = 10
