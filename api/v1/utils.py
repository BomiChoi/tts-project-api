import re

from apps.audio.models import Audio


def preprocess_sentence(s):
    """ 문장 전처리 함수 """
    # 맨 앞, 맨 뒤 공백 제거
    s = s.strip()

    # 한글, 영어, 숫자, 물음표, 느낌표, 마침표, 따옴표, 공백를 제외한 나머지 제거
    s = re.sub('[^ㄱ-ㅎ가-힣a-zA-Z0-9?!.\'\" ]', '', s)

    return s


def preprocess(li):
    """ 텍스트 전처리 함수 """
    res = []

    # 문장부호 기준으로 자르기
    sp = re.split(r'([.!?])', li[0])

    for i in range(len(sp) // 2):
        # 문장 전처리
        s = preprocess_sentence(sp[2 * i])

        # 빈 문장이 아닐 경우 문장부호 다시 붙인 후 저장
        if len(s) > 0:
            res.append(s + sp[2 * i + 1])

    # 마지막 문장에 문장부호가 없는 경우 따로 추가
    if len(sp) % 2 == 1:
        # 문장 전처리
        s = preprocess_sentence(sp[-1])

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
            project=project
        )
        res.append((audio.id, audio.text))

    return res
