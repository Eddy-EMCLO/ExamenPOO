"""Batterie de référence - conteneur CentraleReservation (épreuve centrale).

Spécification exécutable autoportante : protocoles de conteneur, refus
des doublons et des mauvais types, recherche par code, sous-ensemble des
hébergements libres, et comportement sur élément absent.

Programmation Orientée Objet - EICPN 2025-2026.
"""

import unittest

from hebergement import Hebergement, Gite, EmplacementCamping
from centrale import CentraleReservation

CODE = "RESA1234567890ABC"
CODE2 = "GITE000000000ABCD"
CODE3 = "CAMP000000000WXYZ"


def _hebergement(code=CODE, nom="Villa Soleil"):
    return Hebergement(nom, "Durbuy", code, 6, 2005)


class TestCentraleAjout(unittest.TestCase):

    def setUp(self):
        self.centrale = CentraleReservation()

    def test_centrale_neuve_est_vide(self):
        self.assertEqual(len(self.centrale), 0)

    def test_ajouter_augmente_la_taille(self):
        self.centrale.ajouter(_hebergement())
        self.assertEqual(len(self.centrale), 1)

    def test_ajouter_non_hebergement_leve_TypeError(self):
        with self.assertRaises(TypeError):
            self.centrale.ajouter("pas un hébergement")

    def test_ajouter_doublon_code_leve_ValueError(self):
        self.centrale.ajouter(_hebergement())
        with self.assertRaises(ValueError):
            self.centrale.ajouter(_hebergement(nom="Autre nom"))

    def test_sous_types_acceptes(self):
        self.centrale.ajouter(_hebergement())
        self.centrale.ajouter(Gite("Moulin", "Rochefort", CODE2, 4, 1890, 3))
        self.centrale.ajouter(
            EmplacementCamping("Pré", "La Roche", CODE3, 4, 2015, 80.0))
        self.assertEqual(len(self.centrale), 3)


class TestCentraleRetrait(unittest.TestCase):

    def setUp(self):
        self.centrale = CentraleReservation()
        self.h = _hebergement()
        self.centrale.ajouter(self.h)

    def test_retirer_diminue_la_taille(self):
        self.centrale.retirer(self.h)
        self.assertEqual(len(self.centrale), 0)

    def test_retirer_non_hebergement_leve_TypeError(self):
        with self.assertRaises(TypeError):
            self.centrale.retirer("pas un hébergement")

    def test_retirer_absent_leve_KeyError(self):
        with self.assertRaises(KeyError):
            self.centrale.retirer(_hebergement(code=CODE2))


class TestCentraleConteneur(unittest.TestCase):

    def setUp(self):
        self.centrale = CentraleReservation()
        self.h = _hebergement()
        self.centrale.ajouter(self.h)

    def test_contains_par_objet(self):
        self.assertIn(self.h, self.centrale)

    def test_contains_par_code(self):
        self.assertIn(CODE, self.centrale)

    def test_contains_absent(self):
        self.assertNotIn(CODE2, self.centrale)

    def test_contains_autre_type_retourne_false(self):
        self.assertNotIn(12345, self.centrale)

    def test_iteration_ordre_d_ajout(self):
        g = Gite("Moulin", "Rochefort", CODE2, 4, 1890, 3)
        self.centrale.ajouter(g)
        codes = [h.code_reservation for h in self.centrale]
        self.assertEqual(codes, [CODE, CODE2])


class TestCentraleMetier(unittest.TestCase):

    def setUp(self):
        self.centrale = CentraleReservation()
        self.h1 = _hebergement()
        self.h2 = _hebergement(code=CODE2, nom="Gîte du Lac")
        self.centrale.ajouter(self.h1)
        self.centrale.ajouter(self.h2)

    def test_trouver_par_code(self):
        self.assertIs(self.centrale.trouver_par_code(CODE), self.h1)

    def test_trouver_par_code_absent_leve_KeyError(self):
        with self.assertRaises(KeyError):
            self.centrale.trouver_par_code(CODE3)

    def test_hebergements_libres(self):
        self.h1.reserver()
        libres = self.centrale.hebergements_libres()
        self.assertEqual(libres, [self.h2])

    def test_nombre_libres(self):
        self.assertEqual(self.centrale.nombre_libres, 2)
        self.h1.reserver()
        self.assertEqual(self.centrale.nombre_libres, 1)


if __name__ == "__main__":
    unittest.main()
