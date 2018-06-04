# Bibliotecas Python
import datetime
from functools import partial 

# Bibliotecas Kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition

from kivy.properties import NumericProperty
from kivy.properties import StringProperty
from kivy.lang import Builder


Builder.load_string('''
#:import random random.random

#:import BoxLayout kivy.uix.boxlayout.BoxLayout
#:import BoxLayout kivy.uix.floatlayout.FloatLayout

#:import ActionBar kivy.uix.actionbar.ActionBar
#:import ActionView kivy.uix.actionbar.ActionView
#:import ActionGroup kivy.uix.actionbar.ActionGroup

#:import Button kivy.uix.button.Button
#:import Image kivy.uix.image.Image
#:import TextInput kivy.uix.textinput.TextInput

<TelaPrincipal>:
    canvas:
        Color:
            rgb: 1, 1, 1
        Rectangle:
            pos: 0,0
            size: root.width,root.height
    ActionBar:
        id: rootActionBar
        size: root.width,self.height
        pos: root.x, root.top - self.height
        ActionView:
            use_separator: True
            ActionPrevious:
                title: 'Projeto vDieta'
                with_previous: False

			ActionOverflow:

            ActionButton:
                text: 'Dieta do Dia'
                on_release:
                    root.mmbDietaDia_Click()

            ActionButton:
                text: 'Consumir Receita'
                on_release:
                    root.mmbCC_Click()
					
			ActionGroup:
				text: 'Acessorios'
                ActionButton:
                    text: 'Historico'
					on_release:
						root.mmbHist_Click()
						
				ActionButton:
                    text: 'Resumo'
					on_release:
						root.mmbRes_Click()
						
                ActionButton:
                    text: 'Autor'
					on_release:
						root.mmbAutor_Click()
						
    FloatLayout:
        id: rootFloatLayout
        size: root.width,root.height - rootActionBar.height
        pos: root.x, root.y
        canvas:
            Color:
                rgb: 0, 1, 0
            Rectangle:
                size: self.size
                pos: self.pos
        ScreenManager:
            id: rootManager

<widBtnOpt>
			
			
<scDietaDia>:
    hue: random()
    canvas:
        Color:
            rgba: .0, .0, .8, 1
        Rectangle:
            size: self.size

	on_pre_enter: root.gerarTelaDietaAtual()
			
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Dieta do Dia'
            padding: 10,10
            halign: 'center'
            valign: 'middle'
            line_height: '2'
            font_size: 30
            text_size: self.size
            size_hint: 1,.2
        BoxLayout:
			id: scDietaDia_Buttons_BoxLayout
            orientation: 'vertical'
            padding: 50
            size_hint: 1,.8
            halign: 'center'
            valign: 'middle'
			Button:
				text: 'Proximo'
				on_press: root.proximo()
			
			
			
<scCCRef>:
    hue: random()
    canvas:
        Color:
            hsv: self.hue, .5, .3
        Rectangle:
            size: self.size

	on_pre_enter: root.gerarTelaCCRef()

	BoxLayout:
        orientation: 'vertical'
        Label:			
			id: scCCRef_Mainlabel
            text: 'Receitas da Refeição'
            font_size: 40
            size_hint: 1,0.2

<scCC>:
    hue: random()
    canvas:
        Color:
            hsv: self.hue, .5, .3
        Rectangle:
            size: self.size

    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Consumir Receita'
            font_size: 40
            size_hint: 1,0.2

<scHist>:
    hue: random()
    canvas:
        Color:
            hsv: self.hue, .5, .3
        Rectangle:
            size: self.size

    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Histórico de Consumo para o Dia'
            font_size: 40
            size_hint: 1,0.2

<scRes>:
    hue: random()
    canvas:
        Color:
            hsv: self.hue, .5, .3
        Rectangle:
            size: self.size

    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Resumo de Consumo para o período'
            font_size: 40
            size_hint: 1,0.2
			
<scAutor>:
    hue: random()
    canvas:
        Color:
            hsv: self.hue, .5, .3
        Rectangle:
            size: self.size
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'AUTOR'
            font_size: 40

        FloatLayout:
            Scatter:
                rotation: 30
                scale: 2
                pos: 20,20
                size_hint: None, None
                size: 100,100
                BoxLayout:
                    orientation: 'vertical'
                    Image:
                        source: "autorSmartstepsystems.jpg"
                        size: self.width, self.height
                    Label:
                        text: 'Mova! Gire!'
                        color: [1,0,0,1]
            Scatter:
                rotation: 25
                scale: 2
                pos: 120,40
                size_hint: None, None
                size: 100,100
                BoxLayout:
                    orientation: 'vertical'
                    Image:
                        source: "autorPessoa.jpg"
                        size: self.width, self.height
                    Label:
                        markup: True
                        text: 'Autor: Ronie Porfirio'
                        font_name: "autorFonte.ttf"
                        valign: 'bottom'
''')

# Aquivos do Projeto

#Variaveis Globais
chosenOpt = 0


# Janelas do Sistema
class TelaPrincipal(Widget):
    def returnFloatLayout(self):
        return self.ids['rootFloatLayout']

    def returnScreenManager(self):
        return self.ids['rootManager']

    def mmbDietaDia_Click(self):
        self.ids['rootManager'].transition = SlideTransition(direction="right")
        self.ids['rootManager'].current = 'scDietaDia'

    def mmbCCRef_Click(self):
        self.ids['rootManager'].transition = SlideTransition(direction="left")
        self.ids['rootManager'].current = 'scCCRef'

    def mmbCC_Click(self):
        self.ids['rootManager'].transition = SlideTransition(direction="left")
        self.ids['rootManager'].current = 'scCC'

    def mmbHist_Click(self):
        self.ids['rootManager'].transition = SlideTransition(direction="left")
        self.ids['rootManager'].current = 'scHist'

    def mmbRes_Click(self):
        self.ids['rootManager'].transition = SlideTransition(direction="left")
        self.ids['rootManager'].current = 'scRes'
		
    def mmbAutor_Click(self):
        self.ids['rootManager'].transition = SlideTransition(direction="left")
        self.ids['rootManager'].current = 'scAutor'


class widBtnOpt(Button):
	global chosenOpt
	codOpt = NumericProperty(0)

	def __init__(self, **kwargs):
		super(widBtnOpt, self).__init__(**kwargs)
		
	def iniciar(self,texto,cod):
		self.text = texto
		self.codOpt = cod

	def evento_click(self,manager,*args):
		global chosenOpt
		print(str(self.codOpt))
		chosenOpt = self.codOpt
		manager.current = 'scCCRef'
		
class scDietaDia(Screen):
	hue = NumericProperty(1)	
			
	def proximo(self):
		self.manager.current = 'scAutor'
	
	def	gerarTelaDietaAtual(self,*args):
		if db.getConfig('DietaAlterada') == '1':
			auxBoxLayout = self.ids['scDietaDia_Buttons_BoxLayout']
			df = db.retDF_DietaAtual()
			strRefeicao = ''
			for index,row in df.iterrows():
				if strRefeicao != row['strRefeicao']:
					strRefeicao = row['strRefeicao']
					lbRef = Label(text = str(row['hrHora']) + ' ' + strRefeicao)
					auxBoxLayout.add_widget(lbRef)
				btnOpt = widBtnOpt()
				btnOpt.iniciar(row['strOpt'],int(row['codOpt']))
				btnOpt.bind(on_press = partial(btnOpt.evento_click,self.manager))
				auxBoxLayout.add_widget(btnOpt)
			db.setConfig('DietaAlterada','0')			
			# Ao alterar a Dieta Atual seja consumindo algo ou etc, preciso refazer essa tela ou mandar excluir o botao
			
class scCCRef(Screen):
	global chosenOpt
	hue = NumericProperty(0)

	def gerarTelaCCRef(self,*args):
		global chosenOpt
		a = self.ids['scCCRef_Mainlabel']
		a.text = str(chosenOpt)
		#Aqui vou pegar a opcao e criar botoes com os conjuntos do tipo toogle para escolher e consumir
		# Atualizar tbHistOpt, atualizar tbHistConj e voltar pra tela anterior

	
class scCC(Screen):
    hue = NumericProperty(0)

class scHist(Screen):
    hue = NumericProperty(0)

class scRes(Screen):
    hue = NumericProperty(0)

class scAutor(Screen):
    hue = NumericProperty(0)

# Banco de dados
import dbDieta as db

###############################################################################
                                # Aplicativo Principal
###############################################################################
class mainDieta(App):
	def build(self):
		db.initDB()
		root = TelaPrincipal()
		rFL = root.returnFloatLayout()
		rSG = root.returnScreenManager()

		widScDietaDia  = scDietaDia(name='scDietaDia')
		widScCCRef  = scCCRef(name='scCCRef')
		widScCC  = scCC(name='scCC')
		widScHist  = scHist(name='scHist')
		widScRes  = scRes(name='scRes')
		widScAutor  = scAutor(name='scAutor')		
		
		listWidSc = [widScDietaDia,widScCCRef,widScCC,widScHist,widScRes,widScAutor]
		for widsc in listWidSc:
			rSG.add_widget(widsc)
		return root

if __name__ == '__main__':
    mainDieta().run()