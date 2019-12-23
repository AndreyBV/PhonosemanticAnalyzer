import sys
sys.path.insert(0, "e:/Files/University/Project/CourseWorkPython/sound_convert")
from pybrain3.tools.shortcuts import buildNetwork
from pybrain3.datasets import ClassificationDataSet, SupervisedDataSet
from pybrain3.structure import TanhLayer, SoftmaxLayer, LinearLayer
from pybrain3.supervised.trainers import BackpropTrainer
from vector import WordToVectorConvert

"""
from pprint import pprint
import matplotlib.pyplot as plt
from extractor import SoundLetterExtractor
import pandas as pd
"""

class NeuNet:
    """
    Модуль для обучения нейронной сети.
    """
    net = None
    words_classes_vector_list = list()

    #nortage = None
    #nortrain = None
    #trainer = None

    
    def trainingNetwork(self, words_classes_vector_list, number_epoch = 1000):
        """
        Метод преобразования слова в векторную форму.
        """
        self.words_classes_vector_list = words_classes_vector_list

        # Параметры нейронной сети
        num_input_neuron = 25
        num_output_neuron = len(words_classes_vector_list[0])
        num_hidden_neuron = int((num_input_neuron + num_output_neuron) * 2/3)

        #print("\n Основные параметры нейронной сети:")
        #print(str(num_input_neuron) + " " + str(num_output_neuron) + " " + str(num_hidden_neuron))

        _bias = False
        _hiddenclass = SoftmaxLayer
        _outclass = LinearLayer
        _nb_classes = num_output_neuron
        num_epoch = number_epoch
       
        # Создание нейронной сети и датасетов
        self.net = buildNetwork(num_input_neuron,num_hidden_neuron,num_output_neuron, bias = _bias, hiddenclass = _hiddenclass, outclass = _outclass)
        norgate = ClassificationDataSet(num_input_neuron, num_output_neuron, nb_classes=_nb_classes)
        nortrain = ClassificationDataSet(num_input_neuron, num_output_neuron, nb_classes=_nb_classes)
 
        # Заполнение нейронной сети
        #print("\n Данные для обучения: ")
        for elem in words_classes_vector_list[1]:
            word = elem[0]
            _class = elem[1]
            
            #print(str(elem[2]) + "  " + str(elem[0]) + "  " + str(_class))
            norgate.addSample(tuple(word), tuple(_class))
            nortrain.addSample(tuple(word), tuple(_class))
       
        # Обучение нейронной сети
        trainer = BackpropTrainer(self.net, norgate) # , verbose=True, batchlearning=False, momentum= 0.1, learningrate= 0.01, weightdecay= 0.01, lrdecay=1.0
        trnerr,valerr = trainer.trainUntilConvergence(dataset=nortrain,maxEpochs=num_epoch, verbose=False)
      
        return (trnerr, valerr)

        """
        plt.plot(trnerr,'b', valerr,'r')
        plt.ylabel('$Ошибка$')
        plt.xlabel('$Эпоха$')
        plt.grid()
        plt.show()
        """

        #print(net.activate(tuple(words_classes_vector_list[1][0][0])))
        #print(net.activateOnDataset(norgate))

        # for epoch in range(num_epoch):
        # res = trainer.trainEpochs(num_epoch)
        # trainer.testOnData(dataset=nortrain, verbose=True)

    def testingNetworkOnDataset(self):
        """
        Метод тестирования нейронной сети на наборе данных
        """
        if len(self.words_classes_vector_list) <= 0:
            raise ValueError("Невозможно протестировать необученную нейронную сеть!\nСперва выполните обучение нейронной сети.")
        res_list = list()
        # res_test = self.net.activateOnDataset(self.nortage)
        #print("\n Данные для тестирования: ")
        for elem in self.words_classes_vector_list[1]:
            word_vector = elem[0]
            word = elem[2]
            print(str(word) + " " + str(word_vector))
            res_test = self.net.activate(tuple(word_vector))
            res_list.append((word, res_test))
            #print("Результат теста: ")
            #print(res_test)
        return (self.words_classes_vector_list[0], res_list)
    
    def testingNetworkOnWord(self, word, word_vector):
        """
        Метод тестирования на базе одного слова
        """
        pass
        #print("\n Данные для тестирования: ")
        if len(self.words_classes_vector_list) <= 0:
            raise ValueError("Невозможно протестировать необученную нейронную сеть!\nСперва выполните обучение нейронной сети.")
        print(str(word) + " " + str(word_vector))
        res_list = list()
        res_test = self.net.activate(tuple(word_vector))
        res_list.append((word, res_test))
        #print("Результат теста: ")
        #print(res_test)
        return (self.words_classes_vector_list[0], res_list)
        # net.activate(tuple(words_classes_vector_list[1][0][0]))
        

def main():
    pass
    converter = WordToVectorConvert()
    words_classes_vector_list = converter.ConvertWordsInVector(
        "e:/Files/University/Project/CourseWorkPython/data_sets/sound_letters_frequency.csv", 
        "e:/Files/University/Project/CourseWorkPython/data_sets/sound_letters_significance.csv",
        "e:/Files/University/Project/CourseWorkPython/data_sets/classes_words_res.csv",
        "e:/Files/University/Project/CourseWorkPython/data_sets/stress_words_res.csv")
    #for t in words_vector_dict.values():
    #    print(str(t[0]) + " ---- " + str(t[1]))
    neu_net = NeuNet()
    neu_net.trainingNetwork(words_classes_vector_list, 100000)
    neu_net.testingNetworkOnDataset()


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()
