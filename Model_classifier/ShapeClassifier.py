import numpy as np
from random import random
import torch
from matplotlib import pyplot as plt
import math

from ShapeCreator import ShapeCreator
from ENN_classifier import ENN_classifier
from RandomModelGenerator import generate_data

def Gauss( x, A, u, sigma ):
    return  A * np.exp(-np.power(x - u, 2) / (2 * np.power(sigma, 2)))


def main():
    epoch = 50
    rate = 200
    classes = 10
    EvolutionalNN = ENN_classifier(20, 20, 10, 5, classes)


    X_data = [[X/2 for X in range(20)] for it in range(classes*rate)]
    Y_data = [ 0 for X in X_data]

    X_data, Y_data = generate_data(X_data, Y_data)
    Dataset = ShapeCreator(X_data, "dummy", Y_data)

    EvolutionalNN.train(Dataset, epoch, 20 )

    #After training, checking performance
    X_test = [[X/2 for X in range(20)] for it in range(classes*rate)]
    Y_test = [ 0 for X in X_data]
    X_test, Y_test = generate_data(X_test, Y_test, rate)
    X_NN = torch.tensor(X_test)
    Y_NN = EvolutionalNN.model(X_NN)
    Y_NN = Y_NN.detach().numpy()

    #for i in range(len(Y_data)):
    #    print("Mean, real : ", Y_data[i][0], " , trained: ", Y_NN[i][0])
    #    print("Std, real : ", Y_data[i][1], " , trained: ", Y_NN[i][1])

    #vis_len = 100
    #In_data = [[0 for t2 in range(vis_len)] for t1 in range(len(X_data))]
    #F_X = np.linspace(0, 10, vis_len, endpoint=False)
    #for i in range(len(X_data)):
    #    for j in range(vis_len):
    #        In_data[i][j] = Gauss(F_X[j], 1, Y_data[i][0], Y_data[i][1])

    fig, ax = plt.subplots(2,2)
    fig.set_size_inches(8, 8)
    n, bins, patches = ax[0, 0].hist(Y_NN[1:500,0], 100, alpha=0.5, range = [0,1], color = 'red', label='Gauss')
    n, bins, patches = ax[0, 0].hist(Y_NN[1500:2000, 0], 100, alpha=0.5, range = [0,1],color='blue', label='Gauss + Gauss')
    n, bins, patches = ax[0, 0].hist(Y_NN[500:1000, 0], 100, alpha=0.5, range = [0,1],color='green', label='Gauss + Exp')
    n, bins, patches = ax[0, 0].hist(Y_NN[1000:1500, 0], 100, alpha=0.5, range=[0, 1], color='yellow', label='Exp')
    ax[0, 0].set_xlabel('Class A (Gauss)')
    ax[0, 0].set_ylabel('Number of counts')
    ax[0, 0].legend(loc='upper right')
    ax[0, 0].set_title('Class affiliation probability')

    ax[1, 0].plot(range(0,epoch), EvolutionalNN.loss_vector, 'k-', label="Loss function")
    ax[1, 0].set_xlabel('Epoch number')
    ax[1, 0].set_ylabel('Loss function')
    ax[1, 0].set_yscale('log')

    #ax[0,0].plot(np.linspace(0, 10, vis_len, endpoint=False), In_data[1], 'k-', label="Gauss no. 1")
    #ax[0,0].plot(np.linspace(0, 10, vis_len, endpoint=False), In_data[2], 'r-', label="Gauss no. 2")
    #ax[0,0].plot(np.linspace(0, 10, vis_len, endpoint=False), In_data[3], 'b-', label="Gauss no. 3")

    #ax[0,0].plot(Y_NN[1][0], Gauss(Y_NN[1][0], 1, Y_NN[1][0], Y_NN[1][1]), 'k*', label="Predicted mean")
    #ax[0,0].plot(Y_NN[2][0], Gauss(Y_NN[2][0], 1, Y_NN[2][0], Y_NN[2][1]), 'r*', label="Predicted mean")
    #ax[0,0].plot(Y_NN[3][0], Gauss(Y_NN[3][0], 1, Y_NN[3][0], Y_NN[3][1]), 'b*', label="Predicted mean")
    #ax[0,0].set_xlabel('Argument X')
    #ax[0,0].set_ylabel('Value Y')

    #leg = ax[0,0].legend(loc = 'upper left', prop={'size':7})

    #A, u, sigma = round(A, 8), round(u, 8), round(sigma, 8)
    #a_opt, b_opt = round(a_opt, 8), round(b_opt, 8)
    #ax[0,0].text(0.45, 1.12, " Mean: " + str(round(Y_data[1][0],3)) + ", NN prediction: " + str(round(Y_NN[1][0],3)),
    #    horizontalalignment='center', verticalalignment='center',
    #    transform=ax[0,0].transAxes, color = 'k')
    #ax[0,0].text(0.45, 1.07, " Mean: " + str(round(Y_data[2][0], 3)) + ", NN prediction: " + str(round(Y_NN[2][0], 3)),
    #        horizontalalignment='center', verticalalignment='center',
    #        transform=ax[0,0].transAxes, color='r')
    #ax[0,0].text(0.45, 1.02, " Mean: " + str(round(Y_data[3][0], 3)) + ", NN prediction: " + str(round(Y_NN[3][0], 3)),
    #        horizontalalignment='center', verticalalignment='center',
    #        transform=ax[0,0].transAxes, color='b')

    #n, bins, patches = ax[0, 1].hist(Y_data[:,0] - Y_NN[:,0], 100, alpha=0.5, color = 'red', label='Mean')
    #ax[0, 1].set_xlabel('Real - NN prediction')
    #ax[0, 1].set_ylabel('Number of counts')

    #n, bins, patches = ax[1, 1].hist(Y_data[:,1] - Y_NN[:,1], 100, alpha=0.5, color = 'blue', label='St. dev.')
    #ax[1, 1].set_xlabel('Real - NN prediction')
    #ax[1, 1].set_ylabel('Number of counts')
    #axs[0, 1].axvline(x=np.mean(Mass_B_data), color='r', linestyle='dashed')
    #ax[0, 1].legend(loc='upper right')
    #ax[1, 1].legend(loc='upper right')

    #ax[1, 0].plot(range(0,epoch), EvolutionalNN.loss_vector, 'k-', label="Loss function")
    #ax[1, 0].set_xlabel('Epoch number')
    #ax[1, 0].set_ylabel('Loss function')
    #ax[1, 0].set_yscale('log')

    plt.show()

if __name__ == "__main__" :
    main()
