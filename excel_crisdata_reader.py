import pandas as pd
from researcher import Researcher
from rowParser import CRISParser as rp

def extract_researchers(file, sheet_name='main_entities'):
    df = pd.read_excel(file, sheet_name=sheet_name)

    researchers = []
    size = len(df.index)
    for index, row in df.iterrows():
        print(f'\rLoading Researchers ... [{index}/{size}]', end='')
            
        name = rp.parse_full_name(row)
        rs = Researcher(
            name['firstName'],
            name['lastName'],
            rp.parse_crisid(row),
            scholar_url=rp.parse_scholar_url(row),
            orcid=rp.parse_orcid(row),
            rg_url=rp.parse_research_gate_url(row))
        researchers.append(rs)

    print(f'\rLoad Completed! ... [{index}/{size}]', end='')
    return researchers


