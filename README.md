# harupy

harupy는 한국어 조사 선택과 한글 숫자 표현을 위한 작고 의존성 없는 Python 라이브러리입니다.

## 설치

```console
pip install harupy
```

Python 3.9 이상을 지원합니다.

## 조사 선택

`String` 객체의 `josa()`는 마지막 글자의 받침에 맞는 조사를 붙입니다.

```python
from harupy import String

name1 = String('김수한무')
name2 = String('삼천갑자 동방삭')

name1.josa('이')  # '김수한무가'
name2.josa('가')  # '삼천갑자 동방삭이'

String('신세계').josa('이라는') + ' 영화 봤나요?'
# '신세계라는 영화 봤나요?'
```

`으로/로`는 받침 `ㄹ`에 대한 예외도 처리합니다.

```python
String('작심삼일').josa('으로')  # '작심삼일로'
String('작전변경').josa('로')      # '작전변경으로'
```

속성으로 조사를 직접 적는 축약 문법도 사용할 수 있습니다.

```python
String('오솔길').로                   # '오솔길로'
String('호떡').이나 + ' 먹자'      # '호떡이나 먹자'
String('떡볶이').이나 + ' 먹자'    # '떡볶이나 먹자'
```

## 한글 숫자

숫자를 한글로 읽거나, 한글로 적힌 숫자를 정수로 변환합니다.

```python
String(152000).to_hangul()                # '십오만이천'
String('37501600').to_hangul()            # '삼천칠백오십만천육백'
String(1110000).to_hangul(read_one=True)  # '일백일십일만'

String('이천십팔').to_number()              # 2018
String('천이백십일억천백만').to_number()  # 121111000000
String('사천오백만').isnumeric()              # True
```

## 다른 한글 도구

```python
String('하루 Python').hangul_rate()            # 22
String('하루, Python 3!').extract_readable()   # '하루Python3'
String('오솔길').get_last_bachim()          # 'ㄹ'
list(String('하루').normalize())               # ['ᄒ', 'ᅡ', 'ᄅ', 'ᅮ']
```

## 2.0에서 변경된 점

harupy 2.0은 한글 처리에 집중합니다. 이전 버전의 `common`, `decorators`, `network`, `shell` 모듈과 범용 텍스트 유틸리티는 제거했습니다.

`String`은 기존과 같이 `harupy.text`에서도 가져올 수 있지만, 새 코드에서는 다음 형태를 권장합니다.

```python
from harupy import String
```

## 라이선스

Apache License 2.0
