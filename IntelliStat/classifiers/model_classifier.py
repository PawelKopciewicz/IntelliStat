from typing import List

import numpy as np
import torch
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split

from IntelliStat.utils.datasets import BaseDataset
from IntelliStat.neural_networks.ENN import ENN
from IntelliStat.utils.components import Component


def model_classifier():
    epoch: int = 80
    train_samples: int = 2000
    test_samples: int = 200
    classes: int = 10
    components: int = 2
    EvolutionalNN = ENN(40, 40, 20, 10, components)

    X_data: List[List[float]] = [[X / 4 for X in range(40)] for _ in range(classes * (train_samples + test_samples))]
    X_data: np.ndarray = np.array(X_data, dtype=np.float32)

    Y_data: np.ndarray = np.zeros((X_data.shape[0], components), dtype=np.float32)

    for c in range(classes):
        for i in range(train_samples + test_samples):
            component = Component[c]
            X_data[i + c * (train_samples + test_samples)] = component.generate_data(
                x=X_data[i + c * (train_samples + test_samples)]
            )
            Y_data[i + c * (train_samples + test_samples)] = component.class_vector

    X_train, X_test, Y_train, Y_test = train_test_split(X_data, Y_data, test_size=0.3)

    Dataset = BaseDataset(X_train, Y_train)
    EvolutionalNN.train(Dataset, epoch, 25)

    X_NN = torch.tensor(X_test)
    Y_NN = EvolutionalNN.model(X_NN)
    Y_NN = Y_NN.detach().numpy()

    idx_gge: List[int] = []
    accuraccy: int = 0

    for i in range(Y_NN.shape[0]):
        if np.array_equal(Y_test[i], Component[3].class_vector):
            idx_gge.append(i)
        if round(Y_NN[i, 0]) == Y_test[i, 0] and round(Y_NN[i][1]) == Y_test[i, 1]:
            accuraccy = accuraccy + 1

    accuraccy = accuraccy / Y_NN.shape[0]
    print("Reached accuraccy: ", accuraccy)

    fig, ax = plt.subplots(2, 2)
    fig.set_size_inches(8, 8)
    n, bins, patches = ax[0, 0].hist(Y_NN[idx_gge, 0], 100, alpha=0.5, range=[0, 3], color='red', label='Gauss')
    n, bins, patches = ax[0, 0].hist(Y_NN[idx_gge, 1], 100, alpha=0.5, range=[0, 3], color='blue', label='Exp')
    # n, bins, patches = ax[0, 0].hist(Y_NN[idx_gge, 2], 100, alpha=0.5, range = [0,1], label='Gauss+Gauss+Gauss')
    # n, bins, patches = ax[0, 0].hist(Y_NN[idx_gge, 3], 100, alpha=0.5, range = [0,1], label='Gauss+Gauss+Exp')
    # n, bins, patches = ax[0, 0].hist(Y_NN[idx_gge, 4], 100, alpha=0.5, range = [0,1], label='Gauss+Exp')
    # n, bins, patches = ax[0, 0].hist(Y_NN[idx_gge, 5], 100, alpha=0.5, range=[0, 1],  label='Exp')
    ax[0, 0].set_xlabel('Class A (Gauss+Gauss+Exp)')
    ax[0, 0].set_ylabel('Number of counts')
    ax[0, 0].legend(loc='upper right')
    ax[0, 0].set_title('Class affiliation probability')

    ax[1, 0].plot(range(0, epoch), EvolutionalNN.loss_vector, 'k-', label="Loss function")
    ax[1, 0].set_xlabel('Epoch number')
    ax[1, 0].set_ylabel('Loss function')
    ax[1, 0].set_yscale('log')
    ax[1, 0].set_ylim([0.0000001, 0.1])
    ax[1, 0].set_xlim([0, 500])

    X_plot = [X / 40 for X in range(400)]
    X_plot = np.array(X_plot, dtype=np.float32)
    X_plot = Component('7G').generate_data(X_plot)
    ax[0, 1].plot(np.linspace(0, 10, 400, endpoint=False), X_plot, 'r-', label="7G(x)")
    ax[0, 1].set_xlabel('X argument')
    # ax[0, 1].set_ylabel('GGE(x)')
    ax[0, 1].legend(loc='upper right')
    ax[0, 1].set_title('Exemplary training 7G(x) curve')
    # ax[0,1].plot(np.linspace(0, 10, vis_len, endpoint=False), In_data[2], 'r-', label="Gauss no. 2")
    # ax[0,1].plot(np.linspace(0, 10, vis_len, endpoint=False), In_data[3], 'b-', label="Gauss no. 3")

    # ax[0,0].plot(Y_NN[1][0], Gauss(Y_NN[1][0], 1, Y_NN[1][0], Y_NN[1][1]), 'k*', label="Predicted mean")
    # ax[0,0].plot(Y_NN[2][0], Gauss(Y_NN[2][0], 1, Y_NN[2][0], Y_NN[2][1]), 'r*', label="Predicted mean")
    # ax[0,0].plot(Y_NN[3][0], Gauss(Y_NN[3][0], 1, Y_NN[3][0], Y_NN[3][1]), 'b*', label="Predicted mean")
    # ax[0,0].set_xlabel('Argument X')
    # ax[0,0].set_ylabel('Value Y')

    # leg = ax[0,0].legend(loc = 'upper left', prop={'size':7})

    # A, u, sigma = round(A, 8), round(u, 8), round(sigma, 8)
    # a_opt, b_opt = round(a_opt, 8), round(b_opt, 8)
    # ax[0,0].text(0.45, 1.12, " Mean: " + str(round(Y_data[1][0],3)) + ", NN prediction: " + str(round(Y_NN[1][0],3)),
    #    horizontalalignment='center', verticalalignment='center',
    #    transform=ax[0,0].transAxes, color = 'k')
    # ax[0,0].text(0.45, 1.07, " Mean: " + str(round(Y_data[2][0], 3)) + ", NN prediction: " + str(round(Y_NN[2][0], 3)),
    #        horizontalalignment='center', verticalalignment='center',
    #        transform=ax[0,0].transAxes, color='r')
    # ax[0,0].text(0.45, 1.02, " Mean: " + str(round(Y_data[3][0], 3)) + ", NN prediction: " + str(round(Y_NN[3][0], 3)),
    #        horizontalalignment='center', verticalalignment='center',
    #        transform=ax[0,0].transAxes, color='b')

    # n, bins, patches = ax[0, 1].hist(Y_data[:,0] - Y_NN[:,0], 100, alpha=0.5, color = 'red', label='Mean')
    # ax[0, 1].set_xlabel('Real - NN prediction')
    # ax[0, 1].set_ylabel('Number of counts')

    # n, bins, patches = ax[1, 1].hist(Y_data[:,1] - Y_NN[:,1], 100, alpha=0.5, color = 'blue', label='St. dev.')
    # ax[1, 1].set_xlabel('Real - NN prediction')
    # ax[1, 1].set_ylabel('Number of counts')
    # axs[0, 1].axvline(x=np.mean(Mass_B_data), color='r', linestyle='dashed')
    # ax[0, 1].legend(loc='upper right')
    # ax[1, 1].legend(loc='upper right')

    # ax[1, 0].plot(range(0,epoch), EvolutionalNN.loss_vector, 'k-', label="Loss function")
    # ax[1, 0].set_xlabel('Epoch number')
    # ax[1, 0].set_ylabel('Loss function')
    # ax[1, 0].set_yscale('log')

    plt.show()


if __name__ == "__main__":
    model_classifier()