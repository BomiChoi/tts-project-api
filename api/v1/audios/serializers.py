from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.v1.utils import preprocess_sentence
from apps.audio.models import Audio
from apps.project.models import Project


class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        fields = (
            'id',
            'audio_id',
            'text',
            'speed',
            'updated_time',
        )


class AudioCreateSerializer(serializers.ModelSerializer):
    audio_id = serializers.IntegerField(allow_null=True, required=False)

    class Meta:
        model = Audio
        fields = (
            'audio_id',
            'text',
        )

    def validate(self, attrs):
        # 현재 프로젝트의 오디오 목록 불러오기
        current_user = self.context['request'].user
        pk = self.context.get('view').kwargs['pk']
        project = get_object_or_404(Project, user=current_user, id=pk)
        attrs['project'] = project
        audios = Audio.objects.filter(project=project).order_by('audio_id')

        # 아이디가 없거나 유효 범위를 벗어날 경우 마지막 아이디로 설정
        id = attrs.get('audio_id', None)
        if not id or id <= 0 or id > len(audios) + 1:
            attrs['audio_id'] = len(audios) + 1

        # 텍스트 전처리
        attrs['text'] = preprocess_sentence(attrs['text'])
        if len(attrs['text']) == 0:
            raise ValidationError({'text', '빈 문장입니다.'})

        return attrs

    @transaction.atomic()
    def create(self, validated_data):
        # 뒤에 있는 아이디 1씩 증가
        audios = Audio.objects.filter(
            project=validated_data['project'],
            audio_id__gte=validated_data['audio_id']
        ).order_by('-audio_id')
        for audio in audios:
            audio.audio_id += 1
            audio.save()

        # 오디오 생성
        return Audio.objects.create(**validated_data)
