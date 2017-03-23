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