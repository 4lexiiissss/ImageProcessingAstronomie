# ImageProcessingAstronomie

Membres: 
- Alexis Demol TPD
- Lucas Debruyne TPC 

## Description du Projet:
Ce projet vise à combiner des images spectrales obtenues à partir de différents télescopes spatiaux pour analyser et visualiser des objets célestes. À travers l'utilisation de bibliothèques Python comme Astropy, numpy et des données fournies par des services tels que SkyView, nous extrayons et traitons des images dans diverses bandes spectrales (visible, infrarouge, etc.) pour créer des représentations RGB complètes. C'est donc une interface graphique compléte avec le téléchargement de données selon les choix de l'utilisateur et des couleurs RGB avec l'utilisateur des curseurs et le chargement de 3 images FIT directement en local. Pour cette interface nous avons respecté le modèle MVC (Modèle vue controller) qui est très important pour une interface graphique. 

## Fonctionnalités:
- Téléchargement automatisé des données d'observation spatiale en fonction d'une position cible (ex. : une galaxie comme M31 ou des coordonnées).
- Support pour plusieurs missions/surveys : SDSS, WISE, DSS, etc.
- Génération et combinaison d'images RGB à partir des bandes rouge, verte et bleue.
- Stockage des images générées dans un dossier local spécifié par l'utilisateur.

## Technologies utilisées
- Python
- astroquery pour la récupération des données depuis SkyView.
- matplotlib et astropy pour la manipulation et l'affichage des images.
- Données astronomiques via SkyView (https://skyview.gsfc.nasa.gov/).

## Prérequis: 
- Installer Python 
- Installer PyQt6 (pip install PyQt6)
- Installer les différences bibliothèques requises pour lancer le projet (pip install astroquery astropy numpy)

## Comment exécuter le projet
Clonez ce dépôt sur votre machine locale :
```bash
git clone https://github.com/4lexiiissss/ImageProcessingAstronomie  
cd <nom_du_répertoire>
```
 
Lancez le script principal :
```bash
python3 main.py
````
Pour charger les images en local il y a juste a cliquer sur le bouton sur la gauche et choisir les 3 fichiers FIT avec les différents canaux.
Pour ajuster la couleur de cette image, il faut juste jouer avec les curseurs et enfin appliquer les changements. 
Enfin pour les téléchargements suivez les instructions affichées pour entrer la position cible, le nom de la mission et le dossier de destination des fichiers téléchargés.
