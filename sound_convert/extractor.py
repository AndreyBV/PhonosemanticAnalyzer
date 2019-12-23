import sys
sys.path.insert(0, "e:/Files/University/Project/CourseWorkPython/sound_convert")
from word import SoundWord


class SoundLetterExtractor:
    """
    Модуль для извлечения звукобукв русского языка из слова.
    """

    @staticmethod
    def extract(input_word, stresses=None):
        """
        Метод извлечения звуко-слова (набора звуко-букв) из слова.
        :param input_word: Слово.
        :param stresses: Массив индексов ударных букв.
        :return: Звуко-слово.
        """
        input_word = input_word.lower()
        if stresses is None or not isinstance(stresses, list):
            raise ValueError('Ударения не найдены')
        return SoundWord(input_word, stresses)


def main():
    pass
    obj = SoundLetterExtractor()
    res = obj.extract("дом", [1])
    #print(res.__repr__())

if __name__ == '__main__':
    main()