import requests


class DictionaryClass:
    def __init__(self):
        self.my_api = "https://api.dictionaryapi.dev/api/v2/entries/en/"
        self.help_data = {
            'word': 'Not Found',
            'audio': '',
            'phonetic': '/not found/',
            'meanings': [
                {
                    'part_name': 'noun',
                    'synonym': 'not found',
                    'definition': 'this word is not in our database'
                }
            ]
        }

    def get_definition(self, word):
        respond = requests.get(url=f"{self.my_api}{word.lower()}")
        try:
            data = respond.json()[0]
            # FIND AUDIO AND PHONETIC - CORRECTLY:
            audio = ""
            phonetic = ""
            for item in data["phonetics"]:
                if ("text" in item.keys()) and ("audio" in item.keys()):
                    phonetic = item["text"]
                    if len(item["audio"]) > len(audio):
                        audio = item["audio"]
                else:
                    pass

            # FIND MEANINGS - CORRECTLY:
            part_of_speech = []
            synonyms = []
            definitions = []
            for my_value in data["meanings"]:
                part_of_speech.append(my_value["partOfSpeech"])
                definitions.append(my_value["definitions"][0]["definition"])
                try:
                    synonyms.append(my_value["synonyms"][0])
                except IndexError:
                    synonyms.append("Not Available")

            # FINAL FACE:
            result = []
            for i in range(len(part_of_speech)):
                result.append({
                    "part_name": part_of_speech[i],
                    "synonym": synonyms[i],
                    "definition": definitions[i]
                })

            answer = {
                "word": data["word"].capitalize(),
                "audio": audio,
                "phonetic": phonetic,
                "meanings": result
            }
            return answer
        except KeyError:
            return self.help_data
