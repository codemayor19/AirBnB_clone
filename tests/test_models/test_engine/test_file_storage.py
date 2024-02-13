import os
import unittest
import models
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage

class TestFileStorageInstallation(unittest.TestCase):
    """
    Testing the installation of file storage
    """
    def test_FileStorage_instantiation_no_args(self):
        # Test creatinf a FileStorage instance with no arguments
        self.assertEqual(type(FileStorage()), FileStorage)
    
    def test_FileStorage_instantiation_with_args(self):
        # Test creating a FileStorage instance with no argument
        # (Should raise TypeError)
        with self.assertRaises(TypeError):
            FileStorage(None)
    
    def test_FileStorage_initializes(self):
        # test if the storage variable in models is an instance of FileStorage
        self.assertEqual(type(models.storage), FileStorage)

class testFileStorage(unittest.TestCase):
    def setUp(self):
        # create a temporary test file after the test
        self.test_file = "test_file.json"
    
    def tearDown(self):
        # Remove the temporary test file after the test
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        
    def test_all_storage_returns_dictionary(self):
        # Test if the all() method returns a dictionary
        self.assertEqual(dict, type(models.storage.all()))
    
    def test_new(self):
        # Test the new method by creating and starting a new object
        obj = BaseModel()
        models.storage.new(obj)
        self.assertIn("BaseModel.{}".format(obj.id), models.storage.all())

    def test_new_with_args(self):
        # Test creating a new object with additional arguments
        # (Should raise TypeError)
        with self.assertRaises(TypeError):
            models.storage.new(BaseModel(), 1)
    
    def test_new_with_None(self):
        # test creatiing a new object with None (should raise AttributeError)
        with self.assertRaises(AttributeError):
            models.storage.new(None)
    
    def test_save_and_reload(self):
        # Test saving objects to a file and ten reloading them
        obj1 = BaseModel()
        obj2 = BaseModel()
        models.storage.new(obj1)
        models.storage.new(obj2)
        models.storage.save()

        # create a new storage instance to simulate reloading
        new_storage = FileStorage()
        new_storage.reload()

        # check if the reloaded objects watch the original objects
        self.assertTrue(new_storage.all().get("BaseModel.{}".format(obj1.id)) is not None)
        self.assertTrue(new_storage.all().get("BaseModel.{}".format(obj2.id)) is not None)

    def test_save_to_file(self):
        # Test saving objects to a file and check if the file is created
        obj = BaseModel()
        models.storage.new(obj)
        models.storage.save()
        self.assertTrue(os.path.exists(models.storage._FileStorage__file_path))

    def test_reload_empty_file(self):
        # Test reloading when the file is empty or does not exist
        with self.assertRaises(TypeError):
            models.storage()
            models.storage.reload()

if __name__ == '__main__':
    unittest.main()


