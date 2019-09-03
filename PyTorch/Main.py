from __future__ import print_function
from FrontNet import PreActBlock
from FrontNet import FrontNet
from FrontNet import GrayFrontNet

from DataProcessor import DataProcessor
from ModelTrainer import ModelTrainer
from Dataset import Dataset
from torch.utils import data
from ModelManager import ModelManager
import logging
import numpy as np
import sys
sys.path.append("../pulp/")
import pandas as pd



def MergeDatasets():
    DATA_PATH = "/Users/usi/PycharmProjects/data/"

    dataset = pd.read_pickle(DATA_PATH + "train.pickle").values
    dataset2 = pd.read_pickle(DATA_PATH + "Hand2.pickle").values
    x_dataset = dataset[:, 0]
    y_dataset = dataset[:, 1]
    x_dataset2 = dataset2[:, 0]
    y_dataset2 = dataset2[:, 1]
    x_dataset = np.append(x_dataset, x_dataset2)
    y_dataset = np.append(y_dataset, y_dataset2)

    print("dataset ready x:{} y:{}".format(len(x_dataset), len(y_dataset)))
    df = pd.DataFrame(data={'x': x_dataset, 'y': y_dataset})
    print("dataframe ready")
    df.to_pickle("HandHead.pickle")


def Train():
    model = FrontNet(PreActBlock, [1, 1, 1])
    trainer = ModelTrainer(model)

    DATA_PATH = "/Users/usi/PycharmProjects/data/"

    [x_train, x_validation, y_train, y_validation] = DataProcessor.ProcessTrainData(
        DATA_PATH + "HandHead.pickle", 60, 108)

    training_set = Dataset(x_train, y_train, True)
    params = {'batch_size': 64,
              'shuffle': True,
              'num_workers': 0}
    training_generator = data.DataLoader(training_set, **params)

    validation_set = Dataset(x_validation, y_validation)
    validation_generator = data.DataLoader(validation_set, **params)

    trainer.Train(training_generator, validation_generator)



def TrainGray():
    model = GrayFrontNet(PreActBlock, [1, 1, 1])
    trainer = ModelTrainer(model)

    DATA_PATH = "/Users/usi/PycharmProjects/data/"
    [x_train, x_validation, y_train, y_validation] = DataProcessor.ProcessTrainData(
        DATA_PATH + "train_vignette.pickle", 60, 108, True)

    training_set = Dataset(x_train, y_train, True)
    params = {'batch_size': 64,
              'shuffle': True,
              'num_workers': 0}
    training_generator = data.DataLoader(training_set, **params)

    validation_set = Dataset(x_validation, y_validation)
    validation_generator = data.DataLoader(validation_set, **params)

    trainer.Train(training_generator, validation_generator)


def ConvertToGray():
    DATA_PATH = "/Users/usi/PycharmProjects/data/"
    DataProcessor.CreateGreyPickle(DATA_PATH + "train.pickle", 60, 108, "train_vignette.pickle")
    DataProcessor.CreateGreyPickle(DATA_PATH + "test.pickle", 60, 108, "test_vignette.pickle")

def main():
    logging.basicConfig(level=logging.INFO,
                            format="%(asctime)s - %(levelname)s - %(message)s",
                            datefmt="%Y-%m-%d %H:%M:%S",
                            filename="log.txt",
                            filemode='w')


    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    TrainGray()
    #ConvertToGray()
    #MergeDatasets()
    #Train()


if __name__ == '__main__':
    main()