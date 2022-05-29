import unittest
import course_instructor as ci

class DataMethodTests(unittest.TestCase):
    '''
    Tests class
    '''
    def test_id_map(self):
        '''
        Tests id_map function
        '''
        self.assertEqual(ci.id_map('1214'), '48')
        self.assertEqual(ci.id_map('1216'), '49')
        self.assertEqual(ci.id_map('1222'), '50')
        self.assertEqual(ci.id_map('1224'), '51')
        self.assertEqual(ci.id_map('1226'), '52')
        self.assertEqual(ci.id_map('1232'), '53')

if __name__ == '__main__':
    unittest.main()