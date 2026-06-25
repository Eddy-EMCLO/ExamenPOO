"""Batterie de référence - persistance de la centrale (épreuve centrale).

Spécification exécutable autoportante : fabrique pilotée par registre
(type absent ou inconnu -> ValueError), round-trip JSON conservant le
type exact ET l'état libre / réservé, dispatch polymorphe sans isinstance.

Programmation Orientée Objet - EICPN 2025-2026.
"""

import json
import os
import tempfile
import unittest

from hebergement import Hebergement, Gite, EmplacementCamping
from persistance import (
    hebergement_depuis_dict,
    sauvegarder_centrale_json,
    charger_centrale_json,
)

CODE = "RESA1234567890ABC"
CODE2 = "GITE000000000ABCD"
CODE3 = "CAMP000000000WXYZ"


class TestFabrique(unittest.TestCase):

    def test_reconstruit_hebergement(self):
        h = Hebergement("Villa", "Durbuy", CODE, 6, 2005)
        reconstruit = hebergement_depuis_dict(h.to_dict())
        self.assertIsInstance(reconstruit, Hebergement)
        self.assertEqual(reconstruit, h)

    def test_reconstruit_gite(self):
        g = Gite("Moulin", "Rochefort", CODE2, 4, 1890, 3)
        reconstruit = hebergement_depuis_dict(g.to_dict())
        self.assertIsInstance(reconstruit, Gite)
        self.assertEqual(reconstruit.nombre_chambres, 3)

    def test_reconstruit_emplacement(self):
        e = EmplacementCamping("Pré", "La Roche", CODE3, 4, 2015, 80.0)
        reconstruit = hebergement_depuis_dict(e.to_dict())
        self.assertIsInstance(reconstruit, EmplacementCamping)
        self.assertEqual(reconstruit.surface_m2, 80.0)

    def test_type_absent_leve_ValueError(self):
        with self.assertRaises(ValueError):
            hebergement_depuis_dict({"nom": "Villa"})

    def test_type_inconnu_leve_ValueError(self):
        with self.assertRaises(ValueError):
            hebergement_depuis_dict({"type": "Chateau"})


class TestToDict(unittest.TestCase):

    def test_to_dict_hebergement_porte_le_type(self):
        h = Hebergement("Villa", "Durbuy", CODE, 6, 2005)
        self.assertEqual(h.to_dict()["type"], "Hebergement")

    def test_to_dict_gite_enrichit(self):
        g = Gite("Moulin", "Rochefort", CODE2, 4, 1890, 3)
        donnees = g.to_dict()
        self.assertEqual(donnees["type"], "Gite")
        self.assertEqual(donnees["nombre_chambres"], 3)
        self.assertEqual(donnees["capacite_personnes"], 4)

    def test_to_dict_emplacement_enrichit(self):
        e = EmplacementCamping("Pré", "La Roche", CODE3, 4, 2015, 80.0)
        donnees = e.to_dict()
        self.assertEqual(donnees["type"], "EmplacementCamping")
        self.assertEqual(donnees["surface_m2"], 80.0)


class TestRoundTripJson(unittest.TestCase):

    def setUp(self):
        self.dossier = tempfile.mkdtemp()
        self.chemin = os.path.join(self.dossier, "centrale.json")

    def test_round_trip_conserve_types_et_valeurs(self):
        centrale = [
            Hebergement("Villa", "Durbuy", CODE, 6, 2005),
            Gite("Moulin", "Rochefort", CODE2, 4, 1890, 3),
            EmplacementCamping("Pré", "La Roche", CODE3, 4, 2015, 80.0),
        ]
        sauvegarder_centrale_json(centrale, self.chemin)
        recharge = charger_centrale_json(self.chemin)

        self.assertEqual([type(h).__name__ for h in recharge],
                         ["Hebergement", "Gite", "EmplacementCamping"])
        self.assertEqual(recharge[1].nombre_chambres, 3)
        self.assertEqual(recharge[2].surface_m2, 80.0)

    def test_round_trip_conserve_etat_reserve(self):
        h = Hebergement("Villa", "Durbuy", CODE, 6, 2005)
        h.reserver()
        sauvegarder_centrale_json([h], self.chemin)
        recharge = charger_centrale_json(self.chemin)
        self.assertFalse(recharge[0].libre)

    def test_fichier_est_du_json_valide(self):
        sauvegarder_centrale_json(
            [Hebergement("Villa", "Durbuy", CODE, 6, 2005)], self.chemin)
        with open(self.chemin, encoding="utf-8") as fichier:
            donnees = json.load(fichier)
        self.assertEqual(donnees[0]["type"], "Hebergement")


if __name__ == "__main__":
    unittest.main()
