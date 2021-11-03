import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()
        self.maksukortti = Maksukortti(1000)
    
    def test_kassapaatteen_saldo_alussa_on_oikein(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
    
    def test_kateisosto_kun_raha_riittaa(self):
        vaihtoraha=self.kassapaate.syo_edullisesti_kateisella(300)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100240)
        self.assertEqual(vaihtoraha, 60)
        self.assertEqual(self.kassapaate.edulliset,1)
        
        vaihtoraha=self.kassapaate.syo_maukkaasti_kateisella(500)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100640)
        self.assertEqual(vaihtoraha, 100)
        self.assertEqual(self.kassapaate.maukkaat,1)
    
    def test_kateisosto_kun_raha_ei_riita(self):
        vaihtoraha=self.kassapaate.syo_edullisesti_kateisella(200)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(vaihtoraha, 200)
        self.assertEqual(self.kassapaate.edulliset,0)

        vaihtoraha=self.kassapaate.syo_maukkaasti_kateisella(200)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(vaihtoraha, 200)
        self.assertEqual(self.kassapaate.maukkaat,0)

    def test_korttiosto_kun_raha_riittaa(self):
        self.assertTrue(self.kassapaate.syo_edullisesti_kortilla(self.maksukortti))
        self.assertEqual(self.kassapaate.edulliset, 1)
        self.assertEqual(self.maksukortti.saldo, 760)
        self.assertTrue(self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti))
        self.assertEqual(self.kassapaate.maukkaat, 1)
        self.assertEqual(self.maksukortti.saldo, 360)
        self.assertEqual(self.kassapaate.kassassa_rahaa,100000)
    
    def test_korttiosto_kun_raha_ei_riita(self):
        self.maksukortti.ota_rahaa(999)
        self.assertFalse(self.kassapaate.syo_edullisesti_kortilla(self.maksukortti))
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.maksukortti.saldo, 1)
        self.assertFalse(self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti))
        self.assertEqual(self.kassapaate.maukkaat, 0)
        self.assertEqual(self.maksukortti.saldo, 1)
        self.assertEqual(self.kassapaate.kassassa_rahaa,100000)
    
    def test_lataa_rahaa_kortille(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti,1)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100001)
        self.assertEqual(self.maksukortti.saldo, 1001)

        self.kassapaate.lataa_rahaa_kortille(self.maksukortti,-1)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100001)
        self.assertEqual(self.maksukortti.saldo, 1001)