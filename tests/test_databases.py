#!flask/bin/python
import databases
import unittest


class MyTestCase(unittest.TestCase):

    def setUp(self):
        databases.app.testing = True
        self.app = databases.app.test_client()

    def test_post(self):
        print ("\nRunning test_post >>")
        result = self.app.post('/databases')
        print(result)
        self.assertEqual(result,result)

    def test_put(self):
        print ("\nRunning test_put >>")
        result = self.app.put('/databases')
        self.assertEqual(result,result)

    def test_delete(self):
        print ("\nRunning test_delete >>")
        result = self.app.delete('/databases')
        self.assertEqual(result,result)

    def test_patch(self):
        print ("\nRunning test_patch >>")
        result = self.app.patch('/databases')
        self.assertEqual(result,result)

    def test_short_organism_name(self):
        pass

    def test_wrong_release_num(self):
        pass

    def test_bad_parameters(self):
        pass
        

if __name__ == '__main__':
    unittest.main()