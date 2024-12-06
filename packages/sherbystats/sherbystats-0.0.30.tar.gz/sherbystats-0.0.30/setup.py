import setuptools


setuptools.setup(
    name="sherbystats",
    version="0.0.30",
    author="Ryan Gosselin",
    author_email="ryan.gosselin@usherbrooke.ca",
    url="https://www.usherbrooke.ca/gchimiquebiotech/departement/professeurs/ryan-gosselin/",
    packages=["sherbystats"],
    description="Ryan @ UdeS",
    long_description="\
    \n\
    \n\
    \nGCB140. STATISTIQUES EN INGÉNIERIE\
    \nanova:        Analyse de variance\
    \ndoe:          Plans d'expérience 2k et 2k-p\
    \nmlr:          Régression linéaire\
    \nxlsread:      Lire document Excel\
    \n\
    \n\
    \nGCH755. Apprentissage machine données multivariées\
    \ncolorspectra\
    \ndtw\
    \ndtw_multi\
    \nlags\
    \nlda\
    \nmlr\
    \nnormplot\
    \npca\
    \npca_trou\
    \npcr\
    \npls\
    \nvif\
    \nvip\
    \nxlsread\
    \n\
    \n\
    \nGCH757. Planification et analyse des expériences\
    \nanova\
    \nbinaire\
    \nbinaire3D\
    \ndoe\
    \nmlr\
    \nternaire\
    \nxlsread\
    \n\
    \n",
    long_description_content_type="text/markdown",
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)