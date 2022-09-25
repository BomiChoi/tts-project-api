from rest_framework.generics import CreateAPIView, DestroyAPIView

from apps.project.models import Project
from .serializers import ProjectCreateSerializer, ProjectSerializer


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
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
