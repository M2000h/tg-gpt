from environs import Env
from speechkit import model_repository, configure_credentials, creds
from speechkit.stt import AudioProcessingType

env = Env()
env.read_env(".env")
api_token = env.str("YA_TOKEN")

configure_credentials(
    yandex_credentials=creds.YandexCredentials(
        api_key=api_token
    )
)


def synthesize(text: str, export_path: str) -> None:
    """
    Generate audio from text
    :param text: user's text for synthesize
    :type text: str
    :param export_path: export filepath
    :type export_path: str
    """
    model = model_repository.synthesis_model()
    model.voice = 'zahar'
    model.role = 'neutral'
    result = model.synthesize(text, raw_format=False)
    result.export(export_path, 'mp3')


def recognize(audio: str):
    """
    Recognize text from audio
    :param audio: filepath to audiofile
    :type audio: str
    :return: recognized text
    :rtype: str
    """
    model = model_repository.recognition_model()
    model.model = 'general'
    model.language = 'ru-RU'
    model.audio_processing_type = AudioProcessingType.Full

    result = model.transcribe_file(audio)
    text = ""
    for c, res in enumerate(result):
        text += res.normalized_text + " "
    return text


if __name__ == '__main__':
    text1 = "Привет мир, как дела 123?"
    synthesize(text1, "test.mp3")
