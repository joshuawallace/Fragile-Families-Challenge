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


def plot_predict_actual_pairs(predicted_values, actual_values, ylabel="The values"):
    order = predicted_values.argsort()

    predicted_values_to_plot = predicted_values[order]
    actual_values_to_plot    = actual_values[order]

    number_of_things_to_plot = len(predicted_values_to_plot)

    fig = plt.figure(figsize=(4,4))

    for i in range(number_of_things_to_plot):
        fig.plot(2*[float(i)/float(number_of_things_to_plot)],
                 [predicted_values_to_plot[i], actual_values_to_plot[i]],
                 color='blue', marker=None)
        fig.scatter(float(i)/float(number_of_things_to_plot),
                    predicted_values_to_plot[i], markersize=20)
        fig.scatter(float(i)/float(number_of_things_to_plot),
                    actual_values_to_plot[i], markersize=5)

    fig.set_ylabel(ylabel)
    fig.set_xticklabels([])

    return fig