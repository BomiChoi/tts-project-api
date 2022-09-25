from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView

from apps.audio.models import Audio
from apps.project.models import Project
from .paginations import AudioPagination
from .serializers import ProjectCreateSerializer, ProjectSerializer, AudioSerializer


class ProjectCreateView(CreateAPIView):
    """
    프로젝트를 생성합니다.
    - input
        text: 텍스트가 담긴 리스트(length = 1)
        title: 프로젝트 제목
    - output
        project: 생성된 프로젝트 정보
    """

    serializer_class = ProjectCreateSerializer


class ProjectDestroyView(DestroyAPIView):
    """ 해당 프로젝트를 삭제합니다. """

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectAudioListView(ListAPIView):
    """ 해당 프로젝트의 텍스트 목록을 조회합니다 """

    serializer_class = AudioSerializer
    pagination_class = AudioPagination

    def get_queryset(self):
        user = self.request.user
        id = self.kwargs['pk']
        project = Project.objects.get(user=user, project_id=id)
        return Audio.objects.filter(project=project).order_by('audio_id')
