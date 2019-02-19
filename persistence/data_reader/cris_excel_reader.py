import pandas as pd
from model.researcher import Researcher
from persistence.data_reader.row_parser import CRISParser

def load_researchers(file, sheet_name='main_entities'):
    dataframe = pd.read_excel(file, sheet_name=sheet_name)

    researchers = []
    size = len(dataframe.index)
    for index, raw_row in dataframe.iterrows():
        print(f'\rLoading Researchers ... [{index+1}/{size}]', end='')
        
        row = CRISParser(raw_row)
        name = row.parse_full_name()
        researcher = Researcher(
            name['firstName'],
            name['lastName'],
            row.parse_crisid(),
            scholar_url=row.parse_scholar_url(),
            orcid=row.parse_orcid(),
            rg_url=row.parse_research_gate_url())

        researchers.append(researcher)

        # TEST
        if index > 4:
            break

    print(f'\nLoad Completed! {index+1} researchers extracted')
    return researchers


