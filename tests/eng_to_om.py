from googletrans import Translator
translator = Translator()

translation = translator.translate("hi" ,'om')
print(translation.text)