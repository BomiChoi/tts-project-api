import re

from django.db import transaction
from rest_framework import serializers

from apps.audio.models import Audio
from apps.project.models import Project


def preprocess(li):
    """ 텍스트 전처리 함수 """
    res = []

    # 문장부호 기준으로 자르기
    sp = re.split(r'([.!?])', li[0])

    for i in range(len(sp) // 2):
        # 맨 앞, 맨 뒤 공백 제거
        s = sp[2 * i].strip()

        # 한글, 영어, 숫자, 물음표, 느낌표, 마침표, 따옴표, 공백를 제외한 나머지 제거
        s = re.sub('[^(ㄱ-ㅎ|가-힣|a-z|A-Z|0-9|?!.\'\" )]', '', s)

        # 빈 문장이 아닐 경우 문장부호 다시 붙인 후 저장
        if len(s) > 0:
            res.append(s + sp[2 * i + 1])

    # 마지막 문장에 문장부호가 없는 경우 따로 추가
    if len(sp) % 2 == 1:
        s = sp[-1].strip()

        # 한글, 영어, 숫자, 물음표, 느낌표, 마침표, 따옴표, 공백를 제외한 나머지 제거
        s = re.sub('[^(ㄱ-ㅎ|가-힣|a-z|A-Z|0-9|?!.\'\" )]', '', s)

        # 빈 문장이 아닐 경우 저장
        if len(s) > 0:
            res.append(s)

    return res


def create_audio(project, li):
    """ 오디오 생성 함수 """
    res = []

    # audio 객체 생성
    for i, txt in enumerate(li):
        audio = Audio.objects.create(
            audio_id=i + 1,
            text=txt,
            speed=1,
            project=project
        )
        res.append((audio.id, audio.text))

    return res


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = (
            'id',
            'project_id',
            'project_title',
            'user',
            'created_time',
            'updated_time',
        )


class ProjectCreateSerializer(serializers.Serializer):
    text = serializers.ListField(
        child=serializers.CharField(),
        max_length=1,
        write_only=True
    )
    title = serializers.CharField(write_only=True)
    project = ProjectSerializer(read_only=True)

    @transaction.atomic()
    def create(self, validated_data):
        # 현재 유저 정보 가져오기
        current_user = self.context['request'].user

        # 새 프로젝트 아이디 값 구하기
        projects = Project.objects.filter(user=current_user).order_by('project_id')
        project_id = 1
        if len(projects) > 0:
            # 현재 유저의 마지막 프로젝트 아이디보다 1 큰 숫자로 설정
            project_id = projects[len(projects) - 1].project_id + 1

        # 프로젝트 생성하기
        project = Project.objects.create(
            project_title=validated_data['title'],
            user=current_user
        )
        project.project_id = project_id
        project.save()

        # 전처리 후 오디오 변환 함수에 넣기
        li = preprocess(validated_data['text'])
        res = create_audio(project, li)

        return project


class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        fields = (
            'id',
            'audio_id',
            'text',
            'speed',
            'project',
            'updated_time',
        )
