import csv
import numpy as np
import pandas as pd


# def load_data(filepath):
#     with open(filepath, encoding="utf-8") as f:
#         csvReader = csv.DictReader(f)
#         gradeList = list(csvReader)
#         return gradeList


# myDict = load_data(
#     r"C:\Users\nithi\Downloads\madeasy\tabula-report-gradedistribution-2021-2022fall.csv"
# )

# print(myDict['108 A A E Grades']['Intro to Ag & Applied Econ 215 001']['A'])


def parse_cancer(filename):
    df = pd.read_csv(
        filename,
        delimiter=";",
        on_bad_lines="skip",
    )
    # values = ["A", "AB", "B"]
    print(df.columns.tolist())
    # df = df[df.average != "A"]
    print(df)


if __name__ == "__main__":
    parse_cancer(
        r"C:\Users\nithi\Downloads\madeasy\tabula-report-gradedistribution-2021-2022fall.csv"
    )
