
import sys
import os 
currentDir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, currentDir + "\sound_convert")
print(os.path.dirname(os.path.abspath(__file__)))
from vector_word import WordToVectorConvert
from neural_network import NeuNet
from pprint import pprint
from PyQt5 import QtWidgets, QtCore, QtGui, uic
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
import pyqtgraph as pg
from math import log10
import re

class MainWindow(QtWidgets.QMainWindow):
    
    openFile = None
    plot = None
    neu_net = NeuNet()
    rootDir = os.path.dirname(os.path.abspath(__file__))
    allClassesSet = set()
    

    def __init__(self):
        super().__init__()
        QtWidgets.QMainWindow.__init__(self)
   
        self.ui = uic.loadUi(self.rootDir + '\design.ui', self)
        pg.setConfigOption('background', 'w')

        self.plot = pg.PlotWidget()
        self.plot.showGrid(True, True)
        self.gridLayout.addWidget(self.plot, 0, 0)

        self.btnAddWordElement.clicked.connect(self.addWord)
        self.btnRemoveSelectRowStress.clicked.connect(self.removeRowStress)
        self.btnRemoveSelectRowClasses.clicked.connect(self.removeRowClasses)

        self.btnSaveChangeDataSet.clicked.connect(self.saveCsv)
        self.btnTrainingNetwork.clicked.connect(self.trainingNetwork)
        self.btnTestingNetworkOnDataSet.clicked.connect(self.testingNetworkOnDataset)
        self.btnTestingNetworkOnWord.clicked.connect(self.testingNetworkOnWord)

    
    def addWord(self):
        """
        Метод выделения слова, его ударений и классов для дальнейшего добавления таблицы
        """
        try:
            word = self.tbxInsertWord.text().replace("'",'')
            stresses = list(elem.start() - 1 for elem in re.finditer("'", self.tbxInsertWord.text()))
            #stresses = self.txbInsertStress.text().split(',')
            classes = self.txbInsertClasses.text().split(',')

            # print(str(word) + " " + str(stresses) + " " + str(classes))
            if word != "" and len(stresses) > 0 and len(classes) > 0:
                self.addDataInTable(self.twWordsStress, word, stresses)
                self.addDataInTable(self.twWordsClasses, word, classes)
                # если появился новый класс, то добавить его в список
                for elem in classes:
                    self.allClassesSet.add(elem)
                    print(self.allClassesSet)
            else:
                raise ValueError("Невозможно выполнить добавление!\nНе введено слово или классы или не указаны ударения в слове.")
        except Exception as identifier:
            QMessageBox.question(self, 
                                'Warning!', 
                                str(identifier), 
                                QMessageBox.Ok)

    def addDataInTable(self, table, word, data):
        """
        Метод добавления введенного слова в таблицы, отражающие датасеты
        """
        pass
        currentRowCount = table.rowCount()
        table.insertRow(currentRowCount)
        table.setItem(currentRowCount, 0, QTableWidgetItem(str(word)))
        for j, elem in enumerate(data):
            currentColumnCount = table.columnCount()
            if currentColumnCount - 1 < len(data):
                table.insertColumn(currentColumnCount)
            table.setItem(currentRowCount, j + 1, QTableWidgetItem(str(elem)))
        

    def removeRowStress(self):
        """
        Метод удаления выбранной строки из таблицы, содержащей слова и их ударения
        """
        try:
            self.twWordsStress.removeRow(self.twWordsStress.currentRow())
        except Exception as identifier:
            QMessageBox.question(self, 
                                'Warning!', 
                                str(identifier), 
                                QMessageBox.Ok)

    def removeRowClasses(self):
        """
        Метод удаления выбранной строки из таблицы, содержащей слова и их классы
        """
        try:
            self.twWordsClasses.removeRow(self.twWordsClasses.currentRow())
        except Exception as identifier:
            QMessageBox.question(self, 
                                'Warning!', 
                                str(identifier), 
                                QMessageBox.Ok)
    
    def saveCsv(self):
        """
        Метод подготовки данных для сохранения изменений в датасетах, связанных со словами, их ударениями и классами
        """
        try:
            stress_file = open(self.rootDir + '/data_sets/stress_words_res.csv', 'w', encoding='utf-8') 
            classes_file = open(self.rootDir + '/data_sets/classes_words_res.csv', 'w', encoding='utf-8') 
            
            # Запись в начало датасета слов и их классов строки, содержащей все имеющиеся классы
            all_classes_str = ""
            for i, elem in enumerate(self.allClassesSet):
                if i == 0:
                    all_classes_str += elem
                else:
                    all_classes_str += "," + elem
            print(all_classes_str)
            classes_file.write(all_classes_str + "\n")
            
            self.saveCsvStressClasses(stress_file, self.twWordsStress)
            self.saveCsvStressClasses(classes_file, self.twWordsClasses)
        except Exception as identifier:
            QMessageBox.question(self, 
                                'Warning!', 
                                str(identifier), 
                                QMessageBox.Ok)

    def saveCsvStressClasses(self, file, table):
        """
        Метод сохранения изменений в датасетах, связанных со словами, их ударениями и классами
        """
        pass
        row_count = table.rowCount()
        column_count = table.columnCount()
        for row in range(row_count):
            res_str = ""
            for col in range(column_count):
                elem = table.item(row,col)
                if elem and elem.text() != "":
                    if col == 0:
                        res_str += elem.text()
                    else:
                        res_str += "," + elem.text()
            file.write(res_str + "\n")
        file.close()

    def loadDataSet(self):
        """
        Метод открытия файлов, связаднных с датасетами
        """
        try:
            words_stress_file = open(self.rootDir + '/data_sets/stress_words_res.csv', encoding='utf-8') 
            word_classes_file = open(self.rootDir + '/data_sets/classes_words_res.csv', encoding='utf-8') 
            line = word_classes_file.readline()
            for elem in line.split(','):
                self.allClassesSet.add(elem.rstrip())
            print(self.allClassesSet)
            self.openCsv(words_stress_file, self.twWordsStress)
            self.openCsv(word_classes_file, self.twWordsClasses)  
            words_stress_file.close()
            word_classes_file.close()
        except IOError as openFileErr:
            QMessageBox.question(self, 
                                'Warning!', 
                                "Не существует файла: " + str(openFileErr.filename), 
                                QMessageBox.Ok)
        except Exception as identifier:
            QMessageBox.question(self, 
                                'Warning!', 
                                str(identifier), 
                                QMessageBox.Ok)
    
    def openCsv(self, file, table):
        """
        Метод чтения данных из датасетов и их отображения в соответсвующих таблицах
        """
        data_file = file.readlines()
        for i, elem in enumerate(data_file):   
            currentRowCount = table.rowCount()
            table.insertRow(currentRowCount)
            data_line = elem.split(",")
            for j, item in enumerate(data_line):
                currentColumnCount = table.columnCount()
                if currentColumnCount < len(data_line):
                    table.insertColumn(currentColumnCount)
                #print(str(i) + " " + str(j))
                table.setItem(i, j, QTableWidgetItem(str(item.rstrip())))
                #print(item.rstrip())


    def trainingNetwork(self):
        """
        Метод обучения нейронной сети
        """
        try:
            # self.statusbar.showMessage("Идет обучение ...")
            number_epoch = self.txbNumberEpoch.value()
            #if type(number_epoch):
            converter = WordToVectorConvert()
            words_classes_vector_list = converter.ConvertWordsInVector(
                self.rootDir + "/data_sets/sound_letters_frequency.csv", 
                self.rootDir + "/data_sets/sound_letters_significance.csv",
                self.rootDir + "/data_sets/classes_words_res.csv",
                self.rootDir + "/data_sets/stress_words_res.csv")
            #self.neu_net = NeuNet()
            self.plot = pg.PlotWidget()
            self.plot.showGrid(True, True)
            self.gridLayout.addWidget(self.plot, 0, 0)

            res_training = self.neu_net.trainingNetwork(words_classes_vector_list, number_epoch)
            self.plot.addLegend()
            # self.plot.plot(x = None, y = list(log10(x) for x in res_training[0]), pen = 'r', name='Ошибка обучения')
            # self.plot.plot(x = None, y = list(log10(x) for x in res_training[1]), pen = 'b', name='Ошибка проверки')
            self.plot.plot(x = None, y = res_training[0], pen = 'r', name='Ошибка обучения')
            self.plot.plot(x = None, y = res_training[1], pen = 'b', name='Ошибка проверки')
            # self.statusbar.showMessage("Обучение завершено ...")
            # self.plot.plot(x = None, y = res_training[0], pen = 'r', symbol='x', symbolPen='r', symbolBrush=0.05, name='Ошибка обучения')
        except Exception as identifier:
            QMessageBox.question(self, 
                                'Warning!', 
                                str(identifier), 
                                QMessageBox.Ok)
       
    def testingNetworkOnDataset(self):
        """
        Метод тестирования нейронной сети на наборе данных
        """
        try:
            res_test = self.neu_net.testingNetworkOnDataset()
            self.showResTestNetwork(res_test)
        except Exception as identifier:
            QMessageBox.question(self, 
                                'Warning!', 
                                str(identifier), 
                                QMessageBox.Ok)

    def testingNetworkOnWord(self):
        """
        Метод тестирования нейронной сети введенного списка слов
        """
        try:
            words = self.txbTestingWord.text().split(',')
            res_test = set()
            for i, data in enumerate(words):
                word = data.replace("'",'')
                stress = list(elem.start() - 1 for elem in re.finditer("'", data))
                #print(str(word) + " " + str(stress))
                if word == "" and len(stress) <= 0:
                    raise ValueError("Невозможно протестировать!\nНе введено слово или не указаны ударения в слове.")
                converter = WordToVectorConvert()
                word_vector = converter.ConvertWordInVector(
                    self.rootDir + "/data_sets/sound_letters_frequency.csv", 
                    self.rootDir + "/data_sets/sound_letters_significance.csv",
                    word,
                    stress)
                if i == 0:
                    res_test = self.neu_net.testingNetworkOnWord(word_vector[0], word_vector[2])
                else:
                    res_test[1].append(self.neu_net.testingNetworkOnWord(word_vector[0], word_vector[2])[1][0])
               
                    
            self.showResTestNetwork(res_test)
                
        except Exception as identifier:
            QMessageBox.question(self, 
                                'Warning!', 
                                str(identifier), 
                                QMessageBox.Ok)

    def showResTestNetwork(self, res_test):
        """
        Метод отображения результатов тестирования нейронной сети
        """
        self.twResTesting.setRowCount(len(res_test[1]))
        self.twResTesting.setColumnCount(3)
        for i, elem in enumerate(res_test[1]):
            for j, item in enumerate(elem):
                #print(str(i) + " " + str(j) + " " + str(item))
                if j == 0:
                    self.twResTesting.setItem(i, j, QTableWidgetItem(str(item)))
                if j == 1:
                    item_list = list(item)
                    index_max_elem = item_list.index(max(item_list))
                    self.twResTesting.setItem(i, j, QTableWidgetItem(str(res_test[0][index_max_elem])))
                    self.twResTesting.setItem(i, j + 1, QTableWidgetItem(str(item)))
   
def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = MainWindow()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    window.loadDataSet()
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()


