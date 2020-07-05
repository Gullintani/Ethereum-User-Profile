import pandas as pd
import numpy as np
from efficient_apriori import apriori

def get_address_list(file_path:str):
    df = pd.read_csv(file_path)
    address_array = np.unique(df["from"].values)
    with open('./transaction/temp.txt', 'w') as w:
        w.write(str(address_array.tolist()))
    return

def test():
    transactions = [('eggs', 'bacon', 'soup'),
                ('eggs', 'bacon', 'apple'),
                ('soup', 'bacon', 'banana')]
    print(type(transactions[0]))
    itemsets, rules = apriori(transactions, min_support=0.5, min_confidence=1)
    print(rules)  # [{eggs} -> {bacon}, {soup} -> {bacon}]
if __name__ == '__main__':
    # test()
    get_address_list("./transaction/0xC7af99Fe5513eB6710e6D5f44F9989dA40F27F26.csv")