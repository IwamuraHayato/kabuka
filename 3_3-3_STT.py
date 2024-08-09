import streamlit as st
import speech_recognition as sr

set_language_list = {
    "日本語" :"ja",
    "英語" :"en-US",
}


# デフォルトの言語を設定
set_language = "日本語"

#アップロード入力
def file_speech_to_text(audio_file):
    # 音声ファイルを読み込み
    with sr.AudioFile(audio_file) as source:
        audio = sr.Recognizer().record(source) # sr.Recognizer().record(開いた音声ファイル)で認識準備

    try:
        text = sr.Recognizer().recognize_google(audio, language="ja") #  sr.Recognizer().recognize_google(音声データ,言語)で音声認識して、textに代入
    except:
        text = "音声認識に失敗しました"
    return text 


#マイク入力
def mic_speech_to_text():

    # マイク入力を音声ファイルとして読み込み
    with sr.Microphone() as source:
        audio = sr.Recognizer().listen(source) # sr.Recognizer().listen(マイク入力)で認識準備

    try:
        text = sr.Recognizer().recognize_google(audio, language="ja") #  sr.Recognizer().recognize_google(音声データ,言語)で音声認識して、textに代入
    except:
        text = "音声認識に失敗しました"
    return text # 認識した文字を返す

st.title("文字起こしアプリ") # タイトル
st.write("音声認識する言語を選んでください。") # 案内を表示
set_language = st.selectbox("音声認識する言語を選んでください。",set_language_list.keys())
current_language_state = st.empty() # 選択肢を表示するための箱を準備
current_language_state.write("選択中の言語:" + set_language) # 選択肢を表示するための箱に選択した言語を表示
file_upload = st.file_uploader("ここにアップロードしてください")

if (file_upload != None):
    st.write("音声認識結果:") # 案内表示
    result_text = file_speech_to_text(file_upload) # アップロードされたファイルと選択した言語を元に音声認識開始
    st.write(result_text) # メソッドから返ってきた値を表示
    st.audio(file_upload) # アップロードした音声をきける形で表示


if st.button("音声認識開始"):
    result_text = mic_speech_to_text() # 選択した言語を元に音声認識開始
    st.write("音声認識結果:") # 案内表示に変更
    st.write(result_text) # メソッドから返ってきた値を表示
