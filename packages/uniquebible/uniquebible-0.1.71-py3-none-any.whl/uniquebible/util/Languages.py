class Languages:

    code = {
        "Chinese (Simplified) 简体中文": "zh_HANS",
        "Chinese (Traditional) 繁體中文": "zh_HANT",
        "English (UK)": "en_GB",
        "English (US)": "en_US",
        "French Français": "fr",
        "German Deutsch": "de",
        "Greek Νέα Ελληνικά": "el",
        "Hindi हिन्दी": "hi",
        "Korean 한국어": "ko",
        "Italian Italiano": "it",
        "Japanese 日本語": "ja",
        "Malayalam മലയാളം": "ml",
        "Romanian Limba Română": "ro",
        "Russian Русский язык": "ru",
        "Spanish Español": "es",
    }

    googleTranslateCodes = {
        "Afrikaans": "af",
        "Albanian": "sq",
        "Amharic": "am",
        "Arabic": "ar",
        "Armenian": "hy",
        "Azerbaijani": "az",
        "Basque": "eu",
        "Belarusian": "be",
        "Bengali": "bn",
        "Bosnian": "bs",
        "Bulgarian": "bg",
        "Catalan": "ca",
        "Cebuano": "ceb",
        "Chinese (Simplied)": "zh-CN",
        "Chinese (Traditional)": "zh-TW",
        "Corsican": "co",
        "Croatian": "hr",
        "Czech": "cs",
        "Danish": "da",
        "Dutch": "nl",
        "English": "en",
        "Esperanto": "eo",
        "Estonian": "et",
        "Finnish": "fi",
        "French": "fr",
        "Frisian": "fy",
        "Galician": "gl",
        "Georgian": "ka",
        "German": "de",
        "Greek": "el",
        "Gujarati": "gu",
        "Haitian Creole": "ht",
        "Hausa": "ha",
        "Hawaiian": "haw",
        "Hebrew": "he",
        "Hindi": "hi",
        "Hmong": "hmn",
        "Hungarian": "hu",
        "Icelandic": "is",
        "Igbo": "ig",
        "Indonesian": "id",
        "Irish": "ga",
        "Italian": "it",
        "Japanese": "ja",
        "Javanese": "jv",
        "Kannada": "kn",
        "Kazakh": "kk",
        "Khmer": "km",
        "Korean": "ko",
        "Kurdish": "ku",
        "Kyrgyz": "ky",
        "Lao": "lo",
        "Latin": "la",
        "Latvian": "lv",
        "Lithuanian": "lt",
        "Luxembourgish": "lb",
        "Macedonian": "mk",
        "Malagasy": "mg",
        "Malay": "ms",
        "Malayalam": "ml",
        "Maltese": "mt",
        "Maori": "mi",
        "Marathi": "mr",
        "Mongolian": "mn",
        "Myanmar (Burmese)": "my",
        "Nepali": "ne",
        "Norwegian": "no",
        "Nyanja (Chichewa)": "ny",
        "Pashto": "ps",
        "Persian": "fa",
        "Polish": "pl",
        "Portuguese (Portugal, Brazil)": "pt",
        "Punjabi": "pa",
        "Romanian": "ro",
        "Russian": "ru",
        "Samoan": "sm",
        "Scots Gaelic": "gd",
        "Serbian": "sr",
        "Sesotho": "st",
        "Shona": "sn",
        "Sindhi": "sd",
        "Sinhala (Sinhalese)": "si",
        "Slovak": "sk",
        "Slovenian": "sl",
        "Somali": "so",
        "Spanish": "es",
        "Sundanese": "su",
        "Swahili": "sw",
        "Swedish": "sv",
        "Tagalog (Filipino)": "tl",
        "Tajik": "tg",
        "Tamil": "ta",
        "Telugu": "te",
        "Thai": "th",
        "Turkish": "tr",
        "Ukrainian": "uk",
        "Urdu": "ur",
        "Uzbek": "uz",
        "Vietnamese": "vi",
        "Welsh": "cy",
        "Xhosa": "xh",
        "Yiddish": "yi",
        "Yoruba": "yo",
        "Zulu": "zu",
    }

    # gtts-cli --all
    gTTSLanguageCodes = {
        "Afrikaans": "af",
        "Arabic": "ar",
        "Bulgarian": "bg",
        "Bengali": "bn",
        "Bosnian": "bs",
        "Catalan": "ca",
        "Czech": "cs",
        "Welsh": "cy",
        "Danish": "da",
        "German": "de",
        "Greek": "el",
        "English": "en",
        "Esperanto": "eo",
        "Spanish": "es",
        "Estonian": "et",
        "Finnish": "fi",
        "French": "fr",
        "Gujarati": "gu",
        "Hebrew": "he",
        "Hindi": "hi",
        "Croatian": "hr",
        "Hungarian": "hu",
        "Armenian": "hy",
        "Indonesian": "id",
        "Icelandic": "is",
        "Italian": "it",
        "Japanese": "ja",
        "Javanese": "jw",
        "Khmer": "km",
        "Kannada": "kn",
        "Korean": "ko",
        "Latin": "la",
        "Latvian": "lv",
        "Macedonian": "mk",
        "Malayalam": "ml",
        "Marathi": "mr",
        "Myanmar (Burmese)": "my",
        "Nepali": "ne",
        "Dutch": "nl",
        "Norwegian": "no",
        "Polish": "pl",
        "Portuguese": "pt",
        "Romanian": "ro",
        "Russian": "ru",
        "Sinhala": "si",
        "Slovak": "sk",
        "Albanian": "sq",
        "Serbian": "sr",
        "Sundanese": "su",
        "Swedish": "sv",
        "Swahili": "sw",
        "Tamil": "ta",
        "Telugu": "te",
        "Thai": "th",
        "Filipino": "tl",
        "Turkish": "tr",
        "Ukrainian": "uk",
        "Urdu": "ur",
        "Vietnamese": "vi",
        "Mandarin": "zh",
    }

    @staticmethod
    def decode(code):
        for key in Languages.code.keys():
            if code == Languages.code[key]:
                return key
        return "Unknown"

if __name__ == '__main__':
    print(Languages.decode("ko"))
