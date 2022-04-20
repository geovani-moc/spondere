import unittest
from entity.user import User

class test_user(unittest.TestCase):
    def testCreate(self):
        name = 'teste1'
        code = '000001'
        userTest = 'apg'
        feature =  [12,12,34,34,51,54]

        user = User(name, code, userTest)
        user.setFeature(feature)

        self.assertEqual(name, user.name, 'Erro class, nome')
        self.assertEqual(code, user.code, 'Erro class, codigo')
        self.assertEqual(userTest, user.user, 'Erro class, usuario')
        self.assertEqual(feature, user.faceFeatures, 'Erro class, caracteristicas')

        print(user)

if __name__=='__main__':
    unittest.main()