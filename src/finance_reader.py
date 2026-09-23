import pandas as pd


def reader_finance_from_csv(filepath):
    """Преобразуем файл из формата CSV в словарь"""
    dataframe = pd.read_csv(filepath, sep=";")
    return dataframe.to_dict("records")


def reader_finance_from_excel(filepath):
    """Преобразуем файл из формата EXCEL в словарь"""
    dataframe = pd.read_excel(filepath, engine="openpyxl")
    return dataframe.to_dict("records")
