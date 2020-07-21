import numpy as np
import pandas as pd

def test(file_path):
    df = pd.read_csv(file_path)
    print(df.describe())
    return

if __name__ == "__main__":
    test("./transaction/all_cate_top10_transaction_simplified.csv")