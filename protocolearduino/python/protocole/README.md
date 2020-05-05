# Fonctionnement du protocole python

Ce document permet d'expliquer le fonctionnement des différentes méthodes du protocole côté python.

> Pour voir le fonctionnement du protocole en détail, regarder l'autre fichier Protocole.md

Toute la communication repose autour d'un objet python de type `Protocole`.

Cet objet permet de communiquer avec la carte Arduino, il permet d'envoyer les informations, de recevoir des demandes de la part de l'Arduino, de démarrer le robot, ou de l'arrêter.

Le protocole étant encore en phase de développement, on y trouve de nombreux `print` pour aider à la compréhension et à l'utilisation en phase de développement.

## Initialisation d'un Protocole

Une instance `p` de `Protocole` s'initialise comme suit :

```python
p = Protocole(serial_port, serial_baudrate, speed_of_iter, pos_0, data)
```

Où les différents attributs sont :

* `serial_port` : Une `string` comportant l'adresse du port où est branchée l'Arduino
* `serial_baudrate` : le baudrate de la connexion Serial. Il doit être en regard de celui écrit sur l'Arduino. On recommande d'utiliser 9600. Une documentation se trouve facilement sur internet à se sujet
* `speed_of_iter` : Le temps en millisecondes entre chaque itération de mouvement pour l'Arduino 
* `pos_0` : La position initiale des moteurs qui sera communiquée à l'Arduino. Il s'agit d'un `array` `numpy` de `dtype` `'int32'`. Aucun autre format ne peut être communiqué
* `data` : L'ensemble des instructions qui seront communiquées à l'Arduino. Il s'agit d'un `array` `numpy` de dimension 2, de `dtype` `'int32'`, et dont la deuxième dimension doit être 8. L'ordre est important car il symbolise chacun des 8 moteurs. Aucun autre format ne peut être communiqué



## Fonctionnement général

Le protocole repose sur les étapes suivantes :

1. Initialiser le protocole (création d'un objet par l'appel de la fonction `Protocole`) . 
2. Envoyer les informations importantes à la carte Arduino (méthode `setup`)
3. Démarrer le robot (méthode `start`)
4. Mettre fin au protocole (méthode `close`)

Il est important de souligner 4 autres points :

* Il est toujours possible de savoir si la machine est en fonctionnement ou non par l'appel de l'attribut `is_started`.
* À tout moment, la communication peut être interrompue par l'appel à la méthode `stop` (et être redémarré par `start`)
* À tout moment, il est possible de modifier les valeurs `speed`, `pos_0` ou `data` de l'instance de protocole à l'aide de la méthode `change_values`. Celle-ci doit toujours être suivi d'un appel à `setup`. Celui-ci est voulu explicite pour que l'utilisateur reste conscient que changer les valeurs réinitialise le protocole
* Dans le cas où le robot est encore en fonctionnement, un appel à `close` ne fonctionnera pas. Il faut faire un appel à la méthode `stop_and_close`.

## Gestion des erreurs

Tout au long de la communication, trois erreurs peuvent intervenir :

1. L'Arduino envoie un signal d'erreur suivi d'une explication. Le protocole lèvera alors lui aussi une erreur avec un message explicatif. Le protocole est ensuite réinitialisé. L'Arduino se sera réinitialisée de son côté.
2. Une communication se passe mal du côté utilisateur. Le protocole lève une erreur avec un message explicatif et avertit l'Arduino pour que celle-ci se réinitialise. Le protocole se réinitialise aussi sur l'ordinateur
3. L'utilisateur fait une demande impossible (un `start` avant `setup` par exemple). Le protocole lève une erreur mais n'en informe pas l'Arduino pour que celle-ci puisse continuer son mouvement.

Par réinitialisation, on entend le fait que les méthodes `setup` et `start` doivent à nouveau être appelées.

Le fait que Python lève des erreurs fait que celles-ci peuvent être appréhendées par des `try/catch` dans une utilisation graphique.

## API

Soit p un instance de `Protocole` (créée selon le modèle précédent) :

### Méthodes publiques

Elles permettent de piloter le robot

```python
p.setup() # initialise l'Arduino, envoie pos_0, speed_of_iter, et reçoit la capacité mémoire de l'Arduino
p.start() # Lance la machine, et si celle-ci a besoin de données, les envoie
p.stop() # Stop le robot
p.close() # ferme le protocole si le robot est à l'arrêt
p.stop_and_close() # ferme le protocole après avoir arrêté le robot
p.change_values(pos_0 = (facultatif), data = (facultatif), speed_of_iter = (facultatif)) # remplace les différentes valeurs spécifiées en argument. Si rien n'est spécifié, l'ancienne valeur est conservée. Nécessite un appel à setup après avant start
```

### Méthodes privées

Elles sont en regard du code Arduino. Il est recommandé de ne pas les appeler, elle sont décrites ici pour la compréhension du code.

```python
_check_feed_or_error #est la fonction du thread d'interception de messages (voir partie suivante)
_init
_send_speed
_ask_memory
_send_pos_0 #Ces 4 fonctions sont appellées dans setup
_send_data #pour envoyer les data
_stop # appelé par stop dans le cadre de la gestion du multi-threading (partie suivante)
_start # idem que _stop mais pour start
_send_error # envoie un signal d'erreur à l'Arduino
_handle_feed_demand #reçoit un feed de l'Arduino, et y répond soit par un send data soit par un stop si le robot a fini son mouvement
_handle_arduino_exception # reçoit une erreur arduino et la signale

```

### Attributs publics

* `is_started` : permet de savoir en permanence si le robot est en fonctionnement ou non.

### Attributs privés

Encore une fois, ces attributs ne sont utilisés qu'à intérieur du protocole. Elles sont décrites ici pour corriger d'éventuels beugues, ou les comprendre pour du développement futur.

* `_MAX_TIME_TO_RECEIVE_A_BYTE` : Temps maximal en millisecondes avant que l'on lève un erreur de réception lorsqu'un bit est attendu de la part de la carte Arduino
* `_memory_initialized`, `_speed_of_iter_initialized`, `pos_0_initialized` : `bool` pour savoir si la connaissance des différentes variables sont partagées par python et Arduino.
* `_pos_0`, `speed_of_iter`, `_data` : valeur de ces variables
* `_pos_in_data` : place dans le vecteur de données des données déjà communiquées à l'Arduino
* `_thread_lock` : Droit acquit par l'un ou l'autre des deux threads (voir multi-threading)
* `_check_thread` : Deuxième thread pour vérifier l'acquisition de messages de la part de l'Arduino à tout moment.
* `_is_check_thread_alive` : Permet d'arrêter le thread
* `_serial` : Connection série à la carte Arduino

## Remarques sur le multi-threading

Afin de pouvoir interpréter des demandes de `feed` et des messages d'erreur de la part de l'Arduino à tout moment, il est nécessaire d'avoir deux threads. Un principal (celui ou l'on rentre les différents ordres), et un autre qui tourne en arrière plan pour intercepté ces messages : `_check_thread`. Pour que ces deux threads ne exécutent pas au même moment, et que l'un n'intercepte pas les messages destinés à l'autre, on utilise un droit d'acquisition qui bloque l'évolution des autres threads que celui qui l'acquiert : `_thread_lock`.

Cependant, le thread de vérification `_check_thread` tourne sur une boucle infinie. Il est donc important de l'arrêter pour terminer le programme. D'où les variables `_is_check_thread_alive` et les méthodes `close` et `stop_and_close`.