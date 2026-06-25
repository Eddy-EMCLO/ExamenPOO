"""Batterie de référence - hiérarchie Hebergement (épreuve centrale).

Spécification exécutable AUTOPORTANTE : tout ce qui est attendu est
testé ici, y compris les types d'exceptions, les bornes hautes ET
basses, le rejet du booléen, et les représentations de TOUTES les
classes. Aucun attendu n'est laissé implicite.

Programmation Orientée Objet - EICPN 2025-2026.
"""

import unittest

from hebergement import Hebergement, Gite, EmplacementCamping

CODE = "RESA1234567890ABC"
CODE2 = "GITE000000000ABCD"
CODE3 = "CAMP000000000WXYZ"


class TestCodeValide(unittest.TestCase):
    """Validation statique du code de réservation."""

    def test_code_valide_accepte_17_alphanum(self):
        self.assertTrue(Hebergement.code_valide("ABC4567890123DEFG"))

    def test_code_valide_refuse_trop_court(self):
        self.assertFalse(Hebergement.code_valide("ABC123"))

    def test_code_valide_refuse_trop_long(self):
        self.assertFalse(Hebergement.code_valide("A" * 18))

    def test_code_valide_refuse_non_alphanumerique(self):
        self.assertFalse(Hebergement.code_valide("RESA-234567890ABC"))

    def test_code_valide_refuse_non_str(self):
        self.assertFalse(Hebergement.code_valide(12345678901234567))


class TestHebergementConstruction(unittest.TestCase):
    """Construction nominale et lecture des attributs."""

    def test_construction_nominale(self):
        h = Hebergement("Villa Soleil", "Durbuy", CODE, 6, 2005)
        self.assertEqual(h.nom, "Villa Soleil")
        self.assertEqual(h.localite, "Durbuy")
        self.assertEqual(h.code_reservation, CODE)
        self.assertEqual(h.capacite_personnes, 6)
        self.assertEqual(h.annee_construction, 2005)

    def test_neuf_est_libre(self):
        h = Hebergement("Villa Soleil", "Durbuy", CODE, 6, 2005)
        self.assertTrue(h.libre)

    def test_attributs_en_lecture_seule(self):
        h = Hebergement("Villa Soleil", "Durbuy", CODE, 6, 2005)
        with self.assertRaises(AttributeError):
            h.nom = "Autre"
        with self.assertRaises(AttributeError):
            h.capacite_personnes = 8


class TestHebergementValidationTypes(unittest.TestCase):
    """Distinction stricte TypeError (type) / ValueError (valeur)."""

    def test_nom_non_str_leve_TypeError(self):
        with self.assertRaises(TypeError):
            Hebergement(123, "Durbuy", CODE, 6, 2005)

    def test_nom_vide_leve_ValueError(self):
        with self.assertRaises(ValueError):
            Hebergement("   ", "Durbuy", CODE, 6, 2005)

    def test_localite_non_str_leve_TypeError(self):
        with self.assertRaises(TypeError):
            Hebergement("Villa", 456, CODE, 6, 2005)

    def test_localite_vide_leve_ValueError(self):
        with self.assertRaises(ValueError):
            Hebergement("Villa", "", CODE, 6, 2005)

    def test_code_invalide_leve_ValueError(self):
        with self.assertRaises(ValueError):
            Hebergement("Villa", "Durbuy", "TROP_COURT", 6, 2005)

    def test_capacite_non_int_leve_TypeError(self):
        with self.assertRaises(TypeError):
            Hebergement("Villa", "Durbuy", CODE, 6.0, 2005)

    def test_capacite_booleen_leve_TypeError(self):
        with self.assertRaises(TypeError):
            Hebergement("Villa", "Durbuy", CODE, True, 2005)

    def test_capacite_zero_leve_ValueError(self):
        with self.assertRaises(ValueError):
            Hebergement("Villa", "Durbuy", CODE, 0, 2005)

    def test_capacite_au_dessus_borne_leve_ValueError(self):
        with self.assertRaises(ValueError):
            Hebergement("Villa", "Durbuy", CODE, 51, 2005)

    def test_capacite_borne_haute_acceptee(self):
        h = Hebergement("Villa", "Durbuy", CODE, 50, 2005)
        self.assertEqual(h.capacite_personnes, 50)

    def test_annee_non_int_leve_TypeError(self):
        with self.assertRaises(TypeError):
            Hebergement("Villa", "Durbuy", CODE, 6, "2005")

    def test_annee_booleen_leve_TypeError(self):
        with self.assertRaises(TypeError):
            Hebergement("Villa", "Durbuy", CODE, 6, True)

    def test_annee_sous_borne_leve_ValueError(self):
        with self.assertRaises(ValueError):
            Hebergement("Villa", "Durbuy", CODE, 6, 1799)

    def test_annee_au_dessus_borne_leve_ValueError(self):
        with self.assertRaises(ValueError):
            Hebergement("Villa", "Durbuy", CODE, 6, 2027)

    def test_annee_bornes_acceptees(self):
        self.assertEqual(
            Hebergement("V", "D", CODE, 6, 1800).annee_construction, 1800)
        self.assertEqual(
            Hebergement("V", "D", CODE, 6, 2026).annee_construction, 2026)


class TestHebergementMetier(unittest.TestCase):
    """Cycle de vie libre / réservé."""

    def setUp(self):
        self.h = Hebergement("Villa Soleil", "Durbuy", CODE, 6, 2005)

    def test_reserver_rend_indisponible(self):
        self.h.reserver()
        self.assertFalse(self.h.libre)

    def test_reserver_deja_reserve_leve_ValueError(self):
        self.h.reserver()
        with self.assertRaises(ValueError):
            self.h.reserver()

    def test_liberer_rend_disponible(self):
        self.h.reserver()
        self.h.liberer()
        self.assertTrue(self.h.libre)

    def test_liberer_deja_libre_leve_ValueError(self):
        with self.assertRaises(ValueError):
            self.h.liberer()


class TestHebergementFicheResume(unittest.TestCase):
    """Format exact de fiche_resume."""

    def test_fiche_resume_hebergement(self):
        h = Hebergement("Villa Soleil", "Durbuy", CODE, 4, 2005)
        self.assertEqual(h.fiche_resume(), "4 personnes")


class TestHebergementDepuisCsv(unittest.TestCase):
    """Constructeur alternatif depuis_csv."""

    def test_depuis_csv_nominal(self):
        h = Hebergement.depuis_csv(f"Villa Soleil;Durbuy;{CODE};6;2005")
        self.assertIsInstance(h, Hebergement)
        self.assertEqual(h.capacite_personnes, 6)
        self.assertEqual(h.annee_construction, 2005)

    def test_depuis_csv_mauvais_nombre_de_champs(self):
        with self.assertRaises(ValueError):
            Hebergement.depuis_csv(f"Villa;Durbuy;{CODE};6")


class TestHebergementRepr(unittest.TestCase):
    """__str__ et __repr__ : présents et, pour repr, reconstructible."""

    def test_str_mentionne_etat(self):
        h = Hebergement("Villa Soleil", "Durbuy", CODE, 6, 2005)
        self.assertIn("libre", str(h))
        h.reserver()
        self.assertIn("réservé", str(h))

    def test_repr_reconstructible(self):
        h = Hebergement("Villa Soleil", "Durbuy", CODE, 6, 2005)
        reconstruit = eval(
            repr(h),
            {"Hebergement": Hebergement, "Gite": Gite,
             "EmplacementCamping": EmplacementCamping},
        )
        self.assertEqual(reconstruit, h)
        self.assertEqual(reconstruit.capacite_personnes, 6)


class TestHebergementIdentite(unittest.TestCase):
    """Égalité et hachage par code de réservation (entité)."""

    def test_egalite_par_code(self):
        h1 = Hebergement("Villa Soleil", "Durbuy", CODE, 6, 2005)
        h2 = Hebergement("Autre Nom", "Liège", CODE, 2, 1990)
        self.assertEqual(h1, h2)

    def test_inegalite_codes_differents(self):
        h1 = Hebergement("Villa Soleil", "Durbuy", CODE, 6, 2005)
        h2 = Hebergement("Villa Soleil", "Durbuy", CODE2, 6, 2005)
        self.assertNotEqual(h1, h2)

    def test_hash_par_code(self):
        h1 = Hebergement("Villa Soleil", "Durbuy", CODE, 6, 2005)
        h2 = Hebergement("Autre Nom", "Liège", CODE, 2, 1990)
        self.assertEqual(hash(h1), hash(h2))

    def test_eq_avec_autre_type_retourne_notimplemented(self):
        h = Hebergement("Villa Soleil", "Durbuy", CODE, 6, 2005)
        self.assertNotEqual(h, "une chaîne")


class TestGite(unittest.TestCase):
    """Sous-classe Gite : enrichissement."""

    def test_construction_nominale(self):
        g = Gite("Le Moulin", "Rochefort", CODE2, 4, 1890, 3)
        self.assertEqual(g.nombre_chambres, 3)
        self.assertEqual(g.capacite_personnes, 4)

    def test_est_un_hebergement(self):
        g = Gite("Le Moulin", "Rochefort", CODE2, 4, 1890, 3)
        self.assertIsInstance(g, Hebergement)

    def test_chambres_non_int_leve_TypeError(self):
        with self.assertRaises(TypeError):
            Gite("Le Moulin", "Rochefort", CODE2, 4, 1890, 3.0)

    def test_chambres_booleen_leve_TypeError(self):
        with self.assertRaises(TypeError):
            Gite("Le Moulin", "Rochefort", CODE2, 4, 1890, True)

    def test_chambres_zero_leve_ValueError(self):
        with self.assertRaises(ValueError):
            Gite("Le Moulin", "Rochefort", CODE2, 4, 1890, 0)

    def test_validation_heritee_appliquee(self):
        with self.assertRaises(ValueError):
            Gite("Le Moulin", "Rochefort", CODE2, 51, 1890, 3)

    def test_fiche_resume_enrichit(self):
        g = Gite("Le Moulin", "Rochefort", CODE2, 4, 1890, 3)
        self.assertEqual(
            g.fiche_resume(), "4 personnes [gîte, 3 chambres]")

    def test_repr_reconstructible(self):
        g = Gite("Le Moulin", "Rochefort", CODE2, 4, 1890, 3)
        reconstruit = eval(
            repr(g),
            {"Hebergement": Hebergement, "Gite": Gite,
             "EmplacementCamping": EmplacementCamping},
        )
        self.assertEqual(reconstruit, g)
        self.assertEqual(reconstruit.nombre_chambres, 3)

    def test_depuis_csv_donne_un_gite(self):
        g = Gite.depuis_csv(f"Le Moulin;Rochefort;{CODE2};4;1890;3")
        self.assertIsInstance(g, Gite)
        self.assertEqual(g.nombre_chambres, 3)

    def test_str_renvoie_une_chaine_mentionnant_etat(self):
        g = Gite("Le Moulin", "Rochefort", CODE2, 4, 1890, 3)
        self.assertIsInstance(str(g), str)
        self.assertIn("libre", str(g))


class TestEmplacementCamping(unittest.TestCase):
    """Sous-classe EmplacementCamping : remplacement."""

    def test_construction_nominale(self):
        e = EmplacementCamping("Pré Vert", "La Roche", CODE3, 4, 2015, 80.0)
        self.assertEqual(e.surface_m2, 80.0)

    def test_est_un_hebergement(self):
        e = EmplacementCamping("Pré Vert", "La Roche", CODE3, 4, 2015, 80.0)
        self.assertIsInstance(e, Hebergement)

    def test_surface_acceptee_en_int(self):
        e = EmplacementCamping("Pré Vert", "La Roche", CODE3, 4, 2015, 75)
        self.assertEqual(e.surface_m2, 75.0)
        self.assertIsInstance(e.surface_m2, float)

    def test_surface_non_nombre_leve_TypeError(self):
        with self.assertRaises(TypeError):
            EmplacementCamping("Pré Vert", "La Roche", CODE3, 4, 2015, "80")

    def test_surface_booleen_leve_TypeError(self):
        with self.assertRaises(TypeError):
            EmplacementCamping("Pré Vert", "La Roche", CODE3, 4, 2015, True)

    def test_surface_nulle_leve_ValueError(self):
        with self.assertRaises(ValueError):
            EmplacementCamping("Pré Vert", "La Roche", CODE3, 4, 2015, 0)

    def test_validation_heritee_appliquee(self):
        with self.assertRaises(ValueError):
            EmplacementCamping("Pré Vert", "La Roche", CODE3, 4, 1799, 80.0)

    def test_fiche_resume_remplace(self):
        e = EmplacementCamping("Pré Vert", "La Roche", CODE3, 4, 2015, 80.0)
        self.assertEqual(e.fiche_resume(), "80.0 m² d'emplacement")

    def test_fiche_resume_ne_mentionne_pas_personnes(self):
        e = EmplacementCamping("Pré Vert", "La Roche", CODE3, 4, 2015, 80.0)
        self.assertNotIn("personnes", e.fiche_resume())

    def test_repr_reconstructible(self):
        e = EmplacementCamping("Pré Vert", "La Roche", CODE3, 4, 2015, 80.0)
        reconstruit = eval(
            repr(e),
            {"Hebergement": Hebergement, "Gite": Gite,
             "EmplacementCamping": EmplacementCamping},
        )
        self.assertEqual(reconstruit, e)
        self.assertEqual(reconstruit.surface_m2, 80.0)

    def test_depuis_csv_donne_un_emplacement(self):
        e = EmplacementCamping.depuis_csv(
            f"Pré Vert;La Roche;{CODE3};4;2015;80.0")
        self.assertIsInstance(e, EmplacementCamping)
        self.assertEqual(e.surface_m2, 80.0)

    def test_str_renvoie_une_chaine_mentionnant_etat(self):
        e = EmplacementCamping("Pré Vert", "La Roche", CODE3, 4, 2015, 80.0)
        self.assertIsInstance(str(e), str)
        self.assertIn("libre", str(e))


if __name__ == "__main__":
    unittest.main()
