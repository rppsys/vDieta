# Bibliotecas Python
import datetime
from functools import partial 

# Bibliotecas Kivy
from kivy.app import App

from kivy.uix.widget import Widget

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label

from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition, WipeTransition

# Bibliotecas Properties
from kivy.properties import NumericProperty
from kivy.properties import StringProperty
from kivy.properties import ListProperty
from kivy.properties import BooleanProperty

# Bibliotecas Recycled View
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior

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
            halign: 'center'
            valign: 'middle'
            font_size: 20
            size_hint: 1,.2
        BoxLayout:
			id: scDietaDia_Buttons_BoxLayout
			canvas:
				Color:
					rgba: .0, .5, .0, 1
				Rectangle:
					size: self.size

            orientation: 'vertical'
            padding: 50,0,50,50
			spacing: 10
            size_hint: 1,.8
            halign: 'center'
            valign: 'middle'
			
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
			text: 'Consumir Refeição'
            halign: 'center'
            valign: 'middle'
            font_size: 20
            size_hint: 1,.1
        Label:			
			id: scCCRef_lbStrRef
			text: 'Nome da Refeição'
            halign: 'center'
            valign: 'middle'
            font_size: 18
            size_hint: 1,.05
		BoxLayout:
			id: scCCRef_Buttons_BoxLayout
			canvas:
				Color:
					rgba: .0, .5, .0, 1
				Rectangle:
					size: self.size
			orientation: 'vertical'
            padding: 70,20,70,20
			spacing: 10
			size_hint: 1,.75
			halign: 'center'
			valign: 'middle'
		BoxLayout:
			canvas:
				Color:
					rgba: .5, .5, .0, 1
				Rectangle:
					size: self.size

			orientation: 'horizontal'
            padding: 50,5,50,5
			spacing: 10
			size_hint: 1,.1
			halign: 'center'
			valign: 'middle'
			
			Button:
				text: 'Consumir'
				font_size: 16
				on_press: root.consumir_click()
			Button:
				text: 'Cancelar'
				font_size: 16
				on_press: root.cancelar_click()				
<scCC>:
    hue: random()
    canvas:
        Color:
            hsv: self.hue, .5, .3
        Rectangle:
            size: self.size

	on_pre_enter: root.gerarTelaCC()			
			
	BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Consumir Receita'
            font_size: 40
            size_hint: 1,0.1
		BoxLayout:
			orientation: 'horizontal'
			canvas:
				Color:
					rgba: .0, .8, .0, 1
				Rectangle:
					size: self.size
			RV:
				id: scCC_rvConjunto
				size_hint: 1,1

			RV:
				id: scCC_rvAlimento
				size_hint: 1,1
		BoxLayout:
			canvas:
				Color:
					rgba: .5, .5, .0, 1
				Rectangle:
					size: self.size

			orientation: 'horizontal'
            padding: 50,5,50,5
			spacing: 10
			size_hint: 1,.1
			halign: 'center'
			valign: 'middle'
			
			Button:
				text: 'Consumir'
				font_size: 16
				
			Button:
				text: 'Cancelar'
				font_size: 16
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
						
<SelectableLabel>:
	canvas.before:
		Color:
			rgba: (.0, 0.9, .1, .3) if self.selected else (0, 0, .2, 1)
		Rectangle:
			pos: self.pos
			size: self.size
<RV>:
	viewclass: 'SelectableLabel'
	SelectableRecycleBoxLayout:
		default_size: None, dp(56)
		default_size_hint: 1, None
		size_hint_y: None
		height: self.minimum_height
		orientation: 'vertical'
		multiselect: True
		touch_multiselect: True
''')

# Aquivos do Projeto

#Variaveis Globais
toScCCRef_strRefeicao = '#####'

###############################################################################
################################         Widgets 
###############################################################################

class widBtnOpt(Button): # Não estou mais usando
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
		
class widBtnRef(Button):
	global toScCCRef_strRefeicao
	
	strRefeicao = StringProperty('')
	hrHora = NumericProperty(0)
	listOpt = ListProperty([])
	
	def __init__(self, **kwargs):
		super(widBtnRef, self).__init__(**kwargs)
		
	def iniciar(self,strRefeicao,hrHora):
		self.strRefeicao = strRefeicao
		self.hrHora = hrHora
		self.halign = 'center'
		self.valign = 'middle'
		self.text_size = 300, None
		self.font_size = '20sp'
		self.markup = True
		
	def optAppend(self,strOpt):
		self.listOpt.append(strOpt)

	def criar(self):
		textoHora = '[color=ffff00]' + str(self.hrHora) + 'h' + '[/color]'
		textoRefeicao = '[color=ffff00]' + self.strRefeicao + '[/color]'
		self.text = '[b]' + textoHora + ': ' + textoRefeicao + '[/b]'
		for i in self.listOpt:
			self.text += '\n [i][color=daa520] >>> ' + i + '[/color][/i]'
		
	def evento_click(self,manager,*args):
		global toScCCRef_strRefeicao
		toScCCRef_strRefeicao = self.strRefeicao
		manager.transition = SlideTransition(direction="left")
		manager.current = 'scCCRef'

class widTggConj(ToggleButton):
	meuCodigo = NumericProperty(0)
	meuCodOpt = NumericProperty(0)
	meuCodConj = NumericProperty(0)
	
	def __init__(self, **kwargs):
		super(widTggConj, self).__init__(**kwargs)

	def iniciar(self,texto,tbHistOpt_codigo,codOpt,codConj):
		self.meuCodigo = tbHistOpt_codigo
		self.meuCodOpt = codOpt
		self.meuCodConj = codConj
		self.group = 'g' + str(codOpt)
		self.halign = 'center'
		self.valign = 'middle'
		self.font_size = '18sp'
		self.text_size = 300, None
		self.markup = True
		strReceita,numCals = db.getReceitaFromCodConj(codConj)
		textoConjunto = '[b][color=ffff00] >>> ' + texto + ': ' + str(numCals) + ' KCal' + '[/color][/b]'
		textoReceita = '[size=14][i][color=daa520]' + strReceita + '[/color][/i][/size]'
		self.text = textoConjunto + '\n' + textoReceita


# Para as tabelas		
		
class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,RecycleBoxLayout):
	''' Nada '''

	
class SelectableLabel(RecycleDataViewBehavior, Label):
	''' Add selection support to the Label '''
	index = None
	selected = BooleanProperty(False)
	selectable = BooleanProperty(True)
	font_size = 18
	markup = True
	
	def refresh_view_attrs(self, rv, index, data):
		''' Catch and handle the view changes '''
		self.index = index
		return super(SelectableLabel, self).refresh_view_attrs(rv, index, data)

	def on_touch_down(self, touch):
		''' Add selection on touch down '''
		if super(SelectableLabel, self).on_touch_down(touch):
			return True
		if self.collide_point(*touch.pos) and self.selectable:
			return self.parent.select_with_touch(self.index, touch)

	def apply_selection(self, rv, index, is_selected):
		''' Respond to the selection of items in the view. '''
		self.selected = is_selected
		if is_selected:
			pass
			#print("selection changed to {0}".format(rv.data[index]))
		#else:
			#print("selection removed for {0}".format(rv.data[index]))

class RV(RecycleView):
	def __init__(self, **kwargs):
		super(RV, self).__init__(**kwargs)
		#self.data = [{'text': str(x)} for x in range(100)]		
		
		
###############################################################################
################################ Janelas do Sistema
###############################################################################

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
        self.ids['rootManager'].transition = SlideTransition(direction="up")
        self.ids['rootManager'].current = 'scHist'

    def mmbRes_Click(self):
        self.ids['rootManager'].transition = SlideTransition(direction="down")
        self.ids['rootManager'].current = 'scRes'
		
    def mmbAutor_Click(self):
        self.ids['rootManager'].transition = WipeTransition()
        self.ids['rootManager'].current = 'scAutor'
		
class scDietaDia(Screen):
	hue = NumericProperty(1)	
	
	def	gerarTelaDietaAtual(self,*args):
		if db.getConfig('DietaAlterada') == '1':
			auxBoxLayout = self.ids['scDietaDia_Buttons_BoxLayout']
			auxBoxLayout.clear_widgets()
			df = db.retDF_DietaAtual()
			
			if len(df) != 0:
				strRefeicao = '#####'
				for index,row in df.iterrows():
					if strRefeicao != row['strRefeicao']:
						if strRefeicao != '#####':
							btnRef.criar()
							auxBoxLayout.add_widget(btnRef)
					
						strRefeicao = row['strRefeicao']
						# Cria novo widBtnRef
						btnRef = widBtnRef()
						btnRef.bind(on_press = partial(btnRef.evento_click,self.manager))
						btnRef.iniciar(row['strRefeicao'],row['hrHora'])
						btnRef.optAppend(row['strOpt'])
					else:
						btnRef.optAppend(row['strOpt'])

				# Ao final deve adicionar o último botão criado		
				if strRefeicao != '#####':
					btnRef.criar()
					auxBoxLayout.add_widget(btnRef)					
				db.setConfig('DietaAlterada','0')			
				# Ao alterar a Dieta Atual seja consumindo algo ou etc, preciso refazer essa tela ou mandar excluir o botao
			else:
				lbAux = Label(text='Você já consumiu todos os alimentos de hoje!')
				auxBoxLayout.add_widget(lbAux)

class scCCRef(Screen):
	hue = NumericProperty(0)
	listTggConj = ListProperty([])
	
	def gerarTelaCCRef(self,*args):
		global toScCCRef_strRefeicao

		if toScCCRef_strRefeicao != '#####' :
			lbStrRef = self.ids['scCCRef_lbStrRef']
			auxBoxLayout = self.ids['scCCRef_Buttons_BoxLayout']
			
			lbStrRef.text = toScCCRef_strRefeicao
			auxBoxLayout.clear_widgets()
			df = db.retDF_DietaAtualFilterByStrRefeicao(toScCCRef_strRefeicao)
			self.listTggConj.clear()
			for index,row in df.iterrows():
				tggConj = widTggConj()
				tggConj.iniciar(row['strConjunto'],row['tbHistOpt_codigo'],row['codOpt'],row['codConj'])
				auxBoxLayout.add_widget(tggConj)					
				self.listTggConj.append(tggConj)

	def consumir_click(self):
		for tggConj in self.listTggConj:
			if tggConj.state == 'down':
				print(tggConj.text)
				# Tem que apendar tbHistConj
				db.append('tbHistConj',(db.sqlite3_DateTimeForSQL(datetime.date.today()),0,tggConj.meuCodConj,tggConj.meuCodOpt,))
				# TODO: DEPOIS TEM QUE COLOCAR A HORA CERTINHO
				db.tbHistOpt_ChecaOpt(tggConj.meuCodigo)
		db.setConfig('DietaAlterada','1')
		self.manager.transition = SlideTransition(direction="right")
		self.manager.current = 'scDietaDia'

	def cancelar_click(self):
		self.manager.transition = SlideTransition(direction="right")
		self.manager.current = 'scDietaDia'
		
class scCC(Screen):
	hue = NumericProperty(0)
	def gerarTelaCC(self,*args):
		rvConjunto = self.ids['scCC_rvConjunto']
		rvConjunto.data = db.conjuntoDictToRV()
	
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