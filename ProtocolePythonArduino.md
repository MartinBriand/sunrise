# Protocole de communication Câble Robot - SunRise

Le protocole est basé sur une gestion par événements de la communication.
L'objectif de cette gestion est de résoudre le problème suivant : admettant
que l'octet à envoyer pour arrêter la machine soit 0xFF, comment distinguer le
fait que l'hôte Python demande d'arrêter le robot du fait que l'hôte
transmette un bloc de données qui par hasard contient un 0xFF.

L'idée est de toujours envoyer des octets d'événements qui annoncent ce qui
va suivre de sorte à ce qu'il ne soit jamais ambigue de savoir si un octet
fait partie d'un bloc de données ou s'il annonce un événements.

A chacun de ces événements est associé un code décimal, qui est la valeur
à envoyer par la liaision pour déclencher l'événement. Cette valeur est
envoyé sous la forme d'un char (i.e. 1 seul octet).

Notez qu'un échec lors de l'exécution du protocole (de l'une ou l'autre des
parties) doit amener à un arrêt du robot EN FERMANT LA COMMUNICATION (série
ou TCP suivant les cas). N'envoyez pas de signaux d'arrêt à travers la
connection dans le cas d'une erreur de protocole, car le résultat serait
imprévisible. Si l'hôte ou le client ferme la connection, la carte Arduino
devra arrêter les moteurs.

Certains événements sont dédiés à l'initialisation du robot et d'autres à
son mouvement. Utiliser un événement hors du cadre dans lequel il a été
prévu constitue une faute du protocole.

Une information importante concernant les messages d'erreurs ou d'arrêt (stop
et error). Vous êtes libre de substituer ces codes à n'importe quel autre
événement pendant la connection, mais vous n'avez pas le droit de les
substituer à quelque chose qui ne soit pas un événement.

# Les événements définis pour ce protocole sont :

## Evénements utiles à l'initialisation
            Python3          --initial (code 2)->            Arduino
            Python3          --vitesse (code 3)->            Arduino
            Python3          <-mémoire (code 4)--            Arduino
            Python3          -- pos_0  (code 5)->            Arduino
## Evénements utiles pendant le mouvement
            Python3          <- feed   (code 6)--            Arduino
            Python3          -- data   (code 7)->            Arduino
            Python3          -- stop   (code 8)->            Arduino
            Python3          -- start  (code 9)->            Arduino
## Evénements valables pendant toute la communication
            Python3          <-  ACK  (code 10)->            Arduino
            Python3          <- error (code 11)--            Arduino

# Description des événements :

## initial :

    Description: Cet événement est envoyé de Python3 vers la carte Arduino
    pour initier le protocole. La carte Arduino doit répondre à initial par un
    ACK.

    Usage:
    Python3          --initial (code 2)->            Arduino
    Python3          <-  ACK  (code 10)--            Arduino

## vitesse:

    Description: Cet événement précède l'envoi de le vitesse souhaitée par
    l'utilisateur pour la simulation. Cette vitesse est envoyée sous la forme
    d'un entier 32bits (4 octets). La carte Arduino doit répondre à la
    réception de cette vitesse par un echo (i.e. elle renvoie la valeur reçue
    à l'hôte Python).

    Usage:
    Python3          --vitesse (code 3)->            Arduino
    Python3          -- xxxx (4 octets)->            Arduino
    Python3          <- xxxx (4 octets)--            Arduino

## mémoire:

    Description: Cet événement précède l'envoi par la carte Arduino à
    l'hôte Python du nombre de vecteurs qu'elle souhaite recevoir lorsqu'elle
    fera un appel avec feed. Cet événement est suivi par l'envoi du nombre en
    question sous la forme d'un entier 32bits (4 octets). Le code en Python
    doit répondre à la récéption de ce nombre par un écho.

    Usage:
    Python3          <-mémoire (code 4)--            Arduino
    Python3          <- xxxx (4 octets)--            Arduino
    Python3          -- xxxx (4 octets)->            Arduino

## pos_0:

    Description: Cet événement précède l'envoi par l'hôte d'un vecteur
    contenant les positions initiales à donner aux moteurs. Cet événement est
    suivi par l'envoi du vecteur en question sous la forme de 8 entiers 32bits
    collés. Le code en Arduino doit répondre à la récéption de ce vecteur par
    un ACK.

    Usage:
    Python3          -- pos_0  (code 5)->            Arduino
    Python3          -- XXXXXXXX  (vec)->            Arduino
    Python3          <-  ACK  (code 10)--            Arduino

## feed:

    Description: Cet événement est envoyé par l'Arduino à l'hôte Python3
    pour lui demander de fournir davantage de vecteurs de mouvement à l'aide
    d'un événement data. L'hôte Python3 doit toujours répondre à un feed par un
    data (ou un stop le cas échéant).

    Usage:
    Python3          <- feed   (code 6)--            Arduino
    Python3          -- data   (code 7) ou end (code 12) ->            Arduino
                        etc... (voir data)

## data:

    Description: Cet événement est envoyé par l'hôte Python3 en réponse à
    un feed. Immédiatement après cet événement, l'hôte Python3 doit transmette
    à la carte Arduino le nombre de vecteurs qu'il va lui transmette sous la
    forme d'un entier 32bits (4 octets) auquel la carte doit répondre par un
    echo (i.e. renvoyer le nombre qu'elle vient de recevoir). Si tout c'est
    bien passé, l'hôte Python3 doit alors envoyer à la carte tous les vecteurs
    promis sous la forme d'une suite de tableaux de 8 entiers 32bits. Une fois
    le nombre de vecteurs promis reçus, la carte Arduino devra répondre par un
    ACK.

    Usage:
    Python3          -- data   (code 7)->            Arduino
    Python3          -- xxxx (4 octets)->            Arduino
    Python3          <- xxxx (4 octets)--            Arduino
    Python3          -- ****    (vecs) ->            Arduino
    Python3          <-  ACK  (code 10)--            Arduino

## stop:

    Description: Cet événement est envoyé par l'hôte Python3 vers la carte
    Arduino lui ordonner d'interrompre le mouvement de tel sorte qu'il puisse
    être repris plus tard. Il ne s'agit pas d'un arrêt d'urgence comme dans le
    cas où l'on ferme la communication, il s'agit sujet de ne plus faire
    avancer les moteurs jusqu'à nouvel ordre. La carte Arduino devra répondre
    à la récéption de cet événement par un ACK.

    Usage:
    Python3          -- stop   (code 8)->            Arduino
    Python3          <-  ACK  (code 10)--            Arduino

## start:

    Description: Cet événement sert à reprendre un mouvement qui a été
    interrompu par un stop et l'Arduino doit y répondre par un ACK. Notez
    qu'envoyer un start alors que la communication n'a pas été arrêtée par un
    stop constitue une faute de protocole.

    Usage:
    Python3          -- start  (code 9)->            Arduino
    Python3          <-  ACK  (code 10)--            Arduino

## ACK:

    Description: ACK (pour "Acknowledgment") est un événement envoyé à
    divers moments dans le protocole pour valider une communication. Notez que
    le code que j'ai donné à ACK ne correspond pas au code ASCII (0x06) que je
    ne connaissait pas.

## error:

    Description: Cet événement envoyé de la carte Arduino vers l'hôte
    Python3 signale qu'un problème interne a eu lieu et que le mouvement doit
    être interrompu. Immédiatement après avoir envoyé cet événement, la carte
    doit également envoyer un entier 32bit décrivant l'erreur qui a eu lieu
    (l'hôte doit déjà savoir à quoi ces erreurs correspondent). Un fois le code
    d'erreur envoyé par l'Arduino, la connection est considérée morte et aucune
    des parties n'est plus tenue de répondre aux messages de l'autre. La carte
    Arduino doit arrêter ses moteurs après avoir envoyé son code d'erreur à
    l'hôte, et l'hôte doit fermer la connection.

    Usage:
    Python3          <- error (code 11)--            Arduino
    Python3          <- xxxx (4 octets)--            Arduino


J'ai fait exprès de ne pas assigner le code 0 dans le protocole (il peut
parfois être difficile de faire la différence entre recevoir un 0 et ne rien
recevoir), par contre j'ai aussi passé le 1 et je ne vois pas du tout
pourquoi... Tant pis ;-)

Concernant l'initialisation, elle doit s'effectuer dans l'ordre des codes des
événements, c'est à dire : initial - vitesse - mémoire - pos_0.
