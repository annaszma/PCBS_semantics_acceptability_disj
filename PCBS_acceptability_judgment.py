
"""
PCBS Project - Acceptability judgment task in polish
Anna Szmarowska
"""

#Importation of packages
from expyriment import design, control, stimuli, io, misc
from pandas import read_csv
import os.path

#Creation and initialization
exp = design.Experiment(name="Acceptability judgment task")
control.initialize(exp)

#Creation of stimuli
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
data_stimuli = read_csv("sentences.csv")

#Defining further variables
kb = exp.keyboard
mouse = io.Mouse()

instructions1= "Dzień dobry, \n\n\n W ramach pracy nad składnią i znaczeniem w \
języku polskim, zwracam się z prośbą o wyrażenie Państwa opinii na temat \
podanych zdań. \n Przeciętny czas potrzebny na wykonanie badania to około \
15 minut. Odpowiedzi są anonimowe. Dziękuję bardzo za poświęcenie tego czasu. \
\n\n\n Kliknijcie na spację"
instructions_1 = stimuli.TextScreen("Instructions", text = instructions1)

instructions2= "W badaniu ukaże się 12 zdań. Należy kliknąć na ocenę która, \
według Państwa, najbardziej odpowiada poprawności zdania. Skala jest od 0 do \
7. 0 oznacza że sformułowanie jest całkowicie niepoprawne i niezrozumiałe. \
7 jest najwyższą oceną poprawności. \n\n\n Kliknijcie na spację"
instructions_2 = stimuli.TextScreen("Instructions", text = instructions2)

#Defining function to get the subject answer
list_img = [img0, img1, img2, img3, img4, img5, img6, img7]
def get_resp(button):
    """ Enables to obtain response from subject
        by getting the number of the touched button """
    for index in list(range(8)):
        if button == list_img[index]:
            output = index
    return output

#Design
block = design.Block()
for sentence in data_stimuli.sentence :
    t = design.Trial()
    s = stimuli.TextLine(sentence,text_bold=True,text_size=25,\
                         text_colour=(255,255,255),position=(0, 100))
    t.set_factor("sentence", sentence)
    t.add_stimulus(s)
    block.add_trial(t)
exp.add_block(block)
exp.add_data_variable_names(["sentence", "agreement"])

#Starting
control.start()
instructions_1.present()
kb.wait(misc.constants.K_SPACE)
instructions_2.present()
kb.wait(misc.constants.K_SPACE)

for trial in exp.blocks[0].trials:
    BB = io.TouchScreenButtonBox(list_img)
    BB.create()
    BB.add_stimulus(trial.stimuli[0])
    BB.show()
    mouse.show_cursor()
    button, rt = BB.wait()
    agreement = get_resp(button)
    exp.data.add([trial.get_factor("sentence"), agreement])
    exp.screen.clear()
    exp.screen.update()
    exp.clock.wait(1500)

#Ending
control.end()
