# Simulateur de type LIDAR

---

## Utilisation

1. Lancer le programme :

    1.1. Pour lancer le programme, lancer le script `main.py`.


2. Lancer la simulation :

   2.1. Choisissez votre map avec le bouton `Choix de la map`, deux maps sont disponibles dans le dossier, une fois choisie une nouvelle map sera crée dans le dossier (`resize.png`) pour être sûr que ses dimensions soit 1200x600.
   
   2.2. Définissez vos paramètres pour le robot :
      * Nombre de rayons : de 2 à 40 unités
      * Portée des rayons : de 40 à 1200 pixels
      * Rayon d'action : de 90 à 360 degrés
   
   2.3. Cliquez sur le bouton `Lancer la simulation`, un message d'erreur apparaîtra si aucune map n'a été choisie.


3. Utiliser la simulation :

   3.1. Cliquez sur un endroit de la map (de préférence hors d'un obstacle fermé) pour positionner un robot.

   3.2. L'orientation du robot se gère à la souris, et le déplacement avec les flèches du clavier.

   3.3. Les rayons du lidar ne détectant pas de collision s'affichent en bleu, sinon en rouge.

   3.4. La fonction efficience (reconstruction de la map grâce aux données de collisions) est disponible dans le menu `Simulation`.

   3.5. Pour revenir au menu principal, cliquez sur `Simulation` puis `Quitter simulation`.
   