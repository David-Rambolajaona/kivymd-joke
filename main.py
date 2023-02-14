# import requests
# from kivy.app import App
# from kivy.uix.button import Button
# from kivy.uix.label import Label
# from kivy.uix.boxlayout import BoxLayout
# from kivy.clock import Clock


# class JokeApp(App):

#     def build(self):
#         # Créer un layout vertical pour afficher le bouton, le label et le message de chargement
#         layout = BoxLayout(orientation='vertical')

#         # Créer un bouton avec le texte "Obtenir une blague"
#         button = Button(text='Obtenir une blague')

#         # Lier la fonction get_joke à l'événement "on_press" du bouton
#         button.bind(on_press=self.get_joke)

#         # Ajouter le bouton au layout
#         layout.add_widget(button)

#         # Créer un label vide pour afficher la blague
#         self.joke_label = Label(text='')

#         # Mise à la ligne du texte
#         self.joke_label.multiline = True

#         # Ajouter le label au layout
#         layout.add_widget(self.joke_label)

#         # Créer un label pour le message de chargement
#         self.loading_label = Label(text='')

#         # Ajouter le label au layout
#         layout.add_widget(self.loading_label)

#         # Retourner le layout complet comme interface utilisateur
#         return layout

#     def show_loading(self):
#         # Afficher le message de chargement
#         self.loading_label.text = 'Chargement...'

#     def hide_loading(self):
#         # Cacher le message de chargement
#         self.loading_label.text = ''

#     def get_joke(self, instance):
#         # Afficher le message de chargement
#         self.show_loading()

#         # Utiliser Clock.schedule_once pour appeler la fonction get_joke_api après une courte pause
#         Clock.schedule_once(self.get_joke_api, 0.1)

#     def get_joke_api(self, *args):
#         # Envoyer une requête à l'API "JokeAPI" pour obtenir une blague
#         response = requests.get('https://v2.jokeapi.dev/joke/Any')

#         # Extraire la blague de la réponse JSON
#         if response.status_code == 200:
#             response_data = response.json()
#             if 'joke' in response_data:
#                 joke = response_data['joke']
#             else:
#                 if 'setup' in response_data:
#                     joke = response_data['setup'] + ' ' + response_data.get('delivery', '(Une erreur s\'est produite)')
#                 else :
#                     joke = 'Désolé, la structure de la blague ne correspond pas aux attentes'
#         else:
#             joke = 'Désolé, une erreur s\'est produite lors de la récupération de la blague'

#         # Cacher le message de chargement
#         self.hide_loading()

#         # Afficher la blague dans le label
#         self.joke_label.text = joke


# if __name__ == '__main__':
#     JokeApp().run()

"""
==============================================================================================
"""

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.network.urlrequest import UrlRequest
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRectangleFlatButton

KV = '''
BoxLayout:
    orientation: 'vertical'
    spacing: dp(10)
    padding: dp(10)

    MDRectangleFlatButton:
        text: "Tell me a joke"
        on_release: app.get_joke()
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}

'''

class JokeApp(MDApp):
    joke_dialog = None
    joke_label = ObjectProperty(None)

    def build(self):
        return Builder.load_string(KV)

    def get_joke(self):
        self.joke_dialog = MDDialog(title="Joke loading...", text="Please wait...")
        self.joke_dialog.open()
        UrlRequest('https://icanhazdadjoke.com/',
                   on_success=self.success_callback,
                   on_failure=self.failure_callback,
                   on_error=self.error_callback,
                   req_headers={'Accept': 'application/json'})

    def success_callback(self, request, result):
        self.joke_dialog.dismiss()
        joke = result['joke']
        self.joke_dialog = MDDialog(title="Joke", text=joke)
        self.joke_dialog.open()

    def failure_callback(self, request, result):
        self.joke_dialog.dismiss()
        self.joke_dialog = MDDialog(title="Error", text="Une erreur s'est produite")
        self.joke_dialog.open()

    def error_callback(self, request, result):
        self.joke_dialog.dismiss()
        self.joke_dialog = MDDialog(title="Error", text="Une erreur s'est produite")
        self.joke_dialog.open()

if __name__ == '__main__':
    JokeApp().run()

"""
==============================================================================================
"""