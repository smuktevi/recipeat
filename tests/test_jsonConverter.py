import unittest
import pandas as pd
from modules import jsonConverter


class test_jsonConverter(unittest.TestCase):

    def test_boi_convert_to_df(self):
        dataframe = pd.DataFrame({"a": [1, 2, 3], "b": [9, 8, 7], "c": [10, 20, 30]})
        json_obj = jsonConverter.boi_convert_to_json(dataframe)
        self.assertTrue(json_obj == '[{"a":1,"b":9,"c":10},{"a":2,"b":8,"c":20},{"a":3,"b":7,"c":30}]')


if __name__ == '__main__':
    unittest.main()
