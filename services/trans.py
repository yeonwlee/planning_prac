from pydub import AudioSegment

# m4a 파일을 불러오기
audio = AudioSegment.from_file("test.m4a", format="m4a")

# wav 파일로 변환하여 저장
audio.export("output6.wav", format="wav")

print("변환이 완료되었습니다!")