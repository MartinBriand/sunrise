# Simulator

Ce simulateur (peut-être émulateur, je ne suis pas au point sur la 
terminologie) a pour but de vérifier que le code programmé en Arduino de 
contrôle des moteurs est bien correct sans avoir accès au matériel du groupe 
Arduino.

La façon dont il fonctionne est assez simple :
 - On exporte le code Arduino que l'on compile comme n'importe quel code en C++;
 - On réimplémente toutes les fonctions spécifiques à Arduino dont on a 
besoin dans notre code;

Les deux principaux blocs réimplémentés sont :
 - La liaison série, qui est remplacé par un serveur TCP sur le port 1783 de 
localhost;
 - La librairie kangaroo, qui est le coeur du simulateur. Les trajectoires 
décrites par les moteurs sont ensuite écrites dans un fichier nommé 
outfile.csv dont le format est décrit plus tard;

# outfile.csv

Les trajectoires décrites par les moteurs sont renvoyées dans un fichier 
nommé outfile.csv. Ce fichier est de type csv ("comma separated values") et 
utilise le symbole ';' comme séparateur. Chaque ligne de ce fichier est de la 
forme :
\<temps\>;\<1\>;\<2\>;\<3\>;\<4\>;\<5\>;\<6\>;\<7\>;\<8\>;
Où chaque nombre correspond à la coordonnée d'un des huits moteurs. Toutes 
ces valeurs sont entières (int32).

Pour utiliser le simulateur, il vous suffit d'écrire votre projet Arduino dans 
un sous-dossier immédiat du répertoire  arduino de ce dépôt git. Copiez 
ensuite dans ce dossier de travail le Makefile qui se trouve dans 
arduino/simulator. Pour compiler l'émulation de votre programme, il vous 
suffit ensuite de taper "\>\> make". Le fichier à exécuter se nommera 
"simulator.elf".

# Dépendances

Pour pouvoir utiliser l'émulateur, vous devez être sous Linux (je vous aime 
beaucoup, mais faire ce genre de choses sur Windows est assez pénible). Pour 
utiliser l'émulateur, vous aurez besoin de :
 - Un compilateur C++ standard (clang par exemple)
 - L'outil de compilation make

Pour pouvoir tester facilement la liaison série, vous aurez sans doute aussi 
envie d'utiliser netcat, qui vous permettra d'envoyer et de lire du texte à 
travers cette liaison. Pour connecter netcat au port 1783 de localhost, vous 
pouvez utiliser :
 - \>\> netcat localhost 1783;
