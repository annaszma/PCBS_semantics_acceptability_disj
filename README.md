Acceptability Judgment Task
================
Anna Szmarowska

# Tâche de jugement d’acceptabilité en polonais

## Introduction

L’objectif de ce projet est de créer une **tâche de jugement
d’acceptabilité en polonais**. Il rentre en partie dans le cadre de
mon stage en linguistique formelle et a vocation d’être amélioré dans
les prochains mois.

La présente expérience se compose alors d’une suite de jugements
successifs. Après la présentation des instructions, une phrase est
présentée au sujet qui doit la coter à travers une échelle numérique (0
= énoncé peu acceptable jusqu’à 7 = énoncé totalement acceptable).

Le dossier Github se compose notamment des 3 éléments suivant :

  - un *dossier “pictures”* qui comprend les images (.png) qui serviront
    à créer l’échelle numérique pour obtenir la réponse du sujet (images
    avec des chiffres de 0 à 7)  
  - un *fichier “sentences.csv”* qui contient les 12 phrases que le
    sujet devra évaluer  
  - un *script “PCBS\_acceptability\_judgment.py”* qui permettra de
    procéder à l’expérience

## Description du script

### Importation des différents packages

On commence tout d’abord à importer les modules nécessaires à
l’expérience :

``` python
from expyriment import design, control, stimuli, io, misc
from pandas import read_csv
import os.path
```

L’expérience est réalisée grâce au module expyriment. De plus, on
importe aussi la fonction read\_csv qui servira à lire le fichier .csv
qui contient les phrases à proposer au sujet ; ainsi que os.path pour
accéder facilement et de manière lisible aux images du dossier
“pictures”.

### Initialisation et création des stimuli

Ensuite, on crée une expérience à travers expyriment et on l’initialise
:

``` python
exp = design.Experiment(name="Acceptability judgment task")
control.initialize(exp)
```

Il est ensuite nécessaire de préparer les stimuli que l’on va utiliser
dans l’expérience. Pour se faire, on va d’abord créer des stimuli de
type “Picture” avec les images de l’echelle numérique. Ces stimuli
seront ensuite regroupés plus tard afin de créer une échelle complète et
interactive. Afin d’obtenir un code plus lisible, une fonction est
définie - en donnant un nombre et une position, la fonction va créer
directement un stimuli type “Picture” en utilisant l’image
correspondante dans le dossier “Pictures”.

``` python
def create_picture_stimuli(number, position):
    return stimuli.Picture(os.path.join("pictures", str(number)+".png"), position)
img0 = create_picture_stimuli(0, (-250, -100))
img1 = create_picture_stimuli(1, (-175, -100))
img2 = create_picture_stimuli(2, (-100, -100))
img3 = create_picture_stimuli(3, (-25, -100))
img4 = create_picture_stimuli(4, (50, -100))
img5 = create_picture_stimuli(5, (125, -100))
img6 = create_picture_stimuli(6, (200, -100))
img7 = create_picture_stimuli(7, (275, -100))
```

On crée de cette façon 8 différentes images que l’on affichera de
manière simultanée et qui serviront de boutons pour que le participant
réponde.

Enfin, on crée une dataframe à partir du fichier “sentences.csv” grâce à
la fonction read\_csv de pandas. Cette dataframe sera parcourue pendant
l’expérience pour afficher une à une les différents énoncés à juger.

``` python
data_stimuli = read_csv("sentences.csv")
```

### Variables supplémentaires et instructions

On définit alors deux variables supplémentaires qui serviront notamment
dans la définition de la procédure de l’expérience. Elle permettront
respectivement d’accéder de manière plus facile et lisible à la souris
et au clavier :

``` python
kb = exp.keyboard
mouse = io.Mouse()
```

Ensuite, on prépare les instructions. Pour cela, deux stimuli sont
créés:

``` python
instructions1= "Dzień dobry, \n\n\n W ramach pracy nad składnią i znaczeniem w \
języku polskim, zwracam się z prośbą o wyrażenie Państwa opinii na temat \
podanych zdań. \n Przeciętny czas potrzebny na wykonanie badania to około \
15 minut. Odpowiedzi są anonimowe. Dziękuję bardzo za poświęcenie tego czasu. \
\n\n\n Kliknijcie na spację"
instructions_1 = stimuli.TextScreen("Instructions", text = instructions1)

instructions2= "W badaniu ukaże się 15 zdań. Należy kliknąć na ocenę która, \
według Państwa, najbardziej odpowiada poprawności zdania. Skala jest od 0 do \
7. 0 oznacza że sformułowanie jest całkowicie niepoprawne i niezrozumiałe. \
7 jest najwyższą oceną poprawności. \n\n\n Kliknijcie na spację"
instructions_2 = stimuli.TextScreen("Instructions", text = instructions2)
```

### Préparation de l’obtention des réponses

Puis, avant de préparer le design et la procédure, une fonction est
définie pour récupérer de manière facilitée la réponse du participant.
On crée une liste contenant toutes les images définies précedemment.
Cette fonction va simplement comparer la réponse obtenue (ie l’image/le
bouton qui est appuyé(e)) avec la liste des images disponibles. Elle
permettra alors d’obtenir le numéro de cette image et donc d’extraire la
réponse du sujet.

``` python
list_img = [img0, img1, img2, img3, img4, img5, img6, img7]
def get_resp(button):
    """ Enables to obtain response from subject
        by getting the number of the touched button """
    for index in list(range(8)):
        if button == list_img[index]:
            output = index
    return output
```

Il ne reste alors plus qu’à créer le design et la procédure pour chaque
stimulus que l’on souhaite afficher.

### Création du design

Le design de cette expérience est relativement simple car il ne contient
qu’un seul block. Dans ce block, on va déterminer une série de trials
qui ne contiendront chacun qu’un seul stimulus (ie un seul énoncé).

Pour se faire, on définit donc un block que l’on implémente à travers
expyriment. Puis pour chaque phrase dans notre dataframe (issu de
“sentences.csv”), on crée un trial qui contient un seul stimulus ; à
savoir une ligne de texte avec l’énoncé en question.

``` python
block = design.Block()
for sentence in data_stimuli.sentence :
    t = design.Trial()
    s = stimuli.TextLine(sentence,text_bold=True,text_size=25,\
                         text_colour=(255,255,255),position=(0, 100))
    t.set_factor("sentence", sentence)
    t.add_stimulus(s)
    block.add_trial(t)
exp.add_block(block)
```

On définit ensuite les noms de variable pour notre fichier de données :

``` python
exp.add_data_variable_names(["sentence", "agreement"])
```

### Procédure et lancement de l’expérience

De ce fait, il ne reste alors plus qu’à débuter l’expérience. On
commence tout d’abord par afficher successivement nos 2 séries
d’instructions. Le participant devra appuyer sur la barre d’espace
pour continuer l’expérience.

``` python
control.start()
instructions_1.present()
kb.wait(misc.constants.K_SPACE)
instructions_2.present()
kb.wait(misc.constants.K_SPACE)
```

Ensuite, on définit le processus souhaité pour chaque énoncé. On crée
alors l’échelle de réponse, c’est-à-dire qu’on regroupe nos différentes
images sous une forme interactive - le sujet pourra alors cliquer sur
une image pour donner sa réponse. On y ajoute le stimulus du trial, à
savoir l’énoncé qui doit être jugé. Nos stimuli s’affichent alors comme
souhaité.

``` python
for trial in exp.blocks[0].trials:
    BB = io.TouchScreenButtonBox(list_img)
    BB.create()
    BB.add_stimulus(trial.stimuli[0])
    BB.show()
```

Pour que sujet puisse répondre, il est nécessaire que l’on indique
explicitement que le curseur de la souris doit être visible. On attend
ensuite la réponse du sujet et on extrait le chiffre correspondant grâce
à la fonction `get_resp` définie précédemment. On stocke cette
information dans notre fichier de données, en plus de l’énoncé qui est
affiché. Enfin, on prépare notre écran pour le stimulus suivant.

``` python
    mouse.show_cursor()
    button, rt = BB.wait()
    agreement = get_resp(button)
    exp.data.add([trial.get_factor("sentence"), agreement])
    exp.screen.clear()
    exp.screen.update()
    exp.clock.wait(1500)
```

Une fois chaque énoncé affiché, il ne reste plus qu’à terminer
l’expérience :

``` python
control.end()
```

Une fois l’expérience terminée, un fichier de données est alors généré
dans un dossier “data”. Ce fichier contiendra les informations
nécessaires aux futures analyses, à savoir la réponse du sujet (de 0 à
7) pour chaque énoncé.

## Retour sur expérience

Issue de formations littéraires (linguistique descriptive, langues,
littérature polonaise et histoire de l’art), je n’avais aucune notion
de programmation avant les cours du CogMaster. Le cours de PCBS m’a
permis d’apprendre à programmer sur Python et de pouvoir commencer à
l’appliquer à mon stage. En effet dans le cadre de mon stage en
sémantique formelle, je serai amenée au deuxième semestre à programmer
des expériences afin de recueillir des jugements sur les différentes
utilisations des disjonctions en polonais et leurs sens (inférences,
présuppositions et implicatures).

Le projet que j’ai effectué pour ce cours n’est donc qu’une ébauche
d’une première approche afin d’avoir des jugements d’acceptabilité de
phrases et de familiariser avec la programmation en Python.

Le principal problème auquel j’ai été confrontée, outre mon manque de
connaissances des fondamentaux de la programmation, était un problème
pour lancer Expyriment sur mon Mac (j’ai donc du utiliser un PC afin de
pouvoir faire marcher le programme).
