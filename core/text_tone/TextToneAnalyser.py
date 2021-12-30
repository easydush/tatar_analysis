from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel
import operator

POSITIVE = 'positive'
NEGATIVE = 'negative'
SKIP = 'skip'
NEUTRAL = 'neutral'
UNKNOWN = 'unknown'


class TextToneAnalyser:
    def __init__(self):
        self._tokenizer = RegexTokenizer()
        self._model = FastTextSocialNetworkModel(tokenizer=self._tokenizer)

    def get_text_tone(self, text):
        """
        :param text: Text should be array [....]
        :return: tone dictionary {'positive': 0, 'negative': 0, 'skip': 0, 'neutral': 0, 'unknown': 0}
        """
        result = self._model.predict(text, k=2).pop()
        # positive negative skip neutral speech unknown
        result_dict = {POSITIVE: 0, NEGATIVE: 0, SKIP: 0, NEUTRAL: 0, UNKNOWN: 0}

        try:
            # positive text
            positive_value = result.get(POSITIVE)
            if positive_value:
                result_dict.update(positive=positive_value)

            # negative text
            negative_value = result.get(NEGATIVE)
            if negative_value:
                result_dict.update(negative=negative_value)

            # cant understand text tone
            skip_value = result.get(SKIP)
            if skip_value:
                result_dict.update(skip=skip_value)

            # text without tone
            neutral_value = result.get(NEUTRAL)
            if neutral_value:
                result_dict.update(neutral=neutral_value)

            # cant understand text
            unknown_value = result.get(UNKNOWN)
            if unknown_value:
                result_dict.update(unknown=unknown_value)

        except KeyError:
            pass

        return result_dict

    def get_max_text_tone(self, result_dict: dict):
        """
        :param result_dict: {'positive': 0, 'negative': 0, 'skip': 0, 'neutral': 0, 'unknown': 0}
        :return: dictionary with max value
        """
        max_tone_key = max(result_dict.items(), key=operator.itemgetter(1))[0]
        return {max_tone_key: result_dict.get(max_tone_key)}

    def get_max_text_tone_type(self, result_dict: dict):
        """
        :param result_dict: {'positive': 0, 'negative': 0, 'skip': 0, 'neutral': 0, 'unknown': 0}
        :return: max key
        """
        max_tone_key = max(result_dict.items(), key=operator.itemgetter(1))[0]
        return max_tone_key
