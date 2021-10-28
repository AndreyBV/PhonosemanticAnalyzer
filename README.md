# Phonosemantic Analyzer

## Description

In this project, phonosemantics acts as a tool with which it is possible to formalize input data for a neural network, which subsequently must determine an object (class) by a set of phonosemantic features.

Among the main modules of the project are: a data formalization module, i.e. representations of the original word in vector form and theirs, as well as a machine learning module representing a trained neural network, which, as a result, should predict the belonging of an arbitrary object (word) to any class.

## Initialization

1. [Download this repository](https://github.com/AndreyBV/PhonosemanticAnalyzer/archive/refs/heads/master.zip);
1. Install dependency manager **pipenv**:
   `pip install pipenv`
1. Open the console in the project folder;
1. Start the **pipenv** virtual environment by running the command in an open console:
   `pipenv shell`
1. Synchronize the dependencies:
   `pipenv sync`
1. Run the file **MainCW.py**

## How it work

The interface of the developed software, presented in the "Working Example" section, contains a set of necessary controls for editing the initial datasets, displaying neural network training errors on a graph, as well as training and testing the neural network.

- **The "Delete selected item" button** allows you to delete a user-selected row from the corresponding table.
- **The "Add item" button** allows you to add new information to the datasets, which is entered in the "Word" and "Classes" fields located above the button. To successfully add new data, you must fill in both fields, and in the "Word" field you also need to specify the stress using the " ' " symbol (for example: "do'm"), and in the "Classes" field you can list their list separated by commas without spaces (for example: "building, housing").
- **The button "Save changes in the dataset"** allows you to convert the information presented in the corresponding tables into a file in the "\* .csv" format.
- **The "Train network" button** starts the process of training the neural network, selected in the "Number of training epochs" field the number of times. As a result of training the neural network, a graph will be built containing information about training and validation errors.
- **The "Test network" button** allows you to test the ability of the neural network to predict which class the object belongs to, which the user entered in the "Word" field, following the same rule as for adding information to datasets. The test result is provided in the form of a table.
- **The button "Test the network on the original dataset"** allows you to check the ability of the neural network to predict to which class the objects located in the original dataset belong, i.e. there is a check of the conformity of the data that was originally supplied to the network and the data that it produces as a result.

## Work example

<img src="./_documentation/main_window.png?raw=true" alt="Page on mobile"  width=600px height="auto" style="border: 1px solid gray"/>
