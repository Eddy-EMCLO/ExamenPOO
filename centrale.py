# centrale.py - À COMPLÉTER
#
# Ce fichier contient la CentraleReservation : une « boîte » qui contient
# des hébergements et sait répondre à des questions comme « combien
# d'hébergements ? », « cet hébergement est-il présent ? », « lesquels
# sont libres ? ».
#
# Le but est de rendre cette boîte utilisable avec les outils naturels de
# Python :
#   - len(centrale)            -> nombre d'hébergements   (__len__)
#   - x in centrale            -> test de présence        (__contains__)
#   - for h in centrale: ...   -> parcours                (__iter__)
#
# Les hébergements peuvent être de n'importe quel type de la hiérarchie
# (Hebergement, Gite, EmplacementCamping) : votre code ne doit PAS tester
# le type avec isinstance pour les ranger ou les parcourir. Il les traite
# tous de la même manière.
#
# Les tests (test_centrale.py) font foi.

from hebergement import Hebergement


class CentraleReservation:
    """Contient des hébergements, dans leur ordre d'ajout, sans doublon."""

    def __init__(self):
        # Préparer la collection interne qui gardera les hébergements dans
        # l'ordre où on les ajoute.
        ...

    # ------------------------------------------------------------------
    # Ajouter / retirer
    # ------------------------------------------------------------------

    def ajouter(self, hebergement):
        # Ajouter un hébergement à la centrale.
        #   - refuser ce qui n'est pas un Hebergement -> TypeError ;
        #   - refuser un doublon, c.-à-d. un hébergement de même code déjà
        #     présent -> ValueError.
        # Astuce : « déjà présent ? » se teste élégamment avec
        # « hebergement in self » (une fois __contains__ écrit).
        ...

    def retirer(self, hebergement):
        # Retirer un hébergement de la centrale.
        #   - refuser ce qui n'est pas un Hebergement -> TypeError ;
        #   - si l'hébergement n'est pas présent -> KeyError.
        ...

    # ------------------------------------------------------------------
    # Protocole de conteneur
    # ------------------------------------------------------------------

    def __len__(self):
        # Nombre d'hébergements actuellement dans la centrale.
        ...

    def __contains__(self, item):
        # Indiquer si « item » est présent. « item » peut être :
        #   - un Hebergement (comparé par code grâce à __eq__) ;
        #   - une chaîne de caractères (interprétée comme un code) ;
        #   - toute autre chose -> renvoyer False (sans lever d'erreur).
        ...

    def __iter__(self):
        # Permettre « for h in centrale: ... » dans l'ordre d'ajout.
        ...

    # ------------------------------------------------------------------
    # Méthodes métier
    # ------------------------------------------------------------------

    def trouver_par_code(self, code_reservation):
        # Renvoyer l'hébergement portant ce code. Si aucun ne correspond,
        # lever KeyError.
        ...

    def hebergements_libres(self):
        # Renvoyer la liste des hébergements actuellement libres, dans
        # l'ordre d'ajout.
        ...

    @property
    def nombre_libres(self):
        # Nombre d'hébergements actuellement libres.
        ...

    # ------------------------------------------------------------------
    # Représentation
    # ------------------------------------------------------------------

    def __repr__(self):
        # Texte court résumant la centrale (par exemple son nombre total
        # d'hébergements et son nombre de libres).
        ...
