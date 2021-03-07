import pandas as pd


def boi_convert_to_json(df):
    """
    Takes in dataframe object and converts it to a JSON object.
    Returns the JSON object

    :param df:
    :return: json object
    """

    return df.to_json(orient="records")


def boi_convert_to_df(json):
    """

    :param json:
    :return: pandas DataFrame object
    """

    return pd.read_json(json_obj, orient="records")


'''
if __name__ == '__main__':
    dataframe = pd.DataFrame({"a": [1, 2, 3], "b": [9, 8, 7], "c": [10, 20, 30]})
    json_obj = boi_convert_to_json(dataframe)
    print(json_obj)

    print(boi_convert_to_df(json_obj))
'''
