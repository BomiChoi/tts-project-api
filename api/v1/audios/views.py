from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from apps.audio.models import Audio
from apps.project.models import Project
from .paginations import AudioPagination
from .serializers import AudioSerializer, AudioCreateSerializer, AudioUpdateSerializer


class ProjectAudioListCreateView(ListCreateAPIView):
    """
    해당 프로젝트의 텍스트를 조회하거나 생성합니다.

    GET
    - parameter
        page: 페이지 번호
    - output
        results: 해당 프로젝트의 오디오 리스트

    POST
    - input
        text: 생성할 문장
        project_id: 문장을 생성할 위치 (선택)
    - output
        audio: 생성된 오디오 정보
    """

    pagination_class = AudioPagination
    serializer_class = AudioSerializer

    def get_queryset(self):
        id = self.kwargs['pk']
        project = Project.objects.get(id=id)
        return Audio.objects.filter(project=project).order_by('audio_id')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AudioSerializer
        elif self.request.method == 'POST':
            return AudioCreateSerializer


class ProjectAudioDetailView(RetrieveUpdateDestroyAPIView):
    def get_object(self):
        project = get_object_or_404(Project, id=self.kwargs['pk'])
        return get_object_or_404(Audio, project=project, audio_id=self.kwargs['audio_id'])

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AudioSerializer
        elif self.request.method == 'PUT' or self.request.method == 'PATCH':
            return AudioUpdateSerializer
