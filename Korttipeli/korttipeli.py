import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QHBoxLayout, QGroupBox, QPushButton, QGraphicsOpacityEffect, QLineEdit, QErrorMessage
from PyQt5.QtGui import QPixmap, QFont, QIcon, QPalette, QColor
from PyQt5.QtCore import *
import random
import urllib.request
import collections
import requests

global session
global url
global rahatilanne
global network
network = True
url = "http://127.0.0.1:5000/korttipeli/"
session = requests.Session()
try:
        s = session.post(url + 'login', data= {'username':'PeliUser', 'password':'PeliMysteeriSalasana132'})
        print("käytetään paikallista palvelinta")
except:
        url = "http://izba.ovh:5000/korttipeli/"
        try:
                s = session.post(url + 'login', data= {'username':'PeliUser', 'password':'PeliMysteeriSalasana132'})
                print("Käytetään ulkoista palvelinta")
        except:
                network = False
                print("kumpaakaan palvelinta ei löydy. Käynnistetään peli ilman verkkoominaisuuksia.")

class kortti(QPushButton):
        def __init__(self, maa, arvo):
                super().__init__()
                self.maa = maa
                self.arvo = arvo
                self.vaihdettava = False
                self.image = QPixmap("images/"+str(self.maa)+"_"+str(self.arvo)+".png")
                self.setIcon(QIcon(self.image))
                self.setIconSize(self.image.rect().size())
                self.setFixedSize(self.image.rect().size())
                self.effect = QGraphicsOpacityEffect()
                self.disappear()
        def a(self):
                return self.arvo
        
        def m(self):
                return self.maa
        @pyqtSlot()
        def appear(self):
                self.setGraphicsEffect(self.effect)
                self.appearAnim = QPropertyAnimation(self.effect, b"opacity")
                self.appearAnim.setDuration(500)
                self.appearAnim.setStartValue(0)
                self.appearAnim.setEndValue(1)
                print("appearing")
                self.appearAnim.start()

        def disappear(self):
                self.setGraphicsEffect(self.effect)
                self.disappearAnim = QPropertyAnimation(self.effect, b"opacity")
                self.disappearAnim.setDuration(500)
                self.disappearAnim.setStartValue(1)
                self.disappearAnim.setEndValue(0)
                self.disappearAnim.start()


class korttipakka():
        def __init__(self):
                self.kortit = list()
                self.vaihdetutkortit = list()
                self.keratytkortit = list()
                for x in range(0, 4):
                        for z in range(1, 14):
                                self.kortit.append(kortti(x, z))
                self.kortit.append(kortti(4, 14))
                self.kortit.append(kortti(4, 15))
                self.shuffle()
                
        def shuffle(self):
                count = len(self.vaihdetutkortit)
                print("vaihdetutkortit = " + str(count))
                for x in range(1, count + 1):
                        self.kortit.append(kortti(self.vaihdetutkortit[count - x].m(), self.vaihdetutkortit[count -x].a()))
                        self.vaihdetutkortit.pop()
                count = len(self.keratytkortit)
                for x in range(1, count + 1):
                        self.kortit.append(kortti(self.keratytkortit[count - x].m(), self.keratytkortit[count - x].a()))
                        self.keratytkortit.pop()
                
                random.shuffle(self.kortit)

        def jaaKortit(self, poyta):
                print("ennenjakoi =" + str(len(self.kortit)))
                for x in range(0, 5):
                        count = len(self.kortit) - 1
                        print("count = " + str(count))
                        poyta.laitaKortti(x, self.kortit[count])
                        self.kortit.pop()
                poyta.kortit[0].clicked.connect(lambda: poyta.valitse(0))
                poyta.kortit[1].clicked.connect(lambda: poyta.valitse(1))
                poyta.kortit[2].clicked.connect(lambda: poyta.valitse(2))
                poyta.kortit[3].clicked.connect(lambda: poyta.valitse(3))
                poyta.kortit[4].clicked.connect(lambda: poyta.valitse(4))
        def vaihdaKortit(self, poyta):
                for x in range(0, 5):
                        poyta.kortit[x].clicked.disconnect()
                for x in range(0, len(poyta.vaihdettavat)):
                        count = len(self.kortit) - 1
                        poyta.valitse(poyta.vaihdettavat[x])
                        self.vaihdetutkortit.append(poyta.kortit[poyta.vaihdettavat[x]])
                        poyta.kortit.pop(poyta.vaihdettavat[x])            
                        poyta.kortit.insert(poyta.vaihdettavat[x],self.kortit[count])
                        self.kortit.pop()  



class poyta(QGridLayout):
        def __init__(self, korttipakka):
                super().__init__()
                self.kortit = list()
                self.vaihdettavat = list()         
                self.panos = 0.2
                self.highSCORE = highscore()
                global rahatilanne
                rahatilanne = 10.0
                self.vaihdot = False 
                self.tyhja = True
                self.korttipakka = korttipakka
                self.initUI()

        def initUI(self):
                fontti = QFont("Times", 16, 75)
                pienempiFontti = QFont("Times", 14, 75)
                kortpak = QLabel()
                takakansi = QPixmap("images/back.png")
                kortpak.setPixmap(takakansi)
                voitonjako1 = QLabel("Kuningasvärisuora: \nViitoset: \nVärisuora: \nNeloset: \nTäyskäsi:")
                voitonjako2 = QLabel("Väri: \nSuora: \nKolmoset: \nKaksi paria: \nPari:")
                voitonjako1.setFont(fontti)
                voitonjako2.setFont(fontti)
                voitonjako1.setAlignment(Qt.AlignRight)
                voitonjako2.setAlignment(Qt.AlignRight)
                self.voittotaulu1 = QLabel()
                self.voittotaulu2 = QLabel() 
                self.voittotaulu1.setFont(fontti)
                self.voittotaulu2.setFont(fontti)
                self.voittotaulu1.setAlignment(Qt.AlignLeft)
                self.voittotaulu2.setAlignment(Qt.AlignLeft)
                self.kortit = list()
                self.voittoTeksti = QLabel()
                self.voittoTeksti.setFont(fontti)
                groupPanos = QGroupBox()
                groupVoitonjako = QGroupBox()                
                gridVoitonjako = QHBoxLayout()
                gridVoitonjako.addWidget(self.voittoTeksti)
                gridVoitonjako.addWidget(voitonjako1)
                gridVoitonjako.addWidget(self.voittotaulu1)
                gridVoitonjako.addWidget(voitonjako2)
                gridVoitonjako.addWidget(self.voittotaulu2)
                groupVoitonjako.setLayout(gridVoitonjako)
                rowPanos = QHBoxLayout()
                self.panosUp = QPushButton("▲")
                self.panosUp.setFixedSize(50, 50)
                self.panosText = QLabel(str(self.panos) + "€")
                self.panosDown = QPushButton("▼")
                self.panosDown.setFixedSize(50, 50)
                self.rahaText = QLabel(str(rahatilanne)+"€")
                self.panosText.setFont(pienempiFontti)
                self.panosUp.setFont(pienempiFontti)
                self.panosDown.setFont(pienempiFontti)
                self.rahaText.setFont(pienempiFontti)
                self.panosUp.clicked.connect(self.nostaPanosta)
                self.panosDown.clicked.connect(self.laskePanosta)
                pText = QLabel("Panos:")
                rText = QLabel("Rahatilanne:")
                pText.setFont(pienempiFontti)
                rText.setFont(pienempiFontti)
                
                rowPanos.addWidget(pText)
                rowPanos.addWidget(self.panosDown)
                rowPanos.addWidget(self.panosText)
                rowPanos.addWidget(self.panosUp)
                rowPanos.addWidget(rText)
                rowPanos.addWidget(self.rahaText) 
                
                groupPanos.setLayout(rowPanos)              
                
                groupJako = QGroupBox()
                rowJako = QHBoxLayout()
                
                self.jaaButton = QPushButton("Jaa kortit")
                scoreBoardButton = QPushButton("ScoreBoard")
                if(network):
                        scoreBoardButton.clicked.connect(self.highSCORE.updateShow)
                else:
                        error = QErrorMessage()
                        error.setWindowTitle("Network Error")
                        scoreBoardButton.clicked.connect(lambda: error.showMessage("Ominaisuus on pois käytöstä, sillä palvelimet ei vastaa."))
                        
                self.jaaButton.clicked.connect(self.jaaKortit)
                
                self.jaaButton.setFont(pienempiFontti)
                scoreBoardButton.setFont(pienempiFontti)

                rowJako.addWidget(self.jaaButton)
                rowJako.addWidget(scoreBoardButton)
                groupJako.setLayout(rowJako)
                self.setSpacing(20)
                
                self.valinnatText = list()

                for x in range (0, 5):
                        label = QLabel()
                        label.setFont(fontti)
                        label.setAlignment(Qt.AlignHCenter)
                        self.valinnatText.append(label)
                kortinpaikat = list()
                self.addWidget(kortpak, 1, 1)
                self.addWidget(groupVoitonjako, 1, 2, 1, 4)
                for x in range(0, 5):
                        self.addWidget(self.valinnatText[x], 2, x + 1)
                        kortinpaikka = QPushButton()
                        kortinpaikka.setFixedSize(222, 323)
                        kortinpaikat.append(kortinpaikka)
                        self.addWidget(kortinpaikat[x], 3, x + 1)
                self.addWidget(groupPanos, 4, 1, 4, 2)

                self.addWidget(groupJako, 4, 3, 4, 4)
                p = self.panos
                self.voittotaulu1.setText("{:.1f}€\n{:.1f}€\n{:.1f}€\n{:.1f}€\n{:.1f}€".format(100*p,80*p,60*p,40*p,20*p))
                self.voittotaulu2.setText("{:.1f}€\n{:.1f}€\n{:.1f}€\n{:.1f}€\n{:.1f}€".format(10*p,5*p,3*p,2*p,1*p))
            #    self.voittotaulu1.setText(str(100*self.panos) + "\n" + str(80*self.panos) + "\n" + str(60*self.panos) + "\n" + str(40*self.panos) + "\n" + str(20*self.panos))

        
        def laitaKortti(self, numero, kortti):
                if(len(self.kortit) < 5):
                        self.kortit.append(kortti)
                else:
                        self.kortit.insert(numero, kortti)


        def getVaihdettavat(self):
                self.vaihdettavat = list()
                for x in range (0, 5):
                        if(self.kortit[x].vaihdettava):
                                self.vaihdettavat.append(x)
                print("vaihdettavat lukumäärä="+str(len(self.vaihdettavat)))

        def tarkastaPoyta(self):
                global session
                global url
                global network
                addOsuma = url + "addOsuma"
                arvot = list()
                maat = list()
                vari = False
                tayskasi = False
                viitoset = False
                neloset = False
                kolmoset = False
                kaksiparia = False
                pari = False
                suora = False
                varisuora = False
                kuningasvarisuora = False
                jokerit = 0
                for x in range(0, 5):
                        arvot.append(self.kortit[x].a())
                        maat.append(self.kortit[x].m())
                jokerit = maat.count(4)
                counta = collections.Counter(arvot)
                countm = collections.Counter(maat)
                arvot.sort()
                print(len(countm.most_common()))
                if(len(countm.most_common()) == 1 or (len(countm.most_common()) == 2 and jokerit > 1)):
                        vari = True
                        print("Väri =")
                        print(vari)
                if(len(counta.most_common()) == 2):
                        if(counta.most_common()[0][1] == 4 and jokerit == 1):
                                vitoset = True
                                print("Vitoset =")
                                print(vitoset)
                        elif(counta.most_common()[0][1] == 4 or (counta.most_common()[0][1] == 3 and jokerit == 1)):
                                neloset = True
                                print("neloset =")
                                print(neloset)
                        else:
                                tayskasi = True
                                print(tayskasi)
                                print("täyskäsi =")
                if(len(counta.most_common()) == 3):


                        if(jokerit == 2):
                                vitoset = True
                                print("Vitoset")
                        elif(jokerit == 1):
                                tayskasi = True
                                print("täyskäsi")
                        elif(counta.most_common()[0][1] == 3 or (counta.most_common()[0][1] == 2 and jokerit == 1)):
                                kolmoset = True
                                print("Kolmoset =")
                                print(kolmoset)
                        else:
                                kaksiparia = True
                                print("kaksiparia =")
                                print(kaksiparia)
                if(len(counta.most_common()) == 4):
                        if(jokerit == 2):
                                neloset = True
                                print("Neloset")
                        elif(jokerit == 1):
                                kolmoset = True
                                print("Kolmoset")
                        else:
                                pari = True
                                print("yksi pari")
                                print(counta.most_common())
                if(len(counta.most_common()) == 5):
                        print(arvot)
                        tempjokerit = jokerit
                        for x in range(0, 4):
                                print("X="+str(x))
                                if(arvot[x] == arvot[x + 1] - 1):
                                        print(arvot[x])
                                        print(arvot[x + 1])
                                        suora = True
                                else:
                                        if(jokerit > 0):
                                                print("ennen jokerimuutosta:")
                                                print(arvot[x])
                                                print(arvot[x + 1])
                                                arvot.insert(x+1, arvot[x]+1)
                                                arvot.pop()
                                                jokerit = jokerit - 1
                                                print("jokerimuutoksen jälkeen:")
                                                print(arvot[x])
                                                print(arvot[x + 1])
                                                suora = True
                                        else:
                                                suora = False
                                                break
                        print(arvot)
                        if(suora):
                                print("Suora löytyi!")
                        else:
                                if(tempjokerit == 2):
                                        kolmoset = True
                                elif(tempjokerit == 1):
                                        pari = True
                if(suora and vari):
                        if(arvot[4] == 13 or arvot[3] == 13 or arvot[2] == 13):
                                print("Kuningasvärisuora!")
                                kuningasvarisuora = True
                        else:
                                print("Värisuora!")
                                varisuora = True

                voitto = False
                voitot = list()
                if(pari):
                        voitot.append("Sait yhden parin!")
                        voitot.append(1)
                        if(network):
                                session.post(addOsuma, data={'Osuma':'Pari'})
                        voitto = True
                if(kaksiparia):
                        voitot.append("Sait kaksi paria!")
                        voitot.append(2)
                        if(network):
                                session.post(addOsuma, data={'Osuma':'2Paria'})
                        voitto = True
                if(kolmoset):
                        voitot.append("Sait kolmoset!")
                        voitot.append(3)
                        if(network):
                                session.post(addOsuma, data={'Osuma':'3Samaa'})
                        voitto = True
                if(suora and vari == False):
                        voitot.append("Sait suoran!")
                        voitot.append(5)
                        if(network):
                                session.post(addOsuma, data={'Osuma':'Suora'})
                        voitto = True
                if(vari and suora == False):
                        voitot.append("Sait värin!")
                        voitot.append(10)
                        if(network):
                                session.post(addOsuma, data={'Osuma':'Vari'})
                        voitto = True
                if(tayskasi):
                        voitot.append("Sait täyskäden!")
                        voitot.append(20)
                        if(network):
                                session.post(addOsuma, data={'Osuma':'Tays'})
                        voitto = True
                if(neloset):
                        voitot.append("Sait neloset!")
                        voitot.append(40)
                        if(network):
                                session.post(addOsuma, data={'Osuma':'4Samaa'})
                        voitto = True
                if(varisuora):
                        voitot.append("Sait värisuoran!")
                        voitot.append(60)
                        if(network):
                                session.post(addOsuma, data={'Osuma':'Varisuora'})
                        voitto = True
                if(viitoset):
                        voitot.append("Sait viitoset!")
                        voitot.append(80)
                        if(network):
                                session.post(addOsuma, data={'Osuma':'5Samaa'})
                        voitto = True
                if(kuningasvarisuora):
                        voitot.append("SAIT KUNINGASVÄRISUORAN!")
                        voitot.append(100)
                        if(network):
                                session.post(addOsuma, data={'Osuma':'Kuningasvarisuora'})
                        voitto = True
                if(voitto): 
                        return voitot
                else:
                        voitot.append("Ei voittoa tällä kertaa.\nHarmin paikka.")
                        voitot.append(0)
                        return voitot

        @pyqtSlot()
        def valitse(self, y):
                if(self.kortit[y].vaihdettava):
                        self.kortit[y].vaihdettava = False
                        p = self.kortit[y].palette()
                        p.setColor(QPalette.Button, QColor(Qt.gray))
                        self.kortit[y].setAutoFillBackground(True)
                        self.kortit[y].setPalette(p)
                        self.kortit[y].update()
                        self.valinnatText[y].setText("")
                else:
                        self.kortit[y].vaihdettava = True
                        p = self.kortit[y].palette()
                        p.setColor(QPalette.Button, QColor(Qt.blue))
                        self.kortit[y].setAutoFillBackground(True)
                        self.kortit[y].setPalette(p)
                        self.kortit[y].update()
                        self.valinnatText[y].setText("Vaihdettava")
        def nostaPanosta(self):
                if self.panos < 2:
                        if self.panos == 1:
                                self.panos = 2
                        else:
                                self.panos = self.panos + 0.2
                p = self.panos
                self.panosText.setText("{:.2f}€".format(self.panos))
                self.voittotaulu1.setText("{:.1f}€\n{:.1f}€\n{:.1f}€\n{:.1f}€\n{:.1f}€".format(100*p,80*p,60*p,40*p,20*p))
                self.voittotaulu2.setText("{:.1f}€\n{:.1f}€\n{:.1f}€\n{:.1f}€\n{:.1f}€".format(10*p,5*p,3*p,2*p,1*p))
                #self.voittotaulu1.setText(str(100*self.panos) + "\n" + str(80*self.panos) + "\n" + str(60*self.panos) + "\n" + str(40*self.panos) + "\n" + str(20*self.panos))
                #self.voittotaulu2.setText(str(10*self.panos) + "\n" + str(5*self.panos) + "\n" + str(3*self.panos) + str(2*self.panos) + "\n" + str(1*self.panos))
        def laskePanosta(self):
                if self.panos > 0.4:
                        if self.panos == 2:
                                self.panos = 1
                        else:
                                self.panos = self.panos - 0.2
                p = self.panos
                
                self.panosText.setText("{:.2f}€".format(self.panos))
                self.voittotaulu1.setText("{:.1f}€\n{:.1f}€\n{:.1f}€\n{:.1f}€\n{:.1f}€".format(100*p,80*p,60*p,40*p,20*p))
                self.voittotaulu2.setText("{:.1f}€\n{:.1f}€\n{:.1f}€\n{:.1f}€\n{:.1f}€".format(10*p,5*p,3*p,2*p,1*p))
 #               self.voittotaulu1.setText(str(100*self.panos) + "\n" + str(80*self.panos) + "\n" + str(60*self.panos) + "\n" + str(40*self.panos) + "\n" + str(20*self.panos))
  #              self.voittotaulu2.setText(str(10*self.panos) + "\n" + str(5*self.panos) + "\n" + str(3*self.panos) + str(2*self.panos) + "\n" + str(1*self.panos))
        def jaaKortit(self):
                global rahatilanne
                if(self.vaihdot == False):
                        self.tyhjaaPoyta()
                        self.voittoTeksti.setText("")
                        self.korttipakka.jaaKortit(self)
                        rahatilanne = rahatilanne - self.panos
                        self.rahaText.setText("{:.1f}€".format(rahatilanne))
                        self.panosDown.setEnabled(False)
                        self.panosUp.setEnabled(False)
                        self.vaihdot = True
                        print("kortit määrä=" +str(len(self.kortit)))
                        for x in range(0, 5):
                                print(x)
                                QTimer.singleShot(200 * x, self.kortit[x].appear)
                        for x in range(1, 6):
                                self.addWidget(self.valinnatText[x - 1], 2, x)
                                self.addWidget(self.kortit[x - 1], 3, x)
                        self.tyhja = False
                else:
                        self.getVaihdettavat()
                        for x in range(0, len(self.vaihdettavat)):
                                QTimer.singleShot(200 * x, self.kortit[self.vaihdettavat[x]].disappear)
                        self.vaihdaKortit()
                        self.vaihdot = False
                        self.laskeVoitot()
                        self.panosDown.setEnabled(True)
                        self.panosUp.setEnabled(True)
                        #for x in range(0,5):
                                #self.kortit[x].disconnect()
                        self.korttipakka.shuffle() 
        def tyhjaaPoyta(self):
                if(self.tyhja):
                        print("tyhjä")
                else:
                        for x in range(0, len(self.kortit)):
                                cout = len(self.kortit) - 1
                                QTimer.singleShot(200 * x, self.kortit[cout].disappear)
                                self.removeWidget(self.kortit[cout])
                                self.korttipakka.keratytkortit.append(self.kortit[cout])
                                self.kortit.pop()
                        self.tyhja = True
                        print("tyhjäpitäisi olla=" + str(len(self.kortit)))
        def vaihdaKortit(self):
                self.jaaButton.clicked.disconnect()
                QTimer.singleShot(1000, self.waitFunc)
                print("ennen vaihtoa count = " + str(len(self.kortit)))
                self.korttipakka.vaihdaKortit(self)
                for x in range(0, len(self.vaihdettavat)):
                        print("vaihdetaan indeksiin = " + str(self.vaihdettavat[x]))
                        QTimer.singleShot(200 * x, self.kortit[self.vaihdettavat[x]].appear)
                for x in range(0, 5):
                        self.removeWidget(self.kortit[x])
                        self.addWidget(self.kortit[x], 3, x + 1)
                        print(str(x) +". arvo=" + str(self.kortit[x].a()) + "|maa=" + str(self.kortit[x].m()))
                print("vaihdon jälkeen count = " + str(len(self.kortit)))

        def laskeVoitot(self):
                global rahatilanne
                voitot = self.tarkastaPoyta()
                rahasumma = voitot[1] * self.panos
                rahatilanne = rahatilanne + rahasumma
                self.rahaText.setText("{:.1f}€".format(rahatilanne))
                if(voitot[1] > 0):
                        voittoString = voitot[0] + "\n" + "Voitto summa {:.1f}€".format(rahasumma) + "\nOnnittelut!"
                else:
                        voittoString = voitot[0]
                self.voittoTeksti.setText(voittoString)
                
        def waitFunc(self):
                self.jaaButton.clicked.connect(self.jaaKortit)
class screen(QWidget):

        def __init__(self,table):
                super().__init__()
                self.table = table
                self.initUI()
        def initUI(self):
                self.scoret = list()
                self.labels = list()
                self.setWindowTitle("Pokeripeli")
                self.setLayout(self.table)
                self.show()

class highscore(QWidget):
        def __init__(self):
                super().__init__()
                self.initUI()
                
        def initUI(self):
                self.setWindowTitle("ScoreBoard")
                self.scoreGrid = QGridLayout()
                self.fontti = QFont("Times", 14, 75)
                self.labels = list()
                self.scoret = list()
                self.scoreGroup = QGroupBox()
                self.osumaGroup = QGroupBox()
                self.osumaGrid = QGridLayout()
                self.mainGrid = QGridLayout()
                self.setLayout(self.mainGrid)
                self.setFixedSize(self.size()) 
                for x in range(0, 10):
                        self.scoret.append([QLabel(str(x + 1)+"."), QLabel("username"), QLabel("tulos")])
                        self.labels.append(QLabel())

        def updateShow(self):
                global session
                global url
                global rahatilanne
                os = session.get(url + "getOsumat")  
                sco = session.get(url + "getScores")
                o = os.text.replace("(", "")
                o = o.replace(")", "")
                s = sco.text.replace("(", "")
                s = s.replace(")", "")
                s = s.replace("'", "")
                s = s.split(",")
                
                print(sco.text)
                osumat = o.split(",")
                self.labels[0].setText("Parit: " + osumat[0])
                self.labels[1].setText("2 Paria: " + osumat[1])
                self.labels[2].setText("Kolmoset: " + osumat[2])
                self.labels[3].setText("Neloset: " + osumat[3])
                self.labels[4].setText("Vitoset: " + osumat[4])
                self.labels[5].setText("Väri: " + osumat[5])
                self.labels[6].setText("Suora: " + osumat[6])
                self.labels[7].setText("Täys: " + osumat[7])
                self.labels[8].setText("Värisuora: " + osumat[8])
                self.labels[9].setText("Kuningasvärisuora: " + osumat[9])
                self.scoreGrid.setSpacing(20)
                z=0
                cout = len(s) / 2
                cout = int(cout)
                for x in range(0, cout):
                        self.scoret[x][1].setText(s[z])
                        self.scoret[x][2].setText("{:.2f}€".format(float(s[z+1])))
                        z = z + 2
                for x in range(0, 10):
                        self.scoreGrid.removeWidget(self.scoret[x][0])
                        self.scoreGrid.removeWidget(self.scoret[x][1])
                        self.scoreGrid.removeWidget(self.scoret[x][2])
                        self.scoreGrid.addWidget(self.scoret[x][0], x + 1, 1)
                        self.scoreGrid.addWidget(self.scoret[x][1], x + 1, 2)
                        self.scoreGrid.addWidget(self.scoret[x][2], x + 1, 3)
                        self.scoret[x][0].setFont(self.fontti)
                        self.scoret[x][1].setFont(self.fontti)
                        self.scoret[x][2].setFont(self.fontti)
                username = QLineEdit()
                username.setMaxLength(50)
                username.setPlaceholderText("Lisää nimesi listoille!")
                submit = QPushButton("Lähetä")
                submit.clicked.connect(lambda: self.submit(username))
                self.scoreGrid.addWidget(username, 11, 1, 1, 2)
                self.scoreGrid.addWidget(submit, 11, 3) 
                for x in range(0, len(self.labels)):
                        self.osumaGrid.removeWidget(self.labels[x])
                        self.osumaGrid.addWidget(self.labels[x], x + 1, 0)         
                        self.labels[x].setFont(self.fontti)
                        self.labels[x].setAlignment(Qt.AlignRight)
                self.osumaGroup.setLayout(self.osumaGrid)
                self.scoreGroup.setLayout(self.scoreGrid)
                self.mainGrid.addWidget(self.osumaGroup, 1, 1)
                self.mainGrid.addWidget(self.scoreGroup, 1, 2)
                self.show()
        def submit(self, username):
                global session
                global url
                global rahatilanne
                print(username.text())
                if(username.text() == ""):
                        error = QErrorMessage(self)
                        error.setWindowTitle("Error")
                        error.showMessage("Unohdit asettaa käyttäjänimen!")
                else:
                        print(url + "addScore")
                        session.post(url + "addScore", data={"username":username.text(), "score": rahatilanne})
                        self.updateShow()
if __name__ == '__main__':

        app = QApplication(sys.argv)
        pakka = korttipakka()
        table = poyta(pakka)
        ex = screen(table)
        sys.exit(app.exec_())