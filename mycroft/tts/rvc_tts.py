from .tts import TTS, TTSValidator
from mycroft.configuration import Configuration
import requests


config_key = "rvc"


class RvcTTS(TTS):
    def __init__(self, lang, config):
        super(RvcTTS, self).__init__(lang, config, RvcTTSValidator(self))
        self.type = "wav"

        self.config = Configuration.get().get("tts", {}).get(config_key, {})
        self.url = self.config.get("url") + "/tts"
        self.rvc_request_body = self.config.get("body")

    def post_rvc_request_for_tts(self, sentence):
        body = self.rvc_request_body
        body["tts_text"] = sentence
        response = requests.post(self.url, json=body, stream=True)
        # might not work and might need to
        # use response.iter_content and chunk
        # https://requests.readthedocs.io/en/latest/user/quickstart/#raw-response-content
        return response.raw

    def get_tts(self, sentence, wav_file):
        output = self.post_rvc_request_for_tts(sentence)
        with open(wav_file, "wb") as f:
            f.write(output)
        return (wav_file, None)  # No phonemes


class RvcTTSValidator(TTSValidator):
    def __init__(self, tts):
        super(RvcTTSValidator, self).__init__(tts)

    def validate_dependencies(self):
        self.config = Configuration.get().get("tts", {}).get(config_key, {})
        if not self.config or not self.config.get("body"):
            raise Exception(
                "RVC is not configured "
                "Need to specify rvc-tts API location and"
                "rvc queries in the form of"
                "rvc_model_name: str"
                "speed: int"
                "tts_text: str"
                "tts_voice: str"
                "f0_key_up: int"
                "f0_method: str"
                "index_rate: int"
                "protect0: float"
            )

    def validate_lang(self):
        # TODO
        pass

    def validate_connection(self):
        # TODO
        pass

    def get_tts_class(self):
        return RvcTTS
