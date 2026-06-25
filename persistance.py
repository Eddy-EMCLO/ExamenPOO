# persistance.py - À COMPLÉTER
#
# Ce fichier sait ENREGISTRER une centrale dans un fichier JSON et la
# RELIRE plus tard. Le point délicat : quand on relit le fichier, chaque
# hébergement doit retrouver son TYPE EXACT d'origine (un Gite redevient
# un Gite, un EmplacementCamping redevient un EmplacementCamping).
#
# Pour cela, on s'appuie sur le champ "type" écrit par to_dict, et sur un
# REGISTRE qui associe chaque nom de type à sa classe. Ajouter un nouveau
# type d'hébergement demain ne demandera qu'une ligne dans ce registre,
# sans rien changer d'autre.
#
# Remarque : c'est ICI qu'on importe json et qu'on touche aux fichiers.
# Le fichier hebergement.py, lui, ne s'occupe JAMAIS de fichiers ni de
# JSON : chaque fichier a son rôle.
#
# Les tests (test_persistance.py) font foi.

import json

from hebergement import Hebergement, Gite, EmplacementCamping


# Registre « nom de type -> classe ».
# À COMPLÉTER : associez chaque valeur possible du champ "type" à la
# classe correspondante.
_FABRIQUES = {
    "Hebergement": Hebergement,
    "Gite": Gite,
    "EmplacementCamping": EmplacementCamping,
}


def hebergement_depuis_dict(donnees):
    # À partir d'un dictionnaire (issu de to_dict), recréer le bon type
    # d'hébergement :
    #   - lire le champ "type" ;
    #   - si ce type est absent ou inconnu du registre -> ValueError ;
    #   - sinon, déléguer la reconstruction à la méthode from_dict de la
    #     classe trouvée dans le registre.
    type = donnees.get("type")
    if type not in _FABRIQUES:
        raise ValueError(f"type inconnu : {type}")
    classe = _FABRIQUES[type]
    return classe.from_dict(donnees)


# ----------------------------------------------------------------------
# Enregistrement et lecture au format JSON
# ----------------------------------------------------------------------

def sauvegarder_centrale_json(hebergements, chemin):
    # Transformer chaque hébergement en dictionnaire (chacun sait le faire
    # via to_dict, sans qu'on ait à tester son type), puis écrire la liste
    # obtenue dans le fichier « chemin » au format JSON.
    data = [h.to_dict() for h in hebergements]
    with open(chemin , "w")  as f :
        json.dump(data, f)


def charger_centrale_json(chemin):
    # Lire le fichier JSON « chemin », puis reconstruire chaque hébergement
    # avec hebergement_depuis_dict. Renvoyer la liste des hébergements,
    # chacun ayant retrouvé son type exact d'origine.
    with open(chemin , "r") as f :
        data =  json.load(f)
    return [hebergement_depuis_dict(h) for h in data]