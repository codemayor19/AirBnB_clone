import os
import unittest
import models
from models.user import User
from models.base_model import BaseModel

class TestUser(unittest.TestCase):

    def setUp(self):
        # Create a temporary test file for saving data
        self.test_file = "test_file.json"
        models.storage.__file_path = self.test_file
        models.storage.save()

    def tearDown(self):
        # Remove the temporary test file after the test
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_user_attributes(self):
        # Create a new User instance
        test_user = User()
        # check if the default email attribute is an empty string
        self.assertEqual(test_user.email, "")
        # Check if the default password attribute is an empty string
        self.assertEqual(test_user.password, "")
        # Check if the default first_name attribute is an empty string
        self.assertEqual(test_user.first_name, "")
        # Check if the default last name attribute is an empty string
        self.assertEqual(test_user.last_name, "")

    def test_user_inherits_from_base_model(self):
        # Create a new User instanc
        test_user = User()
        # check if the User class is a subclass of BaseModel
        self.assertTrue(issubclass(User, BaseModel))
    
    def test_user_str_representation(self):
        # Create a new user instance
        test_user = User()
        # Set the attributes of the user instance
        test_user.email = "Johnson@example.com"
        test_user.first_name = "Johnson"
        test_user.last_name = "Dennis"
        test_user.password = "password123"
        # get the string representation of the User instance
        user_str = str(test_user)
        # check if "User" is present in the string representation
        self.assertIn("User", user_str)
        # Check if the email is present in the string representation
        self.assertIn("Johnson@example.com", user_str)
        # Check if the first name is present in the string representation
        self.assertIn("Johnson", user_str)
        # Check if the last name is present in the string representation
        self.assertIn("Dennis", user_str)

    def test_user_id_generation(self):
        # Create two different user Instances
        test_user = User()
        user2 = User()
        # Ensure that the 'id' attribute of each User instance is unique
        self.assertNotEqual(test_user.id, user2.id)

if __name__ == '__main__':
    unittest.main()
