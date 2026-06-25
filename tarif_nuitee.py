# tarif_nuitee.py - À COMPLÉTER
#
# Ce fichier contient l'objet-valeur TarifNuitee : un montant associé à
# une devise (par exemple 85.50 EUR).
#
# La différence avec un hébergement est importante :
#   - un hébergement a une IDENTITÉ (son code) : deux hébergements de même
#     code sont « le même » ;
#   - un tarif est un OBJET-VALEUR : ce qui compte est sa VALEUR. Deux
#     tarifs de même montant et même devise sont égaux, point.
#
# Comme les nombres, un tarif a un ordre naturel : on peut dire qu'un
# tarif est « plus petit » qu'un autre. Le décorateur @total_ordering
# (déjà placé) fabrique <=, >, >= automatiquement à partir de __eq__ et
# __lt__ : vous n'avez donc que ces deux comparaisons à écrire.
#
# Comme toujours, les tests (test_tarif_nuitee.py) font foi.

from functools import total_ordering


@total_ordering
class TarifNuitee:
    """Un montant par nuitée, dans une devise donnée. Objet-valeur immuable."""

    def __init__(self, montant, devise="EUR"):
        # Valider puis ranger le montant et la devise.
        #   - montant : un nombre (entier ou réel, mais PAS un booléen) ;
        #     mauvais type -> TypeError. Il doit être positif ou nul ;
        #     une valeur négative -> ValueError. Le ranger sous forme de
        #     nombre réel (float).
        #   - devise : la chaîne de la devise (valeur par défaut "EUR").
        if not isinstance(montant, (int, float)) or isinstance(montant, bool):
            raise TypeError("le montant doit être un nombre")
        if montant < 0:
            raise ValueError("le montant doit être un nombre positif ou nul")
        self._montant = float(montant)
        self._devise = devise

    @property
    def montant(self):
        return self._montant

    @property
    def devise(self):
        return self._devise

    def __eq__(self, autre):
        # Deux tarifs sont égaux s'ils ont le MÊME montant ET la MÊME
        # devise. Si « autre » n'est pas un TarifNuitee, renvoyer
        # NotImplemented.
        if not isinstance(autre, TarifNuitee):
            return NotImplemented
        return self.montant == autre.montant and self.devise == autre.devise

    def __hash__(self):
        # Cohérent avec __eq__ : fondé sur le couple (montant, devise).
        return hash((self.montant, self.devise))

    def __lt__(self, autre):
        # Comparer deux tarifs (« plus petit que »). La comparaison n'a de
        # sens qu'entre MÊMES devises : si les devises diffèrent, lever
        # ValueError. Si « autre » n'est pas un TarifNuitee, renvoyer
        # NotImplemented.
        if not isinstance(autre, TarifNuitee):
            return NotImplemented
        if self.devise != autre.devise:
            raise ValueError("devises différentes")
        return self.montant < autre.montant

    def __add__(self, autre):
        # Additionner deux tarifs de MÊME devise et renvoyer un NOUVEAU
        # TarifNuitee (sans modifier les deux opérandes). Devises
        # différentes -> ValueError. Si « autre » n'est pas un TarifNuitee,
        # renvoyer NotImplemented (additionner un tarif et un simple nombre
        # doit échouer, pas réussir en silence).
        if not isinstance(autre, TarifNuitee):
            return NotImplemented
        if self.devise != autre.devise:
            raise ValueError("devises différentes")
        return TarifNuitee(self.montant + autre.montant, self.devise)

    def __str__(self):
        # Texte lisible, par exemple « 85.50 EUR » (deux décimales).
        # Format exact donné par les tests.
        return f"{self.montant:.2f} {self.devise}"

    def __repr__(self):
        # Texte reconstructible, par exemple TarifNuitee(85.5, 'EUR').
        return f"TarifNuitee({self.montant}, '{self.devise}')"
