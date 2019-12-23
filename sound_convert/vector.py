import sys
sys.path.insert(0, "e:/Files/University/Project/CourseWorkPython/sound_convert")
from extractor import SoundLetterExtractor
from analyzer import PhonosemanticAnalyzer
from letter import SoundLetter
from word import SoundWord
from utils import read_csv
from pprint import pprint
import re

class WordToVectorConvert:
    """
    Модуль для конвертирования слова в вектор.
    """

    def GetVector(self, analyzer, word, stress):
        """
        Метод преобразования слова в вектор
        """
        pass
        sound_extraxtor = SoundLetterExtractor() 
        sound_word = sound_extraxtor.extract(word, stress)
        vector = analyzer.analyze_sound_word(sound_word)
        return (sound_word.word, sound_word.sound_word, vector)
    
    def ConvertWordsInVector(self, sound_letters_frequency_file, sound_letters_significance_file, classes_words_file, words_stress_file):
        """
        Метод преобразования слова в векторную форму для набора данных
        :param sound_letters_frequency_file: Таблица частотности звукобукв.
        :param sound_letters_significance_file: Таблица значимости звукобукв.
        :param classes_words_file: Таблица слов и ударений в них.
        :param classes_words_file: Таблица слов и определяющих их классы.
        :return: кортеж (список всех классов, словарь (ключ: звуко-слово, значение: вектор))
        """
        analyzer = PhonosemanticAnalyzer(sound_letters_frequency_file, sound_letters_significance_file)
        classes_words_f = read_csv(classes_words_file) # Получение списка слов и их классов
        stress_words_f = read_csv(words_stress_file) # Получение списка слов и их ударений
        
        # Формирование списка кортежей (слово, звкослово, вектор)
        words_stress_list = list()
        for elem in stress_words_f:
            word = elem[0]
            stress = list(map(int, list(filter(None, elem[1:]))))
            words_stress_list.append(self.GetVector(analyzer, word, stress))
        #pprint(words_stress_list)


        # Список кортежей (вектор слова, список векторов классов, к которым принадлежит слово, само слого, сами классы)
        words_classes_vector_list = list()
   
        # Список всех существующих классов
        all_classes_list = list()
        # Перебор списка слов и их классов
        for i, elem in enumerate(classes_words_f):  
            # Получение списка всех классов
            if i == 0:
                all_classes_list = elem
                continue
            classes_vector = [0] * len(all_classes_list)
            # Получение слова
            word = elem[0]
            # Получение классов которым принадлежит слово
            classes = list(filter(None, elem[1:]))
            # Формирование вектора классов для слова
            for ii, item in enumerate(all_classes_list):
               if item in classes:
                   classes_vector[ii] = 1

            word_vector_res = list()
            # Перебор списка слов и их векторов
            for item in words_stress_list:
                # Получение слова
                word_str = item[0]
                # Получение вектора
                word_vector = item[2]
                if (word_str == word):
                    word_vector_res = word_vector
            words_classes_vector_list.append((word_vector_res, classes_vector, word, classes))
        return (all_classes_list, words_classes_vector_list)

    # Первод слова в вектор
    def ConvertWordInVector(self, sound_letters_frequency_file, sound_letters_significance_file, word, stress):
        """
        Метод преобразования слова в векторную форму.
        :param sound_letters_frequency_file: Таблица частотности звукобукв.
        :param sound_letters_significance_file: Таблица значимости звукобукв.
        :param sound_letters_significance_file: Таблица слов и ударений в них.
        :return: словарь (ключ: звуко-слово, значение: вектор).
        """
        analyzer = PhonosemanticAnalyzer(sound_letters_frequency_file, sound_letters_significance_file)
        word_vector = self.GetVector(analyzer, word, stress)
        return word_vector
    
    #return (sound_word.word, sound_word.sound_word, vector)
    

def main():
    pass
    converter = WordToVectorConvert()
    res = converter.ConvertWordsInVector(
        "e:/Files/University/Project/CourseWorkPython/data_sets/sound_letters_frequency.csv", 
        "e:/Files/University/Project/CourseWorkPython/data_sets/sound_letters_significance.csv",
        "e:/Files/University/Project/CourseWorkPython/data_sets/classes_words_res.csv",
        "e:/Files/University/Project/CourseWorkPython/data_sets/stress_words_res.csv")
    #pprint(res)

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
