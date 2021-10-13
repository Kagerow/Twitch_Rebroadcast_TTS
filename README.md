# Twitch_Rebroadcast_TTS

Twitch Rebroadcast TTS is tool designed to generate audio file containing Text-to-Speech converted chat of Twitch video.

트위치 재방송 TTS 는 트위치 비디오의 채팅 내용을 기반으로 TTS 를 만들기 위한 툴입니다.

## 사용법 (To-Use Instruction)

사용에 앞서 Chocolatey 나 Winget 같은 패키지 매니져를 설치하는것을 권장합니다. 이 두 툴이 있을경우 프로그램 요구 사항을 간편하게 설치 할 수 있습니다.

1. 최신 버젼의 파이선 3.x 를 설치합니다 (https://www.python.org/downloads/ 또는 choco install python) 
2. 파이선이 설치 된 후 관리자 권한으로 실행된 Powershell 에서 "pip install <이름>" 명령어로 이하의 패키지를 깔아주셔야 합니다
3. twitch_chat_analyzer, pydub, ffmpeg
4. 다만 ffmpeg 는 설치후 추가로 프로그램을 설치하셔야 합니다 (https://ffmpeg.org/ 또는 choco install ffmpeg)
5. 구글 클라우드 SDK 를 설치합니다 (https://cloud.google.com/sdk/docs/install)
6. 그 이후 구글 클라우드 무료 계정을 설정해야 합니다. (https://cloud.google.com/text-to-speech#section-12)
7. Powershell 에 credential json 파일을 등록하고 python tts_get.py 로 프로그램을 실행한 후 프로그램에서 필요로 한다고 요청하는 정보를 입력해주시면 됩니다.
