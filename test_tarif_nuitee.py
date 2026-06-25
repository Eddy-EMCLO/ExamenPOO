"""Batterie de référence - objet-valeur TarifNuitee (épreuve centrale).

Spécification exécutable autoportante : égalité et ordre par valeur,
garde de type sur le montant (booléen exclu), addition et comparaison
réservées aux mêmes devises, refus des opérations avec un non-TarifNuitee.

Programmation Orientée Objet - EICPN 2025-2026.
"""

import unittest

from tarif_nuitee import TarifNuitee


class TestTarifNuiteeConstruction(unittest.TestCase):

    def test_construction_nominale(self):
        t = TarifNuitee(85.50, "EUR")
        self.assertEqual(t.montant, 85.50)
        self.assertEqual(t.devise, "EUR")

    def test_devise_par_defaut_eur(self):
        self.assertEqual(TarifNuitee(50).devise, "EUR")

    def test_montant_entier_converti_en_float(self):
        t = TarifNuitee(85)
        self.assertIsInstance(t.montant, float)
        self.assertEqual(t.montant, 85.0)

    def test_montant_zero_accepte(self):
        self.assertEqual(TarifNuitee(0).montant, 0.0)

    def test_montant_non_nombre_leve_TypeError(self):
        with self.assertRaises(TypeError):
            TarifNuitee("85")

    def test_montant_booleen_leve_TypeError(self):
        with self.assertRaises(TypeError):
            TarifNuitee(True)

    def test_montant_negatif_leve_ValueError(self):
        with self.assertRaises(ValueError):
            TarifNuitee(-5)

    def test_attributs_en_lecture_seule(self):
        t = TarifNuitee(85)
        with self.assertRaises(AttributeError):
            t.montant = 90


class TestTarifNuiteeEgalite(unittest.TestCase):

    def test_egalite_de_valeur(self):
        self.assertEqual(TarifNuitee(85, "EUR"), TarifNuitee(85, "EUR"))

    def test_inegalite_montants(self):
        self.assertNotEqual(TarifNuitee(85, "EUR"), TarifNuitee(40, "EUR"))

    def test_inegalite_devises(self):
        self.assertNotEqual(TarifNuitee(85, "EUR"), TarifNuitee(85, "USD"))

    def test_hash_egal_pour_valeurs_egales(self):
        self.assertEqual(
            hash(TarifNuitee(85, "EUR")), hash(TarifNuitee(85, "EUR")))

    def test_utilisable_dans_un_set(self):
        ensemble = {TarifNuitee(85, "EUR"), TarifNuitee(85, "EUR"),
                    TarifNuitee(40, "EUR")}
        self.assertEqual(len(ensemble), 2)

    def test_eq_avec_non_tarif_retourne_notimplemented(self):
        self.assertNotEqual(TarifNuitee(85), 85)


class TestTarifNuiteeOrdre(unittest.TestCase):

    def test_inferieur(self):
        self.assertLess(TarifNuitee(40, "EUR"), TarifNuitee(85, "EUR"))

    def test_total_ordering_derive_les_autres(self):
        a, b = TarifNuitee(40, "EUR"), TarifNuitee(85, "EUR")
        self.assertLessEqual(a, b)
        self.assertGreater(b, a)
        self.assertGreaterEqual(b, a)

    def test_tri_d_une_liste(self):
        tarifs = [TarifNuitee(85, "EUR"), TarifNuitee(40, "EUR"),
                  TarifNuitee(60, "EUR")]
        montants = [t.montant for t in sorted(tarifs)]
        self.assertEqual(montants, [40.0, 60.0, 85.0])

    def test_comparaison_devises_differentes_leve_ValueError(self):
        with self.assertRaises(ValueError):
            TarifNuitee(85, "EUR") < TarifNuitee(85, "USD")


class TestTarifNuiteeAddition(unittest.TestCase):

    def test_addition_meme_devise(self):
        somme = TarifNuitee(85, "EUR") + TarifNuitee(40, "EUR")
        self.assertEqual(somme, TarifNuitee(125, "EUR"))

    def test_addition_retourne_nouvel_objet(self):
        a = TarifNuitee(85, "EUR")
        somme = a + TarifNuitee(40, "EUR")
        self.assertIsNot(somme, a)
        self.assertEqual(a.montant, 85.0)

    def test_addition_devises_differentes_leve_ValueError(self):
        with self.assertRaises(ValueError):
            TarifNuitee(85, "EUR") + TarifNuitee(40, "USD")

    def test_addition_avec_non_tarif_leve_TypeError(self):
        with self.assertRaises(TypeError):
            TarifNuitee(85, "EUR") + 40


class TestTarifNuiteeRepresentation(unittest.TestCase):

    def test_str_deux_decimales(self):
        self.assertEqual(str(TarifNuitee(85.5, "EUR")), "85.50 EUR")

    def test_repr_reconstructible(self):
        t = TarifNuitee(85.5, "EUR")
        reconstruit = eval(repr(t), {"TarifNuitee": TarifNuitee})
        self.assertEqual(reconstruit, t)


if __name__ == "__main__":
    unittest.main()
