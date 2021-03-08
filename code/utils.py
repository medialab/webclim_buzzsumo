import os

import pandas as pd
import matplotlib.pyplot as plt


def import_data(folder, file_name):
    data_path = os.path.join(".", "data", folder, file_name)
    df = pd.read_csv(data_path)
    return df


def save_figure(figure_name):
    figure_path = os.path.join('.', 'figure', figure_name)
    plt.savefig(figure_path)
    print("The '{}' figure is saved.".format(figure_name))