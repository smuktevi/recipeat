import unittest
from modules.bag_of_ingredients import BagOfIngredients


class TestBagOfIngredients(unittest.TestCase):
    """
    This unittest class is used to test the bag_of_ingredients module.
    """

    def test_get_boi(self):
        """
        Test an already registered email address. Should return false
        """
        boi = BagOfIngredients("aa@aa.com")
        print(type(boi))



if __name__ == '__main__':
    unittest.main()
