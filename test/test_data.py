import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":

    x = np.linspace(10, 1000, 10)
    y = np.sin(x) + x**2

    fig, ax = plt.subplots(3)
    ax[0].plot(x, y / 1e6, 'bo-')
    ax[1].plot(x, y, 'bo-')
    ax[1].set_yscale('log')
    ax[2].plot(x, y, 'bo-')
    ax[2].set_xscale('log')
    ax[2].set_yscale('log')

    plt.savefig("test.png")

    test1 = np.loadtxt("test_data1.csv", delimiter=',', skiprows=1)
    test2 = np.loadtxt("test_data2.csv", delimiter=',', skiprows=1)
    test3 = np.loadtxt("test_data3.csv", delimiter=',', skiprows=1)

    fig, ax = plt.subplots(3)
    ax[0].plot(x, y/1e6, 'bo-')
    ax[1].plot(x, y, 'bo-')
    ax[1].set_yscale('log')
    ax[2].plot(x, y, 'bo-')
    ax[2].set_xscale('log')
    ax[2].set_yscale('log')

    ax[0].plot(test1[:,0],test1[:,1], 'ro-')
    ax[1].plot(test2[:,0],test2[:,1], 'ro-')
    ax[2].plot(test3[:,0],test3[:,1], 'ro-')

    plt.savefig("extracted.png")
