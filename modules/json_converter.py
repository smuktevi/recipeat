import pandas as pd


class JsonConverter:
    """
    Class used to convert json to pandas dataframe and vice versa.
    """

    def convert_to_json(self, df):
        """
        Takes in dataframe object and converts it to a JSON object.
        Returns the JSON object

        :param df: dataframe
        :return: json object
        """

        return df.to_json(orient="records")

    def convert_to_df(self, json):
        """
        Takes in json object and converts it to a dataframe object.
        Returns the JSON object

        :param json: json object
        :return: pandas DataFrame object
        """

        return pd.read_json(json, orient="records")
