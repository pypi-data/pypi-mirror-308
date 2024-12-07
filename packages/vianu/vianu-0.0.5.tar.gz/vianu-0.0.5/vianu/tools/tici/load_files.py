import pandas as pd
from typing import List
from config import (
    FDA_FILEPATH,
    USAN_FILEPATH,
    RXNORM_FILEPATH,
    SWISSMEDIC_FILEPATH,
)
def read_medicament_file_as_list(chosen_sources: List):
    """
    read_medicament_file reads files from any of the four sources ['fda','rxnorm','usan','swissmedic']

    Input:
    chosen_sources: List with any number out of the possible sources ['fda','rxnorm','usan','swissmedic']

    Return:
    File: read individual file for that specific source.
    """
    if chosen_sources == 'fda':
        # Read file for comparison
        filepath = FDA_FILEPATH
        data = pd.read_csv(filepath, header=None, delimiter="|")
        name = pd.Series(data.iloc[:, [1, 4]].to_numpy().flatten())
        name = name.drop_duplicates()
        name = name.dropna().to_list()

    elif chosen_sources == 'usan':
        filepath = USAN_FILEPATH
        data = pd.read_csv(filepath, header='infer', delimiter=";")
        name = data.Examples.to_numpy().flatten()
        name = pd.Series(name).drop_duplicates()
        name = name.dropna()
        name = name.to_list()
        print("Number of drugs USAN database: ", len(name))

    elif chosen_sources == 'rxnorm':
        filepath = RXNORM_FILEPATH
        data = pd.read_csv(filepath, header=None, delimiter="|")
        name = data.iloc[:, 1].to_numpy().flatten()
        name = pd.Series(name).drop_duplicates()
        name = name.dropna().to_numpy()
        list_output = [drug.upper() for drug in name]
        print("Number of drugs at the RxNorm database: ", len(list_output))
        return list_output

    elif chosen_sources == 'swissmedic':
        filepath = SWISSMEDIC_FILEPATH
        data = pd.read_excel(filepath, skiprows=6, header=0)
        col_compounds = 'Bezeichnung des Arzneimittels\n\n\nDénomination du médicament'

        data['drug_name'] = data[col_compounds].apply(extract_drug_name)
        name = data['drug_name'].to_numpy().flatten()
        name = pd.Series(name).drop_duplicates()
        name = name.dropna().to_numpy()
        list_output = [drug.upper() for drug in name]
        print("Number of drugs at the Swissmedic database: ", len(list_output))
        return list_output

    else:
        name = False

    return name