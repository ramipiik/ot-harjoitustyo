import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(10)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)
    
    def test_kortin_saldo_alussa_on_oikein(self):
        self.assertEqual(str(self.maksukortti), 'saldo: 0.1')
    
    def test_rahan_lisaaminen_kasvattaa_saldoa(self):
        self.maksukortti.lataa_rahaa(20)
        self.assertEqual(str(self.maksukortti), 'saldo: 0.3')
    
    def test_saldo_vahenee_kun_otetaan_rahaa(self):
        self.maksukortti.ota_rahaa(5)
        self.assertEqual(str(self.maksukortti), 'saldo: 0.05')

    def test_saldo_ei_vahene_kun_ei_saldoa(self):
        self.maksukortti.ota_rahaa(15)
        self.assertEqual(str(self.maksukortti), 'saldo: 0.1')
    
    def test_ota_rahaa_palauttaa_True_jos_on_saldoa(self):
        self.assertEqual(self.maksukortti.ota_rahaa(5), True)

    def test_ota_rahaa_palauttaa_False_jos_ei_saldoa(self):
        self.assertEqual(self.maksukortti.ota_rahaa(15), False)