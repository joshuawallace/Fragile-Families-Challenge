########################
# Created 3-22-17 by JJW
# Some functions for the Fragile Families Challenge,
# this particular set of functions will plot up the
# results from a model prediction for visual inspection of
# goodness of modelling, etc.
#
#
########################


import matplotlib.pyplot as plt
import numpy as np


def plot_predict_actual_pairs(predicted_values, actual_values, ylabel="The values"):
    predicted_values_to_use = np.asarray(predicted_values)
    actual_values_to_use    = np.asarray(actual_values)
    order = actual_values_to_use.argsort()

    predicted_values_to_plot = predicted_values_to_use[order]
    actual_values_to_plot    = actual_values_to_use[order]

    number_of_things_to_plot = len(predicted_values_to_plot)

    fig= plt.figure()

    for i in range(number_of_things_to_plot):
        plt.plot(2*[float(i)/float(number_of_things_to_plot)],
                 [predicted_values_to_plot[i], actual_values_to_plot[i]],
                 color='blue', marker=None, linewidth=.05)
        plt.scatter(float(i)/float(number_of_things_to_plot),
                    predicted_values_to_plot[i], s=5)
        plt.scatter(float(i)/float(number_of_things_to_plot),
                    actual_values_to_plot[i], s=20)

    plt.ylabel(ylabel)
    #plt.set_xticklabels([])

    return fig

def plot_errors_func_k_noalpha(mean_squared_error, r_squared_error, k_values):
    fig = plt.figure(figsize=(7,4))
    ax = fig.add_subplot(111)
    ln1 = ax.plot(k_values, mean_squared_error, label="MSE", color='blue', ls='--')

    ax2 = ax.twinx()
    ln2 = ax2.plot(k_values, np.mean(r_squared_error, axis=1), label="R^2mean", color='red')
    ln3 = ax2.plot(k_values, np.median(r_squared_error, axis=1), label="R^2median", color='green')

    lns = ln1+ln2+ln3
    labs = [l.get_label() for l in lns]
    ax.legend(lns, labs, loc='best')

    ax.set_ylabel("MSE")
    ax2.set_ylabel("R^2")
    ax.set_xlabel("Value for K")
    ax2.set_ylim(-0.1, .9)

    fig.tight_layout()

    return fig


def plot_errors_func_k_alpha(mean_squared_error, r_squared_error, k_values, alpha_values):
    fig1 = plt.figure(figsize=(7, 4))
    ax1 = fig1.add_subplot(111)
    for i in range(len(alpha_values)):
        ax1.plot(k_values, [line[i] for line in mean_squared_error], label=round(alpha_values[i], 5))

    ax1.set_ylabel("MSE")
    ax1.set_xlabel("Value for K")
    ax1.legend(loc='best')

    ##########################
    fig2 = plt.figure(figsize=(7, 4))
    ax2 = fig2.add_subplot(111)
    for i in range(len(alpha_values)):
        ax2.plot(k_values, [np.mean(line[i]) for line in r_squared_error], label=round(alpha_values[i], 5))

    ax2.set_ylabel("Mean R^2")
    ax2.set_xlabel("Value for K")
    ax2.set_ylim(-0.5,1)
    ax2.legend(loc='best')

    ##########################
    fig3 = plt.figure(figsize=(7, 4))
    ax3 = fig3.add_subplot(111)
    for i in range(len(alpha_values)):
        ax3.plot(k_values, [np.median(line[i]) for line in r_squared_error], label=round(alpha_values[i], 5))

    ax3.set_ylabel("Median R^2")
    ax3.set_xlabel("Value for K")
    ax3.set_ylim(-0.5,1)
    ax3.legend(loc='best')

    fig1.tight_layout()
    fig2.tight_layout()
    fig3.tight_layout()

    return (fig1, fig2, fig3)
