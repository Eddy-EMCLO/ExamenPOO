# hebergement.py - À COMPLÉTER
#
# Ce fichier contient la hiérarchie d'hébergements de la centrale de
# réservation : la classe de base Hebergement et ses deux sous-classes
# Gite et EmplacementCamping.
#
# Votre travail : remplacer chaque « ... » par le code attendu. La forme
# des classes (noms, signatures, propriétés) est déjà posée pour vous ;
# il vous reste à écrire l'intérieur des méthodes.
#
# RÈGLE D'OR : les fichiers test_*.py décrivent EXACTEMENT ce qui est
# attendu (valeurs de retour, bornes, types d'erreurs, formats de texte).
# Ils sont la référence. En cas de doute, lisez le test correspondant et
# lancez « python verifier.py » pour voir où vous en êtes.


class Hebergement:
    """Un hébergement de la centrale de réservation.

    Un hébergement est identifié de façon unique par son CODE DE
    RÉSERVATION (deux hébergements de même code sont considérés comme le
    même hébergement, même si leur nom diffère). Ses caractéristiques
    sont fixées une fois pour toutes à la création ; seul l'état
    « libre / réservé » change ensuite.
    """

    def __init__(self, nom, localite, code_reservation, capacite_personnes,
                 annee_construction):
        # Vérifier chaque information reçue AVANT de la ranger dans l'objet.
        #
        # Deux familles d'erreurs à distinguer :
        #   - mauvais TYPE  -> lever TypeError
        #     (exemple : une capacité donnée sous forme de texte) ;
        #   - bon type mais mauvaise VALEUR -> lever ValueError
        #     (exemple : une capacité égale à 0).
        #
        # À contrôler, dans l'ordre :
        #   - nom et localite : des chaînes de caractères, non vides ;
        #   - code_reservation : valide au sens de code_valide (plus bas) ;
        #     si le code n'est pas valide, lever ValueError ;
        #   - capacite_personnes : un entier (PAS un booléen) dans les
        #     bornes indiquées par l'énoncé et les tests ;
        #   - annee_construction : un entier (PAS un booléen) dans les
        #     bornes indiquées par l'énoncé et les tests.
        #
        # Astuce : en Python, True et False sont aussi des entiers. Il faut
        # donc les refuser explicitement là où on attend un « vrai » entier.
        #
        # Une fois TOUTES les vérifications passées : ranger chaque valeur
        # dans un attribut privé (préfixe « _ ») et marquer l'hébergement
        # comme libre.
        ...

    # ------------------------------------------------------------------
    # Propriétés en lecture seule
    # ------------------------------------------------------------------
    # Chaque propriété donne accès EN LECTURE à l'attribut privé
    # correspondant. Aucune ne permet de modifier l'objet (pas de setter) :
    # un hébergement est immuable, sauf pour son état libre / réservé.

    @property
    def nom(self):
        ...

    @property
    def localite(self):
        ...

    @property
    def code_reservation(self):
        ...

    @property
    def capacite_personnes(self):
        ...

    @property
    def annee_construction(self):
        ...

    @property
    def libre(self):
        ...

    # ------------------------------------------------------------------
    # Méthode statique
    # ------------------------------------------------------------------

    @staticmethod
    def code_valide(chaine):
        # Renvoyer True si « chaine » est un code de réservation valide,
        # False sinon. Un code valide est une chaîne de caractères d'une
        # longueur précise, composée uniquement de lettres et de chiffres.
        # La longueur exacte et la nature des caractères sont fixées par
        # les tests. Une valeur qui n'est même pas une chaîne renvoie False
        # (et ne lève pas d'erreur).
        ...

    # ------------------------------------------------------------------
    # Constructeur alternatif
    # ------------------------------------------------------------------

    @classmethod
    def depuis_csv(cls, ligne):
        # Construire un hébergement à partir d'une ligne de texte dont les
        # champs sont séparés par des points-virgules « ; ».
        # Vérifier d'abord que le nombre de champs est correct (sinon
        # ValueError), puis appeler le constructeur.
        #
        # Important : utiliser cls(...) et NON Hebergement(...). C'est ce
        # qui permettra aux sous-classes (Gite, EmplacementCamping) de
        # réutiliser cette logique en créant le bon type.
        ...

    # ------------------------------------------------------------------
    # Sérialisation (transformation en dictionnaire)
    # ------------------------------------------------------------------

    def to_dict(self):
        # Renvoyer un dictionnaire décrivant l'hébergement, prêt à être
        # enregistré en JSON. Ce dictionnaire contient un champ "type" qui
        # mémorise le nom de la classe : il servira plus tard à recréer le
        # bon type d'objet. Les noms exacts des clés sont donnés par les
        # tests.
        ...

    @classmethod
    def from_dict(cls, donnees):
        # Opération inverse de to_dict : recréer un hébergement à partir
        # d'un dictionnaire. Construire l'objet via cls(...), puis
        # restaurer son état libre / réservé.
        #
        # Pour restaurer l'état, passer par la MÉTHODE prévue (voir
        # _restaurer_etat), jamais en modifiant directement l'attribut
        # privé.
        ...

    @staticmethod
    def _restaurer_etat(hebergement, donnees):
        # Si le dictionnaire indique que l'hébergement était réservé, le
        # replacer dans cet état EN APPELANT la méthode métier prévue à cet
        # effet (et non en écrivant l'attribut privé « à la main »).
        # Cette aide est commune à toutes les sous-classes.
        ...

    # ------------------------------------------------------------------
    # Méthodes métier (changement d'état)
    # ------------------------------------------------------------------

    def reserver(self):
        # Faire passer l'hébergement de « libre » à « réservé ».
        # S'il est déjà réservé, lever ValueError.
        ...

    def liberer(self):
        # Faire passer l'hébergement de « réservé » à « libre ».
        # S'il est déjà libre, lever ValueError.
        ...

    def fiche_resume(self):
        # Renvoyer une courte description de la CAPACITÉ d'accueil.
        # Pour un hébergement générique, l'unité naturelle est la personne.
        # Le format exact est donné par les tests (voir l'énoncé pour un
        # exemple).
        ...

    # ------------------------------------------------------------------
    # Représentations textuelles
    # ------------------------------------------------------------------

    def __str__(self):
        # Texte lisible par un humain, qui mentionne notamment l'état
        # actuel (libre ou réservé). Format précisé par les tests/énoncé.
        ...

    def __repr__(self):
        # Texte « technique » qui, recopié tel quel dans du code Python,
        # permettrait de reconstruire un hébergement équivalent. Format
        # précisé par les tests (il est vérifié qu'il est reconstructible).
        ...

    # ------------------------------------------------------------------
    # Identité (égalité et hachage)
    # ------------------------------------------------------------------

    def __eq__(self, autre):
        # Deux hébergements sont égaux s'ils ont le MÊME code de
        # réservation. Si « autre » n'est pas un Hebergement, renvoyer
        # NotImplemented (et non False) pour laisser Python gérer le cas.
        ...

    def __hash__(self):
        # Doit être cohérent avec __eq__ : fondé sur le code de réservation.
        # (Nécessaire pour utiliser un hébergement dans un set ou comme clé
        # de dictionnaire.)
        ...


class Gite(Hebergement):
    """Un gîte : un hébergement AVEC, en plus, un nombre de chambres.

    Un gîte est un hébergement comme un autre, auquel on AJOUTE une
    information (le nombre de chambres). On parle d'ENRICHISSEMENT : le
    gîte réutilise tout ce que fait Hebergement, et y ajoute sa part.
    """

    def __init__(self, nom, localite, code_reservation, capacite_personnes,
                 annee_construction, nombre_chambres):
        # 1) Laisser la classe parente valider et ranger les attributs
        #    communs (utiliser super()).
        # 2) Valider ensuite l'attribut PROPRE au gîte : nombre_chambres
        #    doit être un entier (PAS un booléen) strictement positif.
        #    Mauvais type -> TypeError ; mauvaise valeur -> ValueError.
        # 3) Ranger nombre_chambres dans un attribut privé.
        ...

    @property
    def nombre_chambres(self):
        ...

    @classmethod
    def depuis_csv(cls, ligne):
        # Comme Hebergement.depuis_csv, mais avec un champ de plus
        # (le nombre de chambres). Adapter le nombre de champs attendu.
        ...

    def to_dict(self):
        # ENRICHIR le dictionnaire du parent au lieu de tout réécrire :
        #   - récupérer le dictionnaire de base via super() ;
        #   - corriger le champ "type" ;
        #   - y ajouter le nombre de chambres.
        ...

    @classmethod
    def from_dict(cls, donnees):
        # Recréer un gîte à partir d'un dictionnaire, puis restaurer son
        # état (même principe que pour Hebergement.from_dict).
        ...

    def fiche_resume(self):
        # ENRICHISSEMENT : on REPREND la fiche de base (la capacité reste
        # pertinente pour un gîte) et on la complète avec le nombre de
        # chambres. Réutiliser le travail du parent via super(). Format
        # exact donné par les tests / l'énoncé.
        ...

    def __str__(self):
        # Reprendre le texte du parent et le compléter. Format donné par
        # les tests / l'énoncé.
        ...

    def __repr__(self):
        # Comme pour Hebergement, mais en incluant le nombre de chambres.
        # Doit rester reconstructible.
        ...


class EmplacementCamping(Hebergement):
    """Un emplacement de camping : la bonne mesure est la SURFACE.

    Sur un emplacement nu, le client installe sa propre tente ou sa
    caravane : compter des « couchages » n'a plus de sens. La capacité de
    base n'est donc plus la mesure naturelle ; on la REMPLACE par la
    surface (en m²). C'est la différence avec le gîte : ici, fiche_resume
    ne réutilise PAS la fiche de base, elle la remplace.
    """

    def __init__(self, nom, localite, code_reservation, capacite_personnes,
                 annee_construction, surface_m2):
        # 1) Laisser la classe parente valider et ranger les attributs
        #    communs (super()).
        # 2) Valider l'attribut PROPRE : surface_m2 doit être un nombre
        #    (entier ou réel, mais PAS un booléen) strictement positif.
        #    Mauvais type -> TypeError ; mauvaise valeur -> ValueError.
        # 3) Ranger la surface dans un attribut privé, sous forme de
        #    nombre réel (float).
        ...

    @property
    def surface_m2(self):
        ...

    @classmethod
    def depuis_csv(cls, ligne):
        # Comme Hebergement.depuis_csv, mais avec un champ de plus
        # (la surface). Adapter le nombre de champs attendu.
        ...

    def to_dict(self):
        # ENRICHIR le dictionnaire du parent : récupérer la base via
        # super(), corriger "type", ajouter la surface.
        ...

    @classmethod
    def from_dict(cls, donnees):
        # Recréer un emplacement à partir d'un dictionnaire, puis restaurer
        # son état.
        ...

    def fiche_resume(self):
        # REMPLACEMENT : ici on N'UTILISE PAS la fiche de base. On décrit
        # la surface de l'emplacement. Format exact donné par les tests /
        # l'énoncé (attention au nombre de décimales).
        ...

    def __str__(self):
        # Reprendre le texte du parent et le compléter avec la description
        # de l'emplacement. Format donné par les tests / l'énoncé.
        ...

    def __repr__(self):
        # Comme pour Hebergement, mais en incluant la surface. Doit rester
        # reconstructible.
        ...
