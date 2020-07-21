import numpy as np
import pandas as pd

def extract_address_graph(address:str, file_path:str, save_path:str):
    df = pd.read_csv(file_path, dtype = {'timeStamp':int, 'from':object, 'to':object, 'value':float, 'contractAddress':object, 'gasUsed':float,
       'from_title':object, 'to_title':object, 'from_category':object, 'to_category':object})
    target = df.loc[(df["from"] == address)|(df["to"] == address)]
    target = target.fillna("NA")
    save_path = save_path + "experiment.csv"
    target.to_csv(save_path, index = False)

    print(f"{ address } degree 1 records saved")

    NA_from_list = target.loc[(target["from_title"] == "NA")]["from"].values
    NA_to_list = target.loc[(target["to_title"] == "NA")]["to"].values
    NA_list = np.unique(np.append(NA_from_list, NA_to_list))
    
    print("===========================start to add degree 1 records==============================")

    index = 1
    total = len(NA_list)
    for NA_address in NA_list:
        NA_df = df.loc[(df["from"] == NA_address)|(df["to"] == NA_address)]
        NA_df.to_csv(save_path, index=False, header=False, mode='a+')
        print(f"NA address records added { NA_address }; {index}/{total}")
        index += 1
    return

if __name__ == "__main__":
    extract_address_graph("0x0b882f0fc7584ab6f894f097aacda9db1886c18e", "./transaction/game/all_game_labeled.csv", "./transaction/experiment/")