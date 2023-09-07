"""
The datasets comes form
Gill, F, D Donsker, and P Rasmussen (Eds). 2023. IOC World Bird List (v 13.2). Doi 10.14344/IOC.ML.13.2.  http://www.worldbirdnames.org/

conda activate PyGIS2
python
#"""

IOCversion = "13.2"
master_dataset = f"master_ioc_list_v{IOCversion}.xlsx"
Multilang_dataset= f"Multiling_IOC-{IOCversion}.xlsx"
Outputdataset_dir = "BirdDatas"

import pandas as pd
import numpy as np

master = pd.read_excel(master_dataset, header = 3,index_col=[0,1,2,3,4,5,6,7])
master = master.reset_index()
master.columns
master[f"IOC_{IOCversion}"] = master["Genus"]+" "+master["Species (Scientific)"]
localized_species = master["Breeding Range"].dropna().index


Multilang = pd.read_excel(Multilang_dataset, header = 0,index_col=0)
master[f"IOC_{IOCversion}"]
Multilang[f"IOC_{IOCversion}"]

Merged = pd.merge(master.loc[localized_species,[f"IOC_{IOCversion}","Breeding Range"]],Multilang, on=f"IOC_{IOCversion}")
Merged = Merged.rename(columns={f"IOC_{IOCversion}":"IOC"})
Merged["Scientific"] = Merged["IOC"]
data_columns = Merged.columns[:4].tolist()
languages = Merged.columns[4:].tolist()

import os
os.makedirs(Outputdataset_dir, exist_ok=True)
for lang in languages:
    #fill the gaps with English names or Scientific names if English is missing (witch is not in my case)
    Merged.loc[Merged[lang].isna(),lang] = Merged.loc[Merged[lang].isna(),"English"]
    Merged.loc[Merged[lang].isna(),lang] = Merged.loc[Merged[lang].isna(),f"IOC"]
    Merged.loc[:, data_columns+[lang]].to_csv(f"{Outputdataset_dir}/All_bird_{lang}.csv")
    print(lang, ": Done")

pd.Series(languages).to_csv(f"{Outputdataset_dir}/All_bird_languages.csv")
