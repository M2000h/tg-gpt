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


def synthesize(text, export_path):
    model = model_repository.synthesis_model()
    model.voice = 'zahar'
    model.role = 'neutral'
    result = model.synthesize(text, raw_format=False)
    result.export(export_path, 'mp3')


def recognize(audio):
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
    text = "Привет мир, как дела 123?"
    synthesize(text, "test.mp3")
