import os
import csv
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QMessageBox, QProgressBar, QShortcut
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QFont, QKeySequence


class MainWindow(QMainWindow):
    def __init__(self, url_list):
        super().__init__()
        self.setWindowTitle("Mon navigateur web")
        # self.showFullScreen()  # Ouvrir en plein écran
        self.setGeometry(0, 0, 1900, 1000)
        shortcut_fullscreen = QShortcut(QKeySequence("F"), self)
        shortcut_fullscreen.activated.connect(self.toggle_fullscreen)
        self.etat = False

        self.url_list = url_list
        self.current_url_index = 0
        self.current_url = self.url_list[self.current_url_index]

        # Création de la vue web
        self.web_view = QWebEngineView()
        self.load_current_url()

        self.web_view.loadStarted.connect(self.on_load_started)
        self.web_view.loadFinished.connect(self.on_load_finished)

        # Barre de progression du chargement
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)

        # Élément de pourcentage de chargement
        self.progress_label = QLabel()
        self.progress_label.setAutoFillBackground(True)
        self.progress_label.hide()

        # Création du layout horizontal pour aligner la progresse bar et son label
        progress_layout = QHBoxLayout()
        progress_layout.addWidget(self.progress_label)
        progress_layout.addWidget(self.progress_bar)

        # Création du champ d'URL
        self.url_label = QLabel()
        self.url_label.setFont(QFont("Arial", 12))
        self.url_label.setText(self.current_url)

        # Création du label de pourcentage d'URL terminées
        self.progress_percentage_label = QLabel()
        self.progress_percentage_label.setFont(QFont("Arial", 12))
        self.update_progress_percentage_label()

        # Création du layout horizontal pour aligner les labels
        label_layout = QHBoxLayout()
        label_layout.addWidget(self.url_label)
        label_layout.addStretch(1)
        label_layout.addWidget(self.progress_percentage_label)

        # Création des boutons
        self.button_layout = QHBoxLayout()

        self.button1 = QPushButton("Scam (A)")
        self.button1.setObjectName("button1")
        self.button1.setFont(QFont("Arial", 18))
        self.button1.setShortcut("A")
        self.button1.setFocus()
        self.button1.clicked.connect(self.update_csv_scam)
        self.button_layout.addWidget(self.button1)

        self.button2 = QPushButton("Spam (Z)")
        self.button2.setObjectName("button2")
        self.button2.setFont(QFont("Arial", 18))
        self.button2.setShortcut("Z")
        self.button2.clicked.connect(self.update_csv_spam)
        self.button_layout.addWidget(self.button2)

        self.button3 = QPushButton("Nothing (E)")
        self.button3.setObjectName("button3")
        self.button3.setFont(QFont("Arial", 18))
        self.button3.setShortcut("E")
        self.button3.clicked.connect(self.update_csv_nothing)
        self.button_layout.addWidget(self.button3)

        # Création du layout principal
        self.layout = QVBoxLayout()
        self.layout.addLayout(label_layout)
        self.layout.addLayout(progress_layout)
        self.layout.addWidget(self.web_view, 1)
        self.layout.addLayout(self.button_layout, 1)

        # Création du widget central
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

    def toggle_fullscreen(self):
        if self.etat:
            self.showNormal()
            self.etat = False
        else:
            self.showFullScreen()
            self.etat = True

    def update_progress_percentage_label(self):
        total_urls = len(self.url_list)
        completed_urls = self.current_url_index
        percentage = float((completed_urls / total_urls) * 100)
        self.progress_percentage_label.setText(
            f"{round(percentage,2)}% terminé sur cette session")

    def load_current_url(self):
        self.web_view.load(QUrl(self.current_url))
        self.web_view.loadStarted.connect(self.on_load_started)
        self.web_view.loadProgress.connect(self.on_load_progress)
        self.web_view.loadFinished.connect(self.on_load_finished)
        self.web_view.loadFinished.connect(
            self.update_progress_percentage_label)

    def on_load_progress(self, progress):
        # print(f"Charger à {progress}%")
        self.setWindowTitle(f"Mon navigateur web - Chargement à {progress}%")
        self.progress_label.setText(f"{progress}%")
        self.progress_bar.setValue(progress)

    def on_load_started(self):
        # print(f"Chargement du site : {self.current_url}")
        self.setWindowTitle(f"Mon navigateur web - Chargement en cours...")
        self.toggle_buttons_enabled(False)
        self.progress_label.setText("0%")
        self.progress_bar.show()
        self.progress_label.show()

    def on_load_finished(self):
        # print(f"Chargement terminé : {self.current_url}")
        self.setWindowTitle(f"Mon navigateur web - {self.current_url}")
        self.toggle_buttons_enabled(True)
        self.progress_bar.hide()
        self.progress_label.hide()

    def toggle_buttons_enabled(self, enabled):
        self.button1.setEnabled(enabled)
        self.button2.setEnabled(enabled)
        self.button3.setEnabled(enabled)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Calculer le pourcentage de hauteur pour les boutons
        button_height_percentage = 0.1  # 10% de la hauteur totale de la fenêtre

        # Calculer la hauteur des boutons en fonction du pourcentage
        button_height = int(max(20, self.height() * button_height_percentage))

        # Appliquer la hauteur calculée aux boutons
        self.button1.setFixedHeight(button_height)
        self.button2.setFixedHeight(button_height)
        self.button3.setFixedHeight(button_height)

    def update_csv_scam(self):
        self.update_csv("SCAM")

    def update_csv_spam(self):
        self.update_csv("SPAM")

    def update_csv_nothing(self):
        self.update_csv("NOTHING")

    def update_csv(self, status):
        with open('result.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([self.current_url, status])
        self.load_next_url()

    def load_next_url(self):
        self.current_url_index += 1
        if self.current_url_index < len(self.url_list):
            self.current_url = self.url_list[self.current_url_index]
            self.url_label.setText(self.current_url)
            self.load_current_url()
        else:
            self.show_summary_popup()

    def show_summary_popup(self):
        spam_count = 0
        scam_count = 0
        nothing_count = 0

        with open('result.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) >= 2:
                    if row[1] == 'SPAM':
                        spam_count += 1
                    elif row[1] == 'SCAM':
                        scam_count += 1
                    elif row[1] == 'NOTHING':
                        nothing_count += 1

        summary_text = f"Résumé :\n\nSPAM : {spam_count}\nSCAM : {scam_count}\nNOTHING : {nothing_count}"

        msg_box = QMessageBox()
        msg_box.setWindowTitle("Traitement terminé")
        msg_box.setText("Toutes les URL ont été traitées.")
        msg_box.setInformativeText(summary_text)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.exec()


if __name__ == '__main__':
    url_list = []
    url_list_finish = []

    with open('./Siti Spam FR - 2023.csv', "r") as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            url_list.append("https://" + row[0])
    if os.path.exists('./result.csv'):
        with open('./result.csv', "r") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                url_list_finish.append(row[0])

        # Convertir les tableaux en ensembles
        set1 = set(url_list)
        set2 = set(url_list_finish)

        # Obtenir les éléments communs
        common_elements = set1.intersection(set2)

        # Obtenir les éléments qui ne sont pas communs
        unique_elements = set1.symmetric_difference(set2)

        # Convertir l'ensemble de résultats en tableau
        url_list_not_finish = list(unique_elements)

        # Calcul du pourcentage d'éléments en commun
        percentage_common = (len(common_elements) /
                             (len(url_list) + len(url_list_finish))) * 100

        print(
            f"Tu as fait {round(percentage_common,2)}% de {len(url_list)}")
        url_list = url_list_not_finish

    app = QApplication([])
    app.setStyleSheet(open("style.css").read())
    window = MainWindow(url_list)
    window.show()
    app.exec()
