# Bibliotecas Python
import datetime
from functools import partial 

# Bibliotecas Kivy
from kivy.app import App

from kivy.uix.widget import Widget

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner

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

#:set lbPrinc_fs 30
#:set grid6_shx .5


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
                title: 'Dieta Monitor'
                with_previous: False

			ActionOverflow:
			ActionGroup:
				text: 'Principal'
				ActionButton:
					text: 'Dieta do Dia'
					on_release:
						root.mmbDietaDia_Click()
				ActionButton:
					text: 'Consumir'
					on_release:
						root.mmbCC_Click()
			ActionGroup:
				text: 'Criar'
                ActionButton:
                    text: 'Alimentos'
					on_release:
						root.mmbCadAlim_Click()
                ActionButton:
                    text: 'Receitas'
					on_release:
						root.mmbCadConj_Click()
			ActionGroup:
				text: 'Acessórios'
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
            rgba: .0, .0, .5, 1
        Rectangle:
            size: self.size

	on_pre_enter: root.gerarTelaDietaAtual()
			
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Dieta do Dia'
            halign: 'center'
            valign: 'middle'
            font_size: lbPrinc_fs
            size_hint: 1,.2
		ScrollView:
			size_hint: 1, 0.8
			BoxLayout:
				id: scDietaDia_Buttons_BoxLayout
				size_hint: 1,None
				canvas:
					Color:
						rgba: .0, .0, .5, 1
					Rectangle:
						size: self.size

				orientation: 'vertical'
				padding: 50,0,50,50
				spacing: 10
				halign: 'center'
				valign: 'middle'
			
<scCCRef>:
    hue: random()
    canvas:
        Color:
            rgba: .0, .0, .5, 1
        Rectangle:
            size: self.size

	on_pre_enter: root.gerarTelaCCRef()

	BoxLayout:
        orientation: 'vertical'
        Label:			
			text: 'Consumir Refeição'
            halign: 'center'
            valign: 'middle'
            font_size: lbPrinc_fs
            size_hint: 1,.1
        Label:			
			id: scCCRef_lbStrRef
			text: 'Nome da Refeição'
            halign: 'center'
            valign: 'middle'
            font_size: 18
            size_hint: 1,.05
		ScrollView:
			size_hint: 1,.75
			BoxLayout:
				size_hint: 1,None
				id: scCCRef_Buttons_BoxLayout
				canvas:
					Color:
						rgba: .0, .0, .5, 1
					Rectangle:
						size: self.size
				orientation: 'vertical'
				padding: 70,20,70,20
				spacing: 10
				halign: 'center'
				valign: 'middle'

		BoxLayout:
			size_hint: 1,.1
			canvas:
				Color:
					rgba: .0, .0, .5, 1
				Rectangle:
					size: self.size

			orientation: 'horizontal'
            padding: 50,5,50,5
			spacing: 10
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
            rgba: .0, .0, .5, 1
        Rectangle:
            size: self.size

	on_pre_enter: root.gerarTelaCC()			
			
	BoxLayout:
        orientation: 'vertical'
        Label:
			size_hint: 1,0.1
            text: 'Consumir'
            font_size: lbPrinc_fs
		multiRV:
			id: scCC_rvReceitas
			size_hint: 1,0.5
		BoxLayout:
			size_hint: 1,0.2
			orientation: 'vertical'
			BoxLayout: #Caption e Bebida
				size_hint: 1,.4
				orientation: 'horizontal'
				Label:
					size_hint: 0.8,1
					text: 'Filtrar:'			
					text_size: self.size
					halign: 'left'
					valign: 'top'
					font_size: 18
				BoxLayout:
					size_hint: 0.2,1
					orientation: 'horizontal'
					CheckBox:
						id: scCC_checkBebida
						size_hint_x: .2
						on_active: root.atualizaRVConjunto()
					Label:
						text: 'Bebida'
					CheckBox:
						id: scCC_checkBebidaEstado
						on_active: if scCC_checkBebida.active: root.atualizaRVConjunto()
			BoxLayout: #Demais Filtros
				size_hint: 1,0.6
				orientation: 'horizontal'
				BoxLayout:
					orientation: 'vertical'
					GridLayout:
						cols: 2
						CheckBox:
							id: scCC_checkAlimento
							size_hint_x: .2
							on_active: root.atualizaRVConjunto()
						Label:
							text: 'Alimento:'
					TextInput:
						id: scCC_txtAlimento
						text: ''
						hint_text: 'Digite o alimento'
						multiline: False
						on_text: if scCC_checkAlimento.active: root.atualizaRVConjunto()
				BoxLayout:
					orientation: 'vertical'
					GridLayout:
						cols: 2
						CheckBox:
							id: scCC_checkGrupo
							size_hint_x: .2
							on_active: root.atualizaRVConjunto()
						Label:
							text: 'Grupo:'
					Spinner:
						id: scCC_spinGrupo
						text: '00 - Nenhum Grupo'
						on_text: if scCC_checkGrupo.active: root.atualizaRVConjunto() 
				BoxLayout:
					orientation: 'vertical'
					GridLayout:
						cols: 2
						CheckBox:
							id: scCC_checkTipo
							size_hint_x: .2
							on_active: root.atualizaRVConjunto()
						Label:
							text: 'Tipo:'
					Spinner:
						id: scCC_spinTipo
						text: '00 - Nenhum Tipo'
						on_text: if scCC_checkTipo.active: root.atualizaRVConjunto() 
		GridLayout:
			cols: 1
			size_hint: 1,0.1
			Label:
				id: scCC_lbAviso
				text: 'Selecione uma ou mais receitas e clique em consumir'
				text_size: self.size
				halign: 'center'
				valign: 'middle'
				font_size: 20
		BoxLayout:
			size_hint: 1,.1
			canvas:
				Color:
					rgba: .0, .0, .5, 1
				Rectangle:
					size: self.size
			orientation: 'horizontal'
            padding: 50,5,50,5
			spacing: 10
			halign: 'center'
			valign: 'middle'
			
			Button:
				text: 'Consumir'
				font_size: 16
				on_press: root.consumir_click()
				
			Button:
				text: 'Voltar'
				font_size: 16
				on_press: root.voltar_click() 

<scCadAlim>:
    hue: random()
    canvas:
        Color:
            rgba: .0, .0, .5, 1
        Rectangle:
            size: self.size

	on_pre_enter: root.gerarTela()			
			
	BoxLayout:
        orientation: 'vertical'
        Label:
            size_hint: 1,0.1
			text: 'Criar Alimentos'
            font_size: lbPrinc_fs
		tableRV:
			id: scCadAlim_rvAlimentos
			size_hint: 1,0.5
		BoxLayout:
			size_hint: 1,0.3
			orientation: 'vertical'
			GridLayout:
				cols: 4
				size_hint: 1,0.6
				Label:
					text: 'Nome:'
					size_hint_x: grid6_shx
				TextInput:
					id: scCadAlim_txtAlimento
					multiline: False
					text: ''
				Label:
					text: 'Bebida?'
					size_hint_x: grid6_shx
				CheckBox:
					id: scCadAlim_checkBebida
				Label:
					text: 'Grupo:'
					size_hint_x: grid6_shx
				Spinner:
					id: scCadAlim_spinGrupo
					text: '00 - Nenhum Grupo'
				Label:
					text: 'Tipo:'
					size_hint_x: grid6_shx
				Spinner:
					id: scCadAlim_spinTipo
					text: '00 - Saudável'
				Label:
					text: 'Qtd:'
					size_hint_x: grid6_shx
				TextInput:
					id: scCadAlim_txtQuantidade
					multiline: False
					text: '1'
				Label:
					text: 'Unid:'
					size_hint_x: grid6_shx
				Spinner:
					id: scCadAlim_spinUnidade
					text: 'unid'
			GridLayout:
				size_hint: 1,0.4
				cols: 2
				padding: 2,2,10,2
				Label:
					text: 'KCal/' + scCadAlim_spinUnidade.text + ' desse alimento?  '
					halign: 'right'
					text_size: self.size
				TextInput:
					size_hint_x: .2
					id: scCadAlim_txtCaloria
					multiline: False
					text: '0'
				Label:
					text: 'Peso g/ml de 1 ' + scCadAlim_spinUnidade.text + ' ?  '
					halign: 'right'
					text_size: self.size
				TextInput:
					size_hint_x: .2
					hint_text: '1'
					id: scCadAlim_txtPeso
					multiline: False
					text: '0'
		BoxLayout:
			size_hint: 1,.1
			canvas:
				Color:
					rgba: .0, .0, .5, 1
				Rectangle:
					size: self.size
			orientation: 'horizontal'
            padding: 50,5,50,5
			spacing: 10
			halign: 'center'
			valign: 'middle'
			Button:
				text: 'Cadastrar'
				font_size: 16
				on_press: root.cadastrar_click()
			Button:
				text: 'Cancelar'
				font_size: 16
		
<scCadConj>		
    hue: random()
    canvas:
        Color:
            rgba: .0, .0, .5, 1
        Rectangle:
            size: self.size

	on_pre_enter: root.gerarTela()			
			
	BoxLayout: #Box Pai
        orientation: 'vertical'
        Label: 
            size_hint: 1,0.1
			text: 'Criar Receitas'
            font_size: lbPrinc_fs
		multiRV:
			id: scCadConj_rvAlimentos
			size_hint: 1,0.4
		BoxLayout: # Comandos em baixo da tabela
			size_hint: 1,0.1 
			orientation: 'horizontal'
            padding: 50,5,50,5
			spacing: 10
			halign: 'center'
			valign: 'middle'
			Button:
				text: 'Gerar Conjunto'
				font_size: 16
				on_press: root.gerarConjunto_click()
			Button:
				text: 'Cancelar'
				font_size: 16
		
		BoxLayout: # Área onde vou gerar os alimentos selecionados para virar um conjunto
			size_hint: 1,0.3
			orientation: 'vertical'
			GridLayout:
				size_hint: 1,0.2
				orientation: 'vertical'
				cols: 3
				id: scCadConj_Box_Quantidades
			GridLayout:
				id: scCadConj_Grid_Quantidades
				cols: 3
				size_hint: 1,0.8
		BoxLayout: # Comandos em baixo
			size_hint: 1,.1
			canvas:
				Color:
					rgba: .0, .0, .5, 1
				Rectangle:
					size: self.size
			orientation: 'horizontal'
            padding: 50,5,50,5
			spacing: 10
			halign: 'center'
			valign: 'middle'
			Button:
				text: 'Incluir'
				font_size: 16
				on_press: root.incluirConjunto_click()
			Button:
				text: 'Cancelar'
				font_size: 16
		
<scHist>:
    hue: random()
    canvas:
        Color:
            rgba: .0, .0, .5, 1
        Rectangle:
            size: self.size

	on_pre_enter: root.gerarTela()			
			
	BoxLayout:
        orientation: 'vertical'
        Label:
			size_hint: 1,0.1
            text: 'Histórico de Consumo'
            font_size: lbPrinc_fs
		tableRV:
			id: scHist_rvHistorico
			size_hint: 1,0.7
		GridLayout:
			cols: 1
			size_hint: 1,0.1
			Label:
				id: scHist_lbAviso
				text: 'Mostrando histórico para hoje'
				text_size: self.size
				halign: 'center'
				valign: 'middle'
				font_size: 20
		BoxLayout:
			size_hint: 1,.1
			canvas:
				Color:
					rgba: .0, .0, .5, 1
				Rectangle:
					size: self.size
			orientation: 'horizontal'
            padding: 50,5,50,5
			spacing: 10
			halign: 'center'
			valign: 'middle'
			
			Button:
				text: 'Ok'
				font_size: 16
				on_press: root.consumir_click()
				
			Button:
				text: 'Voltar'
				font_size: 16
				on_press: root.voltar_click() 
			
<scRes>:
    hue: random()
    canvas:
        Color:
            rgba: .0, .0, .5, 1
        Rectangle:
            size: self.size

    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Resumo de Consumo'
            font_size: lbPrinc_fs
            size_hint: 1,0.2
			
<scAutor>:
    hue: random()
    canvas:
        Color:
            rgba: .0, .0, .5, 1
        Rectangle:
            size: self.size
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'AUTOR'
            font_size: lbPrinc_fs

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
<multiRV>:
	viewclass: 'SelectableLabel'
	SelectableRecycleBoxLayout:
		default_size: None, dp(56)
		default_size_hint: 1, None
		size_hint_y: None
		height: self.minimum_height
		orientation: 'vertical'
		multiselect: True
		touch_multiselect: True
		
<tableRV>:
	numSelCod : 1
	viewclass: 'SelectableLabel'
	SelectableRecycleBoxLayout:
		default_size: None, dp(56)
		default_size_hint: 1, None
		size_hint_y: None
		height: self.minimum_height
		orientation: 'vertical'
		multiselect: False
		touch_multiselect: False

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
		self.size_hint_y = None
		self.height = 100
		
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
		self.size_hint_y = None
		self.height = 100
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
	halign = 'center'
	valign = 'middle'

	
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
		''' Respond to the selection of items in the view. 
			o rv.data tem que ter o campo booSel 
		'''
		self.selected = is_selected
		if is_selected:
			rv.numSelCod = rv.data[index]['codigo']
			rv.data[index]['booSel'] = 1
		else:
			rv.data[index]['booSel'] = 0
			
class multiRV(RecycleView):
	def __init__(self, **kwargs):
		super(multiRV, self).__init__(**kwargs)
		self.data = [
		{'text':'Primeira linha','codigo':1,'booSel':0},
		{'text':'Segunda linha','codigo':2,'booSel':0},
		{'text':'Terceira linha','codigo':3,'booSel':0},
		{'text':'Quarta linha','codigo':4,'booSel':0},
		{'text':'Quinta linha','codigo':5,'booSel':0}
		]
	
class tableRV(RecycleView):
	''' O campo text e o campo codigo são obrigatórios na lista de dicts do campo rv.data '''

	def __init__(self, **kwargs):
		super(tableRV, self).__init__(**kwargs)
		self.data = [
		{'text':'Primeira linha','codigo':1,'booSel':0},
		{'text':'Segunda linha','codigo':2,'booSel':0},
		{'text':'Terceira linha','codigo':3,'booSel':0},
		{'text':'Quarta linha','codigo':4,'booSel':0},
		{'text':'Quinta linha','codigo':5,'booSel':0}
		]
		
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

    def mmbCadAlim_Click(self):
        self.ids['rootManager'].transition = SlideTransition(direction="left")
        self.ids['rootManager'].current = 'scCadAlim'

    def mmbCadConj_Click(self):
        self.ids['rootManager'].transition = SlideTransition(direction="left")
        self.ids['rootManager'].current = 'scCadConj'
		
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
			auxBoxLayout.bind(minimum_height=auxBoxLayout.setter('height'))

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
				lbAux.halign = 'center'
				lbAux.valign = 'middle'
				lbAux.text_size = 300, None
				lbAux.font_size = '20sp'
				lbAux.markup = True
				lbAux.size_hint_y = None
				lbAux.height = 100
				auxBoxLayout.add_widget(lbAux)

class scCCRef(Screen):
	hue = NumericProperty(0)
	listTggConj = ListProperty([])
	
	def gerarTelaCCRef(self,*args):
		global toScCCRef_strRefeicao

		if toScCCRef_strRefeicao != '#####' :
			lbStrRef = self.ids['scCCRef_lbStrRef']
			auxBoxLayout = self.ids['scCCRef_Buttons_BoxLayout']
			auxBoxLayout.bind(minimum_height=auxBoxLayout.setter('height'))

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
				db.append('tbHistConj',(db.sqlite3_DateForSQL(datetime.date.today()),0,tggConj.meuCodConj,tggConj.meuCodOpt,))
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
	
	def atualizaRVConjunto(self):
		rvConjunto = self.ids['scCC_rvReceitas']
		checkBebida = self.ids['scCC_checkBebida']
		checkBebidaEstado = self.ids['scCC_checkBebidaEstado']
		checkAlimento =  self.ids['scCC_checkAlimento']
		checkTipo =  self.ids['scCC_checkTipo']
		checkGrupo =  self.ids['scCC_checkGrupo']
		txtAlimento = self.ids['scCC_txtAlimento']
		spinGrupo = self.ids['scCC_spinGrupo']
		spinTipo = self.ids['scCC_spinTipo']

		textSQL = '''
			SELECT DISTINCT
			codigo, strConjunto, numFreq
			FROM 
			(SELECT 
			tbConj_Alim.codConj as codigo,
			tbConj.strConjunto,
			tbConj.numFreq,
			tbConj_Alim.codAlim,
			tbConj_Alim.numQtd,
			tbAlim.strUnidade,
			tbAlim.strAlimento,
			tbAlim.numCaloria,
			tbConj_Alim.numQtd * tbAlim.numCaloria as qtdCalorias,
			tbAlim.numGrupo,
			tbAlim.booBebida,
			tbAlim.numTipo,
			tbAlim.numPeso
			FROM
			tbConj_Alim, tbAlim, tbConj
			WHERE
			tbConj_Alim.codigo > 0
			AND tbConj_Alim.codAlim = tbAlim.codigo
			AND tbConj_Alim.codConj = tbConj.codigo '''
		if checkBebida.active:
			if checkBebidaEstado.active:
				textSQL += 'AND booBebida = 1 '
			else:
				textSQL += 'AND booBebida = 0 '
		if checkAlimento.active:
			textSQL += 'AND strAlimento LIKE "%{0}%" '.format(txtAlimento.text)
		if checkGrupo.active:
			textSQL += 'AND numGrupo = {0} '.format(int(spinGrupo.text[0:2]))
		if checkTipo.active:
			textSQL += 'AND numTipo = {0} '.format(int(spinTipo.text[0:2]))
		textSQL += ') ' # Fecha os parenteses
		textSQL += 'Order By NumFreq Desc, strConjunto'
	
		rvConjunto.data = db.getListDictForTableRVFromTextSQL(textSQL)
		for dictD in rvConjunto.data:
			auxReceita, numCals = db.getReceitaFromCodConj(dictD['codigo'])
			dictD['text'] = '[b][color=ffd700]{0}[/color][/b]\n[i][color=ffff33]{1} = {2} Kcal[/color][/i]'.format(dictD['strConjunto'],auxReceita,numCals)
	
	def gerarTelaCC(self,*args):
		self.atualizaRVConjunto()
		lbAviso = self.ids['scCC_lbAviso']
		lbAviso.text = 'Escolha as receitas e clique em consumir'
		spinGrupo = self.ids['scCC_spinGrupo']
		spinTipo = self.ids['scCC_spinTipo']
		spinGrupo.values = db.listGrupoValues
		spinTipo.values = db.listTipoValues
				
	def consumir_click(self):
		rvConjunto = self.ids['scCC_rvReceitas']
		strConjs = ''
		for dictD in rvConjunto.data:
			if dictD['booSel'] == 1:
				db.append('tbHistConj',(db.sqlite3_DateForSQL(datetime.date.today()),0,dictD['codigo'],0,))
				db.tbConj_incNumFreq(dictD['codigo'])
				strConjs += dictD['strConjunto'] + ', '
				
		if strConjs != '':
			strConjs = strConjs[:-2]
			lbAviso = self.ids['scCC_lbAviso']
			lbAviso.text = 'Consumiu as receitas: ' + strConjs + '\n Escolha outras ou clique em voltar'
		
	def voltar_click(self):
		self.manager.transition = SlideTransition(direction="right")
		self.manager.current = 'scDietaDia'
					
class scCadAlim(Screen):
	hue = NumericProperty(0)

	def gerarTela(self,*args):
		rvTable = self.ids['scCadAlim_rvAlimentos']
		rvTable.data = db.getListDictForTableRVFromTbTable('tbAlim','')
		for dictD in rvTable.data:
			dictD['text'] = '[color=ffff33][b]' + dictD['strAlimento'] + '[/b] - Grupo ' + str(dictD['numGrupo']) + ' - Tipo ' + str(dictD['numTipo']) + '\n[i]1 ' + dictD['strUnidade'] + ' = ' + str(dictD['numCaloria']) + ' KCal[/i]' + '[/color]' 
		spinUnidade = self.ids['scCadAlim_spinUnidade']
		spinGrupo = self.ids['scCadAlim_spinGrupo']
		spinTipo = self.ids['scCadAlim_spinTipo']
		spinGrupo.values = db.listGrupoValues
		spinUnidade.values = db.listUnidadeValues
		spinTipo.values = db.listTipoValues

	def cadastrar_click(self):
		hab = False
		txtAlimento = self.ids['scCadAlim_txtAlimento']
		spinUnidade = self.ids['scCadAlim_spinUnidade']
		spinGrupo = self.ids['scCadAlim_spinGrupo']
		spinTipo = self.ids['scCadAlim_spinTipo']
		txtCaloria = self.ids['scCadAlim_txtCaloria']
		txtPeso = self.ids['scCadAlim_txtPeso']
		checkBebida = self.ids['scCadAlim_checkBebida']
		txtQuantidade = self.ids['scCadAlim_txtQuantidade']
		
		# Tenho que estudar como restringir entrada de textos e aceitar apenas numeros e etc...
		if txtAlimento.text != '':
			hab = True
		if hab:
			if checkBebida.active:
				nB = 1
			else:
				nB = 0
			db.insAlimUn(txtAlimento.text,spinUnidade.text,float(txtCaloria.text),int(spinGrupo.text[0:2]),nB,int(spinTipo.text[0:2]),float(txtPeso.text),int(txtQuantidade.text))
			rvTable = self.ids['scCadAlim_rvAlimentos']
			rvTable.data = db.getListDictForTableRVFromTbTable('tbAlim','')
			for dictD in rvTable.data:
				dictD['text'] = '[color=ffff33][b]' + dictD['strAlimento'] + '[/b] - Grupo ' + str(dictD['numGrupo']) + ' - Tipo ' + str(dictD['numTipo']) + '\n[i]1 ' + dictD['strUnidade'] + ' = ' + str(dictD['numCaloria']) + ' KCal[/i]' + '[/color]' 
	
class scCadConj(Screen):
	hue = NumericProperty(0)
	txtReceita = None	
	
	# Para os Alimentos e Suas Quantidades
	listCodNum = ListProperty([])
	listLbAlim = ListProperty([])
	listTxtQtd = ListProperty([])
	listLbUnid = ListProperty([])
	
	def gerarTela(self,*args):
		multiRV = self.ids['scCadConj_rvAlimentos']
		multiRV.data = db.getListDictForTableRVFromTbTable('tbAlim','')
		for dictD in multiRV.data:
			dictD['text'] = '[color=ffff33][b]' + dictD['strAlimento'] + '[/b] - Grupo ' + str(dictD['numGrupo']) + ' - Tipo ' + str(dictD['numTipo']) + '\n[i]1 ' + dictD['strUnidade'] + ' = ' + str(dictD['numCaloria']) + ' KCal[/i]' + '[/color]' 

	def gerarConjunto_click(self):
		# Falta  verificar se teve clicks e etc, mas por enquanto nao to preocupando com isso
		multiRV = self.ids['scCadConj_rvAlimentos']
		superBox = self.ids['scCadConj_Box_Quantidades']
		gridBox = self.ids['scCadConj_Grid_Quantidades']
		booPrimeiro = True
		superBox.clear_widgets()
		gridBox.clear_widgets()
		for dictD in multiRV.data:
			if dictD['booSel'] == 1:
				if booPrimeiro:
					booPrimeiro = False
					auxLb = Label(text='Nome da Receita:')
					self.txtReceita = TextInput(text='')
					superBox.add_widget(auxLb)
					superBox.add_widget(self.txtReceita)
			
				# Cria
				auxLbAlim = Label(text=dictD['strAlimento'])
				auxTxtQtd = TextInput(text='1')
				auxLbUnid = Label(text=dictD['strUnidade'])
				# Adiciona
				gridBox.add_widget(auxLbAlim)
				gridBox.add_widget(auxTxtQtd)
				gridBox.add_widget(auxLbUnid)
				# Guarda os objetos em listas
				self.listCodNum.append(dictD['codigo'])
				self.listLbAlim.append(auxLbAlim)
				self.listTxtQtd.append(auxTxtQtd)
				self.listLbUnid.append(auxLbUnid)	
	
	def incluirConjunto_click(self):
		print(self.txtReceita.text)
		for cod in self.listCodNum:
			print(cod)
			
class scHist(Screen):
	hue = NumericProperty(0)
	def gerarTela(self,*args):
		rvHistorico = self.ids['scHist_rvHistorico']
		rvHistorico.data = db.getListDictForTableRVFromTextSQL('Select * From tbHistConj')
		#lbAviso = self.ids['scHist_lbAviso']
		#lbAviso.text = 'Escolha as receitas e clique em consumir'
		
	# Historico que tiver codOpt = 0 é pq vc consumiu fora da Dieta	
	# Depois eu melhoro esse histórico criando o SQL 
	# Tenho que fazer as Horas aparecerem e funcionarem
	
	
		
	def consumir_click(self):
		pass
		
	def voltar_click(self):
		self.manager.transition = SlideTransition(direction="right")
		self.manager.current = 'scDietaDia'
	
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

		widScCadAlim = scCadAlim(name='scCadAlim')
		widScCadConj = scCadConj(name='scCadConj')
		
		widScHist  = scHist(name='scHist')
		widScRes  = scRes(name='scRes')
		widScAutor  = scAutor(name='scAutor')		
		
		listWidSc = [widScDietaDia,widScCCRef,widScCC,widScCadAlim,widScCadConj,widScHist,widScRes,widScAutor]
		for widsc in listWidSc:
			rSG.add_widget(widsc)
		return root

if __name__ == '__main__':
    mainDieta().run()