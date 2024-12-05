import numpy as np
import pandas as pd


def switch_elements(sample_a: list, sample_b: list, index: list):
    a_final: list = sample_a.copy()
    a_final[index[0]] = sample_b[index[1]]
    b_final: list = sample_b.copy()
    b_final[index[1]] = sample_a[index[0]]
    return (a_final, b_final)


def switch_elements_arrays(sample_a: np.array, sample_b: np.array, index: list):
    a_final: np.array = np.copy(sample_a)
    a_final[index[0]] = sample_b[index[1]]
    b_final: np.array = np.copy(sample_b)
    b_final[index[1]] = sample_a[index[0]]
    a_final_dataframe = pd.DataFrame(a_final)
    b_final_dataframe = pd.DataFrame(b_final)
    return (a_final_dataframe, b_final_dataframe)
