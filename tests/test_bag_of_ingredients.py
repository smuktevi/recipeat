import unittest
from modules.bag_of_ingredients import BagOfIngredients
from modules.constants import Ingredient
import pytest

class TestBagOfIngredients(unittest.TestCase):
    """
    This unittest class is used to test the bag_of_ingredients module.
    """
    @pytest.mark.order(10)
    def test_boi_constructor(self):
        """
        Tests the constructor to return a BagOfIngredient object.
        """
        boi = BagOfIngredients("this_does_not_exist@aa.com")
        self.assertIsInstance(boi, BagOfIngredients)

    @pytest.mark.order(11)
    def test_get_boi_registered(self):
        """
        Test a registered user. Should get a list object back.
        """
        boi = BagOfIngredients("aa@aa.com")
        list_of_ingredients = boi.get_boi()
        self.assertIsInstance(list_of_ingredients, list)

    @pytest.mark.order(12)
    def test_get_boi_unregistered(self):
        """
        Test an unregistered user. Should get an empty list object back.
        """
        boi = BagOfIngredients("this_does_not_exist@aa.com")
        list_of_ingredients = boi.get_boi()
        self.assertIsInstance(list_of_ingredients, list)
        self.assertTrue(len(list_of_ingredients) == 0)

    @pytest.mark.order(13)
    def test_push_boi_ingredient_already_in_bag(self):
        """
        Test an registered user, but ingredient already exists in the bag.
        Should return False
        """
        boi = BagOfIngredients("aa@aa.com")
        boi.push_boi(Ingredient(ingredient_full="10 grams salt",
                                             ingredient_name="salt", amount=10,
                                             units="grams"))
        push_check = boi.push_boi(Ingredient(ingredient_full="10 grams salt",
                                             ingredient_name="salt", amount=10,
                                             units="grams"))
        self.assertFalse(push_check)

    @pytest.mark.order(15)
    def test_delete_ingredient(self):
        """
        Tests to delete an ingredient. Should return True
        """
        boi = BagOfIngredients("aa@aa.com")
        delete_check_failure = boi.delete_ingredient(ingredient_name="'ingredient_does_not_exist'")
        self.assertFalse(delete_check_failure)

        print("delete success check")
        delete_check_success = boi.delete_ingredient(ingredient_name="'salt'")
        print(delete_check_success)
        self.assertTrue(delete_check_success)

        self.assertFalse(boi.delete_ingredient(ingredient_name=None))

    @pytest.mark.order(14)
    def test_update_ingredient(self):
        """
        Tests to update a specific ingredient. Should return True
        """
        boi = BagOfIngredients("aa@aa.com")
        update_check = boi.update_ingredient(ingredient_name="'salt'",
                                             new_quantity="10")
        self.assertTrue(update_check)
        self.assertFalse(boi.update_ingredient(ingredient_name=None, new_quantity=None))


if __name__ == '__main__':
    unittest.main()
