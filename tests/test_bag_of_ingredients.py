import unittest
from modules.bag_of_ingredients import BagOfIngredients
from modules.constants import Ingredient


class TestBagOfIngredients(unittest.TestCase):
    """
    This unittest class is used to test the bag_of_ingredients module.
    """

    def test_boi_constructor(self):
        """
        Tests the constructor to return a BagOfIngredient object.
        """
        boi = BagOfIngredients("asngfuisetb@aa.com")
        self.assertIsInstance(boi, BagOfIngredients)

    def test_get_boi_registered(self):
        """
        Test a registered user. Should get a list object back.
        """
        boi = BagOfIngredients("aa@aa.com")
        list_of_ingredients = boi.get_boi()
        self.assertIsInstance(list_of_ingredients, list)

    def test_get_boi_unregistered(self):
        """
        Test an unregistered user. Should get an empty list object back.
        """
        boi = BagOfIngredients("asngfuisetb@aa.com")
        list_of_ingredients = boi.get_boi()
        self.assertIsInstance(list_of_ingredients, list)
        self.assertTrue(len(list_of_ingredients) == 0)

    def test_push_boi_ingredient_already_in_bag(self):
        """
        Test an registered user, but ingredient already exists in the bag.
        Should return False
        """
        boi = BagOfIngredients("aa@aa.com")
        push_check = boi.push_boi(Ingredient(ingredient_full="10 grams salt",
                                             ingredient_name="salt", amount=10,
                                             units="grams"))
        self.assertFalse(push_check)

    def test_delete_ingredient(self):
        """
        Tests to delete an ingredient. Should return True
        """
        boi = BagOfIngredients("aa@aa.com")
        delete_check = boi.delete_ingredient(ingredient_name="anything")
        self.assertTrue(delete_check)

    def test_update_ingredient(self):
        """
        Tests to update a specific ingredient. Should return True
        """
        boi = BagOfIngredients("aa@aa.com")
        update_check = boi.update_ingredient(ingredient_name="salt",
                                             new_quantity="10")
        self.assertTrue(update_check)


if __name__ == '__main__':
    unittest.main()
