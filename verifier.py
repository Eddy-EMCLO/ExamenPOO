#!/usr/bin/env python3
# verifier.py - lance tous les tests et affiche un récapitulatif lisible.
#
# Utilisation, dans un terminal ouvert dans ce dossier :
#
#     python verifier.py
#
# Ce script ne fait rien de magique : il lance exactement les mêmes tests
# que « python -m unittest », mais il regroupe le résultat par fichier et
# affiche un petit bilan à la fin. Lancez-le aussi souvent que vous le
# souhaitez pendant que vous complétez les fichiers.

import unittest


MODULES_DE_TEST = [
    "test_hebergement",
    "test_tarif_nuitee",
    "test_centrale",
    "test_persistance",
]


def lancer_un_module(nom_module):
    """Lance un module de test et renvoie (réussis, total)."""
    suite = unittest.defaultTestLoader.loadTestsFromName(nom_module)
    resultat = unittest.TestResult()
    suite.run(resultat)
    total = resultat.testsRun
    echoues = len(resultat.failures) + len(resultat.errors)
    return total - echoues, total, resultat


def main():
    print("=" * 60)
    print("  Vérification de votre travail")
    print("=" * 60)

    total_ok = 0
    total_tests = 0
    details = []

    for nom in MODULES_DE_TEST:
        try:
            ok, total, resultat = lancer_un_module(nom)
        except Exception as erreur:  # noqa: BLE001
            print(f"\n  {nom:<22} : IMPOSSIBLE À CHARGER")
            print(f"     -> {type(erreur).__name__}: {erreur}")
            continue

        total_ok += ok
        total_tests += total
        etat = "OK" if ok == total else f"{total - ok} à corriger"
        print(f"\n  {nom:<22} : {ok}/{total} réussis   ({etat})")

        for cas, _trace in list(resultat.failures) + list(resultat.errors):
            details.append(str(cas))

    print("\n" + "=" * 60)
    print(f"  TOTAL : {total_ok}/{total_tests} tests réussis")
    print("=" * 60)

    if details:
        print("\n  Tests encore à faire passer :")
        for nom_cas in details:
            print(f"    - {nom_cas}")
        print(
            "\n  Conseil : ouvrez le fichier de test correspondant pour "
            "voir\n  exactement ce qui est attendu, puis relancez "
            "« python verifier.py »."
        )
    else:
        print("\n  Bravo, tout est au vert !")


if __name__ == "__main__":
    main()
