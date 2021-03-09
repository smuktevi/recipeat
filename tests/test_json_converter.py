import unittest
import pandas as pd
from modules.json_converter import JsonConverter


class TestJsonConverter(unittest.TestCase):
    """
    Class used to test json and dataframe converter
    """

    def test_convert_to_df(self):
        """
        Test if the given dataframe returns a proper json object
        """
        dataframe = pd.DataFrame({"a": [1, 2, 3], "b": [9, 8, 7], "c": [10, 20, 30]})
        json_converter = JsonConverter()
        json_obj = json_converter.convert_to_json(dataframe)
        self.assertTrue(json_obj == '[{"a":1,"b":9,"c":10},{"a":2,"b":8,"c":20},{"a":3,"b":7,"c":30}]')

    def test_convert_to_json(self):
        """
        Test if the given json returns a df
        """
        json_obj = '[{"a":1,"b":9,"c":10},{"a":2,"b":8,"c":20},{"a":3,"b":7,"c":30}]'
        json_converter = JsonConverter()
        df = json_converter.convert_to_df(json_obj)
        self.assertTrue(isinstance(df, pd.DataFrame))


if __name__ == '__main__':
    unittest.main()
