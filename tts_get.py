#Requirement (pip install): twitch_chat_analyzer, pydub, ffmpeg, gTTS, langdetect

from langdetect import detect
from twitch_chat_analyzer import analyzer
#from gtts import gTTS
from pydub import AudioSegment
from tempfile import NamedTemporaryFile
from google.cloud import texttospeech
import os

def input_handle():
    print("This program generates audio file of tts based on chat log from recorded twitch broadcast")

    id = input("VOD ID: ")
    
    return(id)

def parameter_handle():
    print("No input is considered as 0.")
    print("0 is ignored during processing")
    start = input("Start Time (in milliseconds): ")
    end = input("End Time (in milliseconds): ")

    if start == '':
        start = 0
    else:
        start = int(start)
    if end == '':
        end = 0
    else:
        end = int(end)

    print("Following input is used when generating tts from specific user, if not needed, please leave input empty.")
    name = input("true user ID: ")

    return(start, end, name)

def main():
    vod_id = int(input_handle())

    vod = analyzer.FromVideoId(vod_id).ToDataFrame()

    # All time processing are performed in millisecond scale.
    start_time, end_time, name = parameter_handle()
    current_tape = start_time

    output = AudioSegment.empty()

    timelist = vod['offset']
    namelist = vod['username']
    textlist = vod['text_body']
    noticelist = vod['is_sub_notice']

    size = len(timelist)
    
    client = texttospeech.TextToSpeechClient()
    voice = texttospeech.VoiceSelectionParams(
        language_code="ko-KR",
        name="ko-KR-Standard-A",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    for i in range(size):
        
        t = int(timelist[i]*1000)

        if end_time != 0:
            if t > end_time:
                break

        if t > start_time:
            if namelist[i] == 'Moobot':
                #print('moobot')
                continue
            elif noticelist[i]:
                #print('notice')
                continue
            elif name != '':
                if namelist[i] != name:
                    continue

            #Fill in empty time, if tts backlog is too large, skip this tts.
            if t > current_tape:
                output = output + AudioSegment.silent(duration=t - current_tape)
                current_tape = t
            elif current_tape > (t + 10000):
                continue

            fragment = textlist[i]

            print(t)
            print(fragment)
            
            #language detection.
            # if detect(textlist[i]) == 'kr':
            #    tts = gTTS(textlist[i], lang='kr', tld='co.kr')
            #    tts.write_to_fp(tts_mp3)
            #elif detect(textlist[i]) == 'en':
            #    tts = gTTS(textlist[i], lang='en')
            #    tts.write_to_fp(tts_mp3)
            #elif detect(textlist[i]) == 'jp':
            #    tts = gTTS(textlist[i], lang='jp', tld='co.jp')
            #    tts.write_to_fp(tts_mp3)

            if fragment.startswith('ㅋ'):
                fragment = "크크크"
            elif fragment.startswith('?'):
                fragment = "question mark"
            elif fragment.startswith('^^7'):
                fragment = "carrot carrot seven"
            elif fragment.startswith('!'):
                print(i)
                continue
            #elif len(fragment) <= 1:
                #print(fragment)
            #    continue

            tts_mp3 = NamedTemporaryFile()

            #tts = gTTS(fragment, lang='ko', lang_check=False)
            #tts.write_to_fp(tts_mp3)
            input = texttospeech.SynthesisInput(text=fragment)
            tts_mp3.write(client.synthesize_speech(input=input, voice=voice, audio_config=audio_config).audio_content)

            tts_mp3.seek(0)
            tts_out = AudioSegment.from_file(tts_mp3, format='mp3')

            current_tape = current_tape + len(tts_out)
            output = output + tts_out

            tts_mp3.close()

            

    output.export(os.path.join(r"C:\\", "{}_tts.mp3".format(vod_id)), format="mp3")
    print("Writing has been finished.")


# Initiate if code is directly executed.
if __name__ == '__main__':
    main()
