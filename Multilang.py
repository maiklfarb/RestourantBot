import json

class TR:
    resources = dict()

    @staticmethod
    def Initialize(resourcePath):
        with open(resourcePath, "r", encoding="UTF-8") as file:
            TR.resources = json.load(file)

    @staticmethod
    def Get(key, default, lang="en"):
        result = TR.GetByKey(key, lang)

        if result is None:
            return default

        return result

    @staticmethod
    def GetByKey(key, lang="en"):
        try:
            res = TR.resources[lang]
            result = res[key]

            return result
        except:
            return None