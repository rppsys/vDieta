#Cria a estrutura de banco de dados e insere os dados HARD CODED

import sqlite3
import datetime

import numpy as np
import pandas as pd

strDbFilename = "dbDieta.db"
dictTables = dict()

listTipoValues = [
	'00 - Natural e Saudável',
	'01 - Natural mas evitar',
	'02 - Natural mas proibido',
	'03 - Açucares',
	'04 - Dietéticos',
	'05 - Doces sem lactose',
	'06 - Doces com lactose',	
	'07 - Especiais'
	]

listGrupoValues = [
	'00 - Nenhum Grupo',
	'01 - Vegetais A',
	'02 - Vegetais B',
	'03 - Frutas Frescas',
	'04 - Carnes',
	'05 - Ovos',
	'06 - Gorduras',
	'07 - Cereais e Vegetais C',
	'08 - Leguminosas',
	'09 - Leites e Derivados',
	'10 - Queijos',
	'11 - Embutidos',
	'12 - Castanhas e Oleaginosas',
	'13 - Frutas Secas',
	'14 - Grãos e Farinhas'		
	]
		
listUnidadeValues = [
	'unid',
	'fatia',
	'porção',
	'barra',
	'col de sopa',
	'col de chá',
	'concha P',
	'concha M',
	'concha G',
	'xícara de chá',
	'copo de 300 ml',
	'copo de 500 ml'
	]
		
hl_a = []
hl_c = []
hl_o = []

################################################################################
								# Funções Auxiliares Banco de Dados
################################################################################
def nC(tbTable):
	# Verifica maior codigo da tabela tbTable e retorna esse codido incrementado de 1
    conn=sqlite3.connect(strDbFilename)
    cur=conn.cursor()
    cur.execute("SELECT MAX(codigo) FROM " + tbTable)
    row = cur.fetchone()
    conn.close()
    if row[0] == None:
        return 1
    else:
        return row[0] + 1

		
def getDataHoje():
	return datetime.date.today()
		
def getDataAgora():
	return datetime.date(datetime.datetime.today().year,datetime.datetime.today().month,datetime.datetime.today().day)

def getHoraAgora():
	return datetime.datetime(2001,1,1,datetime.datetime.today().hour,datetime.datetime.today().minute,datetime.datetime.today().second)
	
def getDataHoraHoje():
	return datetime.datetime.today()

def makeData(d,m,y): #Retorna um objeto do tipo datetime.date
	return datetime.date(y,m,d)

def makeHora(h,m,s): #Retorna um objeto do tipo datetime.time
	return datetime.datetime(2001,1,1,h,m,s)
	
def sqlite3_DateForSQL(dtData): #Pega um objeto do tipo datetime e converte para strSQL
	strRet = "'{0:04}-{1:02}-{2:02}'".format(dtData.year,dtData.month,dtData.day)
	return strRet
	
def sqlite3_TimeForSQL(hrHora): #Pega um objeto do tipo datetime e converte para strSQL
	strRet = "'2001-01-01 {0:02}:{1:02}:{2:02}'".format(hrHora.hour,hrHora.minute,hrHora.second)
	return strRet

def getStrData(d,m,y): #Retorna uma string contendo a data 
	return sqlite3_DateForSQL(makeData(d,m,y))
	
def getStrHora(h,m,s): #Retorna uma string contendo a hora
	return sqlite3_TimeForSQL(makeHora(h,m,s))

def getStrDataAgora(): #Retorna uma string contendo a data de agora
	return sqlite3_DateForSQL(getDataAgora())
	
def getStrHoraAgora(): #Retorna uma string contendo a hora de agora
	return sqlite3_TimeForSQL(getHoraAgora())
	
def strHrBr(strObjHora):
	# 'YYYY-MM-DD HH:MM:SS
	strH = strObjHora[11:13]
	strM = strObjHora[14:16]
	strRet = strH + 'h' + strM
	return strRet
	
def getWeekDay(dtData):
	'Domingo começa em 1 até sábado igual a 7'
	numRet = dtData.isoweekday() + 1
	if numRet == 8:
		numRet = 1
	return numRet

def retDtInicioFinalFromDtData(dtData,charTipo):
	dtInicio = dtData
	dtFinal = dtData
	if charTipo == 'S':
		nW = getWeekDay(dtData)
		dtInicio = dtData - datetime.timedelta(nW-1)
		dtFinal = dtData + datetime.timedelta(7 - nW)
	elif charTipo == 'M':
		# Fabrica dtInicio
		dtInicio = makeData(1,dtData.month,dtData.year)

		#Fabrica dtFinal
		proxMes = dtData.month + 1
		if proxMes == 13:
			proxMes = 1
		dtFinal = makeData(1,proxMes,dtData.year)
		dtFinal = dtFinal - datetime.timedelta(1)
	elif charTipo == '2':
		nW = getWeekDay(dtData)
		dtInicio = dtData - datetime.timedelta(nW-1)
		dtInicio = dtInicio - datetime.timedelta(7)
		dtFinal = dtData + datetime.timedelta(7 - nW)
	elif charTipo == 'D': 
		dtInicio = dtData
		dtFinal = dtData
	else:
		nW = getWeekDay(dtData)
		dtInicio = dtData - datetime.timedelta(nW-1)
		dtFinal = dtData + datetime.timedelta(7 - nW)
	return dtInicio, dtFinal
	

def dateToBrStr(dtData): #Pega um objeto do tipo date e converte para String no Formato Brasileiro
	strRet = "{0:02}/{1:02}/{2:04}".format(dtData.day,dtData.month,dtData.year)
	return strRet

	
def habStrData(strData):
	ret = False
	try:
		dtData = datetime.datetime.strptime(strData, '%d/%m/%Y')
		ret = True
	except ValueError:
		ret = False
	return ret


def retDtDataFromStrData(strData):
	dtData = datetime.date(datetime.datetime.today().year,datetime.datetime.today().month,datetime.datetime.today().day) 
	if habStrData(strData):
		dtData = datetime.datetime.strptime(strData,'%d/%m/%Y')
	return datetime.date(dtData.year,dtData.month,dtData.day)
	
	
################################################################################
								# Funções para Teste do Código
################################################################################

		
def mostrarTabela(tbTable):
	df = retPandasDfFromSQL('Select * From ' + tbTable)
	print("")
	print("....................")
	print(tbTable)
	print("....................")
	display(df)
	print("-------------------")
	return df
				
def mostrarTodasTabelas():
	global dictTables
	for i,k in dictTables.items():
		df = retPandasDfFromSQL('Select * From ' + i)
		print("")
		print("....................")
		print(i)
		print("....................")
		display(df)
		print("-------------------")
		
def retPandasDfFromSQL(textSQL):
	conn=sqlite3.connect(strDbFilename)
	cur=conn.cursor()
	cur.execute(textSQL)
	colnames = [description[0] for description in cur.description]
	rows=cur.fetchall()
	retDF = pd.DataFrame.from_records(rows,columns=colnames)
	retDF.index = retDF['codigo']
	retDF.drop('codigo',axis=1,inplace=True)
	return retDF
	
def getRefFromPlanDia(codPlan,diaSemana):	
	textSQL = '''
	SELECT
	tbPlan_Ref.codigo as codigo,
	tbRef.strRefeicao,
	tbRef.hrHora,
	tbPlan_Ref.codRef
	FROM
	tbPlan_Ref, tbRef
	WHERE
	tbPlan_Ref.codPlan > 0
	AND tbRef.codigo = tbPlan_Ref.codRef
	AND tbPlan_Ref.codPlan = ''' + str(codPlan) + ' ' + '''
	AND tbPlan_Ref.diaSemana = ''' + str(diaSemana)	
	df = retPandasDfFromSQL(textSQL)
	display(df)

def inicializar(drop,gera):
	global dictTables
	defineTables()
	if drop:
		dropAllTables()
	if gera:
		gerarDB()
		print('Novo banco de dados criado')

def reset():
	dropTable('tbHistOpt')
	dropTable('tbHistConj')
	dropTable('tbConfig')

		
################################################################################
								# Funções Principais Banco de Dados
################################################################################

def defineTables():
	global dictTables
	dictAuxFields = dict()
	#----------------------------------------
	# Tabela Alimento
	#----------------------------------------
	strAuxTable = 'tbAlim'
	dictAuxFields = {
	'strAlimento':'TEXT',
	'strUnidade':'TEXT',
	'numCaloria':'REAL',
	'numGrupo':'INTEGER',
	'booBebida':'INTEGER',
	'numTipo':'INTEGER',
	'numPeso':'REAL'
	}
	dictTables[strAuxTable] = dictAuxFields
	#----------------------------------------
	# Tabela Conjunto
	#----------------------------------------
	strAuxTable = 'tbConj'
	dictAuxFields = {
	'strConjunto':'TEXT',
	'numFreq':'INTEGER'
	}
	dictTables[strAuxTable] = dictAuxFields
	#----------------------------------------
	# Tabela Vinculo Conj_Alim
	#----------------------------------------
	strAuxTable = 'tbConj_Alim'
	dictAuxFields = {
	'codConj':'INTEGER',
	'codAlim':'INTEGER',
	'numQtd':'INTEGER'
	}
	dictTables[strAuxTable] = dictAuxFields
	#----------------------------------------	
	# Tabela Opcao
	#----------------------------------------
	strAuxTable = 'tbOpt'
	dictAuxFields = {
	'strOpt':'TEXT'
	}
	dictTables[strAuxTable] = dictAuxFields
	#----------------------------------------
	# Tabela Vinculo Opt_Conj
	#----------------------------------------
	strAuxTable = 'tbOpt_Conj'
	dictAuxFields = {
	'codOpt':'INTEGER',
	'codConj':'INTEGER'
	}
	dictTables[strAuxTable] = dictAuxFields
	#----------------------------------------
	# Tabela Refeicao
	#----------------------------------------
	strAuxTable = 'tbRef'
	dictAuxFields = {
	'strRefeicao':'TEXT',
	'hrHora':'TEXT'
	}
	dictTables[strAuxTable] = dictAuxFields
	#----------------------------------------
	# Tabela Vinculo Ref_Opt
	#----------------------------------------
	strAuxTable = 'tbRef_Opt'
	dictAuxFields = {
	'codRef':'INTEGER',
	'codOpt':'INTEGER'
	}
	dictTables[strAuxTable] = dictAuxFields
	#----------------------------------------
	# Tabela Plano
	#----------------------------------------
	strAuxTable = 'tbPlan'
	dictAuxFields = {
	'dataCria':'TEXT',
	'dataInicio':'TEXT',
	'dataFinal':'TEXT'
	}
	dictTables[strAuxTable] = dictAuxFields
	#----------------------------------------
	# Tabela Vinculo Plan_Ref
	#----------------------------------------
	strAuxTable = 'tbPlan_Ref'
	dictAuxFields = {
	'codPlan':'INTEGER',
	'codRef':'INTEGER',
	'diaSemana':'INTEGER'
	}
	dictTables[strAuxTable] = dictAuxFields
	#----------------------------------------
	# Tabela Histórico de Opt
	#----------------------------------------
	strAuxTable = 'tbHistOpt'
	dictAuxFields = {
	'dtData':'TEXT',
	'hrHora':'TEXT',
	'strRefeicao':'TEXT',
	'codOpt':'INTEGER',
	'booC':'INTEGER'
	}
	dictTables[strAuxTable] = dictAuxFields
	#----------------------------------------
	# Tabela Histórico de Conj
	#----------------------------------------
	strAuxTable = 'tbHistConj'
	dictAuxFields = {
	'dtData':'TEXT',
	'hrHora':'TEXT',
	'codConj':'INTEGER',
	'codOpt':'INTEGER'
	}
	dictTables[strAuxTable] = dictAuxFields
	#----------------------------------------
	# Tabela Configurações
	#----------------------------------------
	strAuxTable = 'tbConfig'
	dictAuxFields = {
	'strKey':'TEXT',
	'strValue':'TEXT'
	}
	dictTables[strAuxTable] = dictAuxFields
	
def gerarDB():
	conn=sqlite3.connect(strDbFilename)
	cur=conn.cursor()
	for strTable,dictAuxFields in dictTables.items():
		strExec = 'CREATE TABLE IF NOT EXISTS ' + strTable + ' ('
		strExec += 'codigo INTEGER PRIMARY KEY, '
		for strField,strType in dictAuxFields.items():
			strExec += strField + ' ' + strType + ', '
		strExec = strExec[:-2] #Tira último ", "
		strExec += ')'
		cur.execute(strExec)
	# Commita tudo
	conn.commit()
	#print('Tabelas criadas')
	
def dropAllTables():
	global dictTables
	conn=sqlite3.connect(strDbFilename)
	cur=conn.cursor()
	for strTable,dictAuxFields in dictTables.items():
		strExec = 'DROP TABLE ' + strTable
		cur.execute(strExec)
	# Commita tudo
	conn.commit()
	print('Tabelas antigas dropadas')
	
def dropTable(tbTable):
	global dictTables
	conn=sqlite3.connect(strDbFilename)
	cur=conn.cursor()
	strExec = 'DROP TABLE ' + tbTable
	cur.execute(strExec)
	conn.commit()
	print('Tabela {0} dropada'.format(tbTable))
		
def append(tbTable,tValues):
	'''
	db.append('tbAlim',('Pão',10,5,))
	db.append('tbConj',('Sanduiche',))
	Ou seja, tem que dar a tupla e terminar com um ,
	'''
	global dictTables
	hab = False
	# Valida
	if tbTable in dictTables:
		if len(tValues) == len(dictTables[tbTable]):
			hab = True
		else:
			print('Erro no append {0}: Numero de itens da tupla difere do dictTables'.format(tbTable))
	else:
		print('Erro no append: Tabela não existe')
	# Passou nos testes
	if hab:
		nCod = nC(tbTable)
		strQ = '?,'*len(tValues)
		strQ = strQ[:-1]
		textSQL = 'INSERT INTO ' + tbTable + ' VALUES (' + str(nCod) + ',' + strQ + ')'
		conn=sqlite3.connect(strDbFilename)
		cur=conn.cursor()
		cur.execute(textSQL,tValues)
		conn.commit() 
		return nCod
	else:
		return -1

def appendLtValues(tbTable,ltValues): #Não vou usar, deixei aqui apenas por referencia
	'''
	
	db.append('tbAlim',[('Pão',10,5,)])
	db.append('tbConj',[('Sanduiche',)])
	Ou seja, tem que dar a lista de tuplas com uma unica tupla e terminar com um ,
	'''
	global dictTables
	hab = False
	# Valida
	if tbTable in dictTables:
		if len(ltValues) == 1:
			if len(ltValues[0]) == len(dictTables[tbTable]):
				hab = True
			else:
				print('Erro no append: Numero de itens difere do dictTables')
		else:
			print('Erro no append: ltValues possui mais de uma tupla')
	else:
		print('Erro no append: Tabela não existe')
	# Passou nos testes
	if hab:
		nCod = nC(tbTable)
		strQ = '?,'*len(ltValues[0])
		strQ = strQ[:-1]
		textSQL = 'INSERT INTO ' + tbTable + ' VALUES (' + str(nCod) + ',' + strQ + ')'
		conn=sqlite3.connect(strDbFilename)
		cur=conn.cursor()
		cur.execute(textSQL,ltValues[0])
		conn.commit() 
		return nCod
	else:
		return -1
		
def view(tbTable):
	conn=sqlite3.connect(strDbFilename)
	cur=conn.cursor()
	cur.execute("SELECT * FROM " + tbTable)
	rows=cur.fetchall()
	conn.close()
	return rows

def hardInsReset():
	global hl_a
	global hl_c
	global hl_o
	hl_a = []
	hl_c = []
	hl_o = []
	
def insAlimUn(strAlimento,strUnidade,numCaloria,numGrupo,booBebida,numTipo,numPeso,numQtd):
	global hl_a
	global hl_c
	global hl_o
	a = append('tbAlim',(strAlimento,strUnidade,numCaloria,numGrupo,booBebida,numTipo,numPeso,))
	c = append('tbConj',(strAlimento + ' (' + str(numQtd) + ' ' + strUnidade + ')',0,))
	append('tbConj_Alim',(c,a,numQtd,))
	o = append('tbOpt',(strAlimento + ' (' + str(numQtd) + ' ' + strUnidade + ')',))
	append('tbOpt_Conj',(o,c))	
	hl_a.append(a)
	hl_c.append(c)
	hl_o.append(o)
	return a,c,o

def insAlimUnG(numGrupo,strAlimento,numPeso,numQtd,strUnidade,numTipo):
	return insAlimUn(strAlimento,strUnidade,0,numGrupo,0,numTipo,numPeso,numQtd)

def inserirAlimentosNutricionista():
	# Grupo 1 - Vegetais A
	insAlimUn('Vegetal A','unid',0,1,0,0,0,1)
	insAlimUn('Folha de Acelga','unid',0,1,0,0,0,1)
	insAlimUn('Folha de Agrião','unid',0,1,0,0,0,1)
	insAlimUn('Folha de Alface','unid',0,1,0,0,0,1)
	insAlimUn('Folha de Almeirão','unid',0,1,0,0,0,1)
	insAlimUn('Folha de Bertalha','unid',0,1,0,0,0,1)
	insAlimUn('Folha de Chicória','unid',0,1,0,0,0,1)
	insAlimUn('Folha de Couve de Bruxelas','unid',0,1,0,0,0,1)
	insAlimUn('Folha de Couve manteiga','unid',0,1,0,0,0,1)
	insAlimUn('Folha de Endívia','unid',0,1,0,0,0,1)
	insAlimUn('Folha de Escarola','unid',0,1,0,0,0,1)
	insAlimUn('Folha de Espinafre','unid',0,1,0,0,0,1)
	insAlimUn('Folha de Mostarda','unid',0,1,0,0,0,1)
	insAlimUn('Folha de Repolho','unid',0,1,0,0,0,1)
	insAlimUn('Folha de Rúcula','unid',0,1,0,0,0,1)
	insAlimUn('Folha de Salsão','unid',0,1,0,0,0,1)
	insAlimUn('Folha de Taioba','unid',0,1,0,0,0,1)
	insAlimUn('Abobrinha','unid',0,1,0,0,0,1)
	insAlimUn('Aipo','unid',0,1,0,0,0,1)
	insAlimUn('Alcachofra-coração','unid',0,1,0,0,0,1)
	insAlimUn('Aspargos','unid',0,1,0,0,0,1)
	insAlimUn('Berinjela','unid',0,1,0,0,0,1)
	insAlimUn('Brócolis','unid',0,1,0,0,0,1)
	insAlimUn('Broto de feijão','unid',0,1,0,0,0,1)
	insAlimUn('Broto de Alfafa','unid',0,1,0,0,0,1)
	insAlimUn('Cebola','unid',0,1,0,0,0,1)
	insAlimUn('Cogumelo fresco','unid',0,1,0,0,0,1)
	insAlimUn('Couve-flor','unid',0,1,0,0,0,1)
	insAlimUn('Jiló','unid',0,1,0,0,0,1)
	insAlimUn('Maxixe','unid',0,1,0,0,0,1)
	insAlimUn('Nabo','unid',0,1,0,0,0,1)
	insAlimUn('Palmito','unid',0,1,0,0,0,1)
	insAlimUn('Pepino','unid',0,1,0,0,0,1)
	insAlimUn('Rabanete','unid',0,1,0,0,0,1)
	insAlimUn('Tomate','unid',0,1,0,0,0,1)
	# Grupo 2 - Vegetais B
	insAlimUn('Vegetal B','col de sopa',0,2,0,0,0,4)
	insAlimUn('Abóbora','col de sopa',0,2,0,0,0,4)
	insAlimUn('Beterraba','col de sopa',0,2,0,0,0,4)
	insAlimUn('Cenoura','col de sopa',0,2,0,0,0,4)
	insAlimUn('Chuchu','col de sopa',0,2,0,0,0,4)
	insAlimUn('Pimentão','col de sopa',0,2,0,0,0,4)
	insAlimUn('Quiabo','col de sopa',0,2,0,0,0,4)
	insAlimUn('Vagem','col de sopa',0,2,0,0,0,4)
	# Grupo 3 Fruta Fresca - OK
	insAlimUnG(3,'Fruta Fresca',0,1,'fatia',0)
	insAlimUnG(3,'Abacaxi',100,2,'fatias P',0)
	insAlimUnG(3,'Laranja',180,1,'unid M',0)
	insAlimUnG(3,'Acerola',84,7,'unid',0)
	insAlimUnG(3,'Lichia',100,10,'unid',0)
	insAlimUnG(3,'Ameixa',68,2,'unid P',0)
	insAlimUnG(3,'Maça',130,1,'unid M',0)
	insAlimUnG(3,'Amora',50,1,'meio copo',0)
	insAlimUnG(3,'Mamão formosa',170,1,'fatia M',0)
	insAlimUnG(3,'Banana d’água',35,1,'meia unid M',0)
	insAlimUnG(3,'Mamão papaia',135,1,'meia unid M',0)
	insAlimUnG(3,'Banana (maçã ou prata)',50,1,'unid M',0)
	insAlimUnG(3,'Manga',60,1,'unid P',0)
	insAlimUnG(3,'Cajá manga',55,1,'unid M',0)
	insAlimUnG(3,'Maracujá',45,1,'unid M',0)
	insAlimUnG(3,'Cajú',200,2,'unid M',0)
	insAlimUnG(3,'Melancia',100,1,'fatia M',0)
	insAlimUnG(3,'Caqui',110,1,'unid M',0)
	insAlimUnG(3,'Melão',115,1,'fatia G',0)
	insAlimUnG(3,'Carambola',130,1,'unid G',0)
	insAlimUnG(3,'Morango',120,10,'unid M',0)
	insAlimUnG(3,'Cereja',50,7,'undiades M',0)
	insAlimUnG(3,'Nectarina',100,1,'unid M',0)
	insAlimUnG(3,'Figo',100,2,'unid M',0)
	insAlimUnG(3,'Nêspera',180,3,'unid G',0)
	insAlimUnG(3,'Framboesa',50,3,'col de sopa',0)
	insAlimUnG(3,'Pêra',110,1,'unid M',0)
	insAlimUnG(3,'Fruta do conde',60,1,'unid M',0)
	insAlimUnG(3,'Pêssego',60,1,'unid M',0)
	insAlimUnG(3,'Graviola',50,1,'unid M',0)
	insAlimUnG(3,'Pitanga',100,12,'unid',0)
	insAlimUnG(3,'Goiaba',170,1,'unid M',0)
	insAlimUnG(3,'Pitaya',50,1,'meia unid M',0)
	insAlimUnG(3,'Jabuticaba',100,20,'unid',0)
	insAlimUnG(3,'Tangerina',135,1,'unid M',0)
	insAlimUnG(3,'Jaca',30,3,'gomos G',0)
	insAlimUnG(3,'Uva',80,10,'bagos',0)
	insAlimUnG(3,'Jambo',120,2,'unid G',0)
	insAlimUnG(3,'Salada de frutas',250,1,'copo americano',0)
	insAlimUnG(3,'Kiwi',76,1,'unid M',0)
	# Grupo 4 - GRUPO DAS CARNES - OK
	insAlimUnG(4,'Almôndega (Carne, frango ou soja)',100,2,'unid M',0)
	insAlimUnG(4,'Frango desfiado',100,2,'col de sopa',0)
	insAlimUnG(4,'Atum',100,4,'col de sopa',0)
	insAlimUnG(4,'Hambúrguer caseiro (bovino,soja, suíno, frango)',56,1,'unid M',0)
	insAlimUnG(4,'Bife (bovino, soja, suino)',100,1,'unid M',0)
	insAlimUnG(4,'Quibe (assado ou cru)',100,2,'pedaços M',0)
	insAlimUnG(4,'Carne assada (bovino, soja, suino)',90,1,'fatia M',0)
	insAlimUnG(4,'Peito – bife / filé (frango, peru)',100,1,'filé M',0)
	insAlimUnG(4,'Carne em cubos (bovino, suino)',120,4,'col de sopa',0)
	insAlimUnG(4,'Peixe',120,1,'posta ou 1 filé G',0)
	insAlimUnG(4,'Carne moída',120,3,'col de sopa',0)
	insAlimUnG(4,'Polvo',120,4,'col de sopa',0)
	insAlimUnG(4,'Coxa de frango',75,3,'unid P',0)
	insAlimUnG(4,'Sardinha',85,4,'unid M',0)
	insAlimUnG(4,'Espeto de carne magra (churrasquinho)',100,2,'unid',0)
	insAlimUnG(4,'Espeto de frango (churrasquinho)',100,2,'unid',0)
	insAlimUnG(4,'Sobrecoxa de frango',65,1,'unid M',0)
	#Grupo 5 - GRUPO DOS OVOS - OK
	insAlimUnG(5,'Ovo de codorna',50,5,'unid',0)
	insAlimUnG(5,'Ovo de galinha',60,1,'unid',0)
	#Grupo 6 - Gorduras
	insAlimUnG(6,'Azeite de Oliva',5,1,'col de chá',1)
	insAlimUnG(6,'Óleo de Coco',5,1,'col de chá',1)
	insAlimUnG(6,'Becel',5,1,'col de chá',1)	
	#Grupo 7 - GRUPO DOS VEGETAIS ‘C’ / CEREAIS - OK
	insAlimUnG(7,'Vegetal C',40,2,'col sopa',0)
	insAlimUnG(7,'Arroz',40,2,'col sopa',0)
	insAlimUnG(7,'Arroz Integral',40,2,'col sopa',0)
	insAlimUnG(7,'Batata baroa',70,2,'col sopa',0)
	insAlimUnG(7,'Biscoito de arroz integral',30,5,'unid',0)
	insAlimUnG(7,'Batata doce',84,2,'col sopa',0)
	insAlimUnG(7,'Biscoito de polvilho / Peta',15,10,'unid',0)
	insAlimUnG(7,'Batata inglesa',60,2,'col sopa',0)
	insAlimUnG(7,'Cuscuz',85,4,'col sopa',0)
	insAlimUnG(7,'Cará',70,3,'col de sopa',0)
	insAlimUnG(7,'Farelo de trigo',18,2,'col sopa',0)
	insAlimUnG(7,'Farelo de mandioca',18,2,'col sopa',0)
	insAlimUnG(7,'Inhame',105,3,'col de sopa',0)
	insAlimUnG(7,'Granola sem açúcar',50,3,'col de sopa',0)
	insAlimUnG(7,'Mandioca',60,2,'col sopa',0)
	insAlimUnG(7,'Macarrão integral',110,1,'escumadeira',0)
	insAlimUnG(7,'Milho verde',100,1,'espiga M',0)
	insAlimUnG(7,'Pão árabe / sírio integral',50,1,'unid M',0)
	insAlimUnG(7,'Pão de forma integral',50,1,'fatia',0)
	insAlimUnG(7,'Pão Francês',50,1,'metade',0)
	insAlimUnG(7,'Pipoca (milho cru)',20,1,'xícara',0)
	insAlimUnG(7,'Polenta',80,2,'col sopa',0)
	insAlimUnG(7,'Tapioca (Goma hidratada)',80,4,'col de sopa',0)
	#Grupo 8 – GRUPO DAS LEGUMINOSAS - OK
	insAlimUnG(8,'Ervilha seca cozida',60,1,'concha P',0)
	insAlimUnG(8,'Lentilha cozida',54,3,'col de sopa',0)
	insAlimUnG(8,'Feijão cozido',65,1,'concha P',0)
	insAlimUnG(8,'Soja cozida',70,3,'col de sopa',0)
	insAlimUnG(8,'Grão de bico cozido',66,3,'col de sopa',0)
	#Grupo 9 - GRUPO DOS LEITES E DERIVADOS - OK
	insAlimUnG(9,'Iogurte natural',120,1,'unid',1)
	insAlimUnG(9,'Leite em pó',200,1,'copo M',1)
	insAlimUnG(9,'Leite integral ou desnatado',200,1,'copo M',1)
	insAlimUnG(9,'Leite (cereais, castanhas, soja)',200,1,'copo M',0)
	#Grupo 10 - GRUPO DOS QUEIJOS - OK
	insAlimUnG(10,'Queijo Cottage',50,3,'col de sopa',0)
	insAlimUnG(10,'Queijo Ricota',30,1,'fatia G',0)
	insAlimUnG(10,'Queijo Minas frescal',30,1,'fatia M',0)
	insAlimUnG(10,'Queijo Tofu',30,1,'fatia M',0)
	insAlimUnG(10,'Queijo Prata',30,1,'fatia M',0)
	insAlimUnG(10,'Queijo Mussarela',30,1,'fatia M',0)
	#Grupo 11 - EMBUTIDOS - OK
	insAlimUnG(11,'Blanquet de peru',5,1,'fatia',1)
	insAlimUnG(11,'Peito de peru defumado',5,1,'fatia',1)
	insAlimUnG(11,'Presunto',5,1,'fatia',1)
	insAlimUnG(11,'Salame',5,1,'fatia',1)
	#Grupo 12 - GRUPO DAS CASTANHAS E OLEAGINOSAS - OK
	insAlimUnG(12,'Amêndoa',25,25,'unid',0)
	insAlimUnG(12,'Abacate',185,1,'meia unid P',0)
	insAlimUnG(12,'Amendoin',28,35,'unid',0)
	insAlimUnG(12,'Açaí',200,1,'copo / 1 polpa',0)
	insAlimUnG(12,'Avelã',20,20,'unid',0)
	insAlimUnG(12,'Coco verde',60,1,'unid',0)
	insAlimUnG(12,'Castanha de caju',48,12,'unid',0)
	insAlimUnG(12,'Coco maduro',130,1,'pedaço P',0)
	insAlimUnG(12,'Castanha de Baru',30,3,'unid',0)
	insAlimUnG(12,'Semente de abóbora',30,2,'col de sopa',0)
	insAlimUnG(12,'Castanha do Pará',12,3,'unid',0)
	insAlimUnG(12,'Semente de girassol',30,2,'col de sopa',0)
	insAlimUnG(12,'Macadâmia',20,10,'unid',0)
	insAlimUnG(12,'Noz',50,10,'unid',0)
	insAlimUnG(12,'Pasta integral de castanhas',30,1,'col de sopa',0)
	insAlimUnG(12,'Pinhão',30,3,'unid',0)
	insAlimUnG(12,'Pistache',25,34,'unid',0)
	#Grupo 13 - GRUPO DAS FRUTAS SECAS / DESIDRATADAS - OK
	insAlimUnG(13,'Fruta Seca',20,1,'unid',0)
	insAlimUnG(13,'Abacaxi desidratado',20,1,'xícara de chá',0)
	insAlimUnG(13,'Damasco seco',28,4,'unid',0)
	insAlimUnG(13,'Ameixa seca',25,5,'unid',0)
	insAlimUnG(13,'Figo seco',30,1,'unid',0)
	insAlimUnG(13,'Banana desidratada',10,0.5,'meia xícara chá',0)
	insAlimUnG(13,'Maçã desidratada',25,1,'meia xícara de chá',0)
	insAlimUnG(13,'Banana passa',10,1,'unid',0)
	insAlimUnG(13,'Manga desidratada',20,1,'xícara de chá',0)
	insAlimUnG(13,'Barra de fruta',23,1,'barra',0)
	insAlimUnG(13,'Tâmara seca',60,2,'unid',0)
	insAlimUnG(13,'Blueberry',34,2,'col de sopa',0)
	insAlimUnG(13,'Cramberry',34,2,'col de sopa',0)
	insAlimUnG(13,'Gojiberry',34,2,'col de sopa',0)
	insAlimUnG(13,'Gold Berry',34,2,'col de sopa',0)
	insAlimUnG(13,'Uva passa',36,2,'col de sopa',0)
	#Grupo 14 – GRUPO DAS FIBRAS - OK
	insAlimUnG(14,'Amaranto',20,2,'col de sopa',0)
	insAlimUnG(14,'Gergelim',20,2,'col de sopa',0)
	insAlimUnG(14,'Aveia (farelo, farinha, flocos)',36,2,'col de sopa',0)
	insAlimUnG(14,'Quinoa',20,2,'col de sopa',0)
	insAlimUnG(14,'Chia',20,2,'col de sopa',0)
	insAlimUnG(14,'Linhaça',20,2,'col de sopa',0)
	
def inserirAlimentosOrdinarios():
	#Bebidas
	insAlimUn('Água','ml',0,0,1,0,0,100)							
	insAlimUn('Água de coco','ml',0,0,1,0,0,300)							
	insAlimUn('Café','ml',0,0,1,0,0,100)
	insAlimUn('Suco de Fruta','ml',0,0,1,0,0,300)
	insAlimUn('Refrigerante','ml',0,0,1,2,0,300)

	#Doces sem Lactose Tipo 5
	insAlimUn('Maria mole','unid',0,0,0,5,0,1)							
	insAlimUn('Suspiro','unid',0,0,0,5,0,1)							
	insAlimUn('Fatia de bolo s/ lactose','unid',0,0,0,5,0,1)							
	insAlimUn('Chocolate s/ lactose','tablet',0,0,0,5,0,1)									
	insAlimUn('Maple Syrup','col de sopa',0,0,0,5,0,1)									
	insAlimUn('Geléia','col de sopa',0,0,0,5,0,1)									
	
	#Doces com Lactose Tipo 6
	insAlimUn('Fatia de bolo c/ lactose','unid',0,0,0,6,0,1)							
	insAlimUn('Chocolate c/ lactose','tablet',0,0,0,6,0,1)								
	insAlimUn('Bombom','unid',0,0,0,6,0,1)								
	
	# Açucares Tipo 3
	insAlimUn('Açucar cristal','col de chá',0,0,0,3,0,1)
	insAlimUn('Açucar mascavo','col de chá',0,0,0,3,0,1)
	insAlimUn('Açucar demerara','col de chá',0,0,0,3,0,1)
	insAlimUn('Açucar cristal','col de sopa',0,0,0,3,0,1)
	insAlimUn('Açucar mascavo','col de sopa',0,0,0,3,0,1)
	insAlimUn('Açucar demerara','col de sopa',0,0,0,3,0,1)

	# Dietéticos Tipo 4
	insAlimUn('Sucralose','gota',0,0,1,4,0,1)
	insAlimUn('Stévia','gota',0,0,1,4,0,1)
	insAlimUn('Xilitol','col de chá',0,0,0,4,0,1)
	
	# Especiais
	insAlimUn('Lactase','comprimido 10.000 FCC ALU',0,0,0,7,0.5,1)
	
def inserirPlanoPadrao():
	append('tbPlan',(getDataAgora(),makeData(12,4,2018),makeData(12,7,2018),))

def inserirRefeicoesPadrao():
	append('tbRef',('DESJEJUM',makeHora(7,0,0),))
	append('tbRef',('COLAÇÃO',makeHora(10,0,0),))
	append('tbRef',('ALMOÇO',makeHora(12,0,0),))
	append('tbRef',('LANCHE',makeHora(15,0,0),))
	append('tbRef',('PRE-TREINO A',makeHora(17,30,0),))
	append('tbRef',('INTRA-TREINO',makeHora(18,30,0),))
	append('tbRef',('POS-TREINO',makeHora(21,50,0),))
	append('tbRef',('JANTAR A',makeHora(22,0,0),))
	append('tbRef',('PRE-DORMIR',makeHora(23,0,0),))
	append('tbRef',('PRE-TREINO B',makeHora(17,30,0),))	
	append('tbRef',('JANTAR B',makeHora(22,0,0),))
	
def inserirConjuntosRonie():
	tomate,a,b = insAlimUn('Tomate','fatia',0,1,0,0,0,1)
	kefir,a,b = insAlimUn('Kefir','ml',0,0,1,7,0,1)

	c = append('tbConj',('Sanduiche de Frango 1',0,))
	append('tbConj_Alim',(c,124,2,)) #Pão
	append('tbConj_Alim',(c,85,2,)) #Frango
	append('tbConj_Alim',(c,103,2,)) #Azeite
	append('tbConj_Alim',(c,1,1,)) #Vegetal A
	append('tbConj_Alim',(c,36,1,)) #Vegetal B
	o = append('tbOpt',('Sanduiche de Frango 1',))
	append('tbOpt_Conj',(o,c,))	

	c = append('tbConj',('Presunto Quente',0,))
	append('tbConj_Alim',(c,124,2,)) #Pão
	append('tbConj_Alim',(c,146,1,)) #Presunto
	append('tbConj_Alim',(c,103,4,)) #Azeite
	o = append('tbOpt',('Presunto Quente',))
	append('tbOpt_Conj',(o,c,))	
	
	c = append('tbConj',('Peru Quente',0,))
	append('tbConj_Alim',(c,124,2,)) #Pão
	append('tbConj_Alim',(c,145,1,)) #Peru
	append('tbConj_Alim',(c,103,4,)) #Azeite
	o = append('tbOpt',('Peru Quente',))
	append('tbOpt_Conj',(o,c,))	
	
	c = append('tbConj',('Blanquet Quente',0,))
	append('tbConj_Alim',(c,124,2,)) #Pão
	append('tbConj_Alim',(c,144,1,)) #Blanquet
	append('tbConj_Alim',(c,103,4,)) #Azeite
	o = append('tbOpt',('Blanquet Quente',))
	append('tbOpt_Conj',(o,c,))	

	c = append('tbConj',('Bauru s/ queijo',0,))
	append('tbConj_Alim',(c,124,2,)) #Pão
	append('tbConj_Alim',(c,145,1,)) #Peru
	append('tbConj_Alim',(c,103,4,)) #Azeite
	append('tbConj_Alim',(c,tomate,4,)) #Fatia de Tomate
	o = append('tbOpt',('Bauru s/ queijo',))
	append('tbOpt_Conj',(o,c,))	

	c = append('tbConj',('Bauru',0,))
	append('tbConj_Alim',(c,124,2,)) #Pão
	append('tbConj_Alim',(c,145,1,)) #Peru
	append('tbConj_Alim',(c,103,4,)) #Azeite
	append('tbConj_Alim',(c,tomate,4,)) #Fatia de Tomate
	append('tbConj_Alim',(c,143,1,)) #Queijo Mussarela
	o = append('tbOpt',('Bauru',))
	append('tbOpt_Conj',(o,c,))	

	c = append('tbConj',('Hamburguer de carne',0,))
	append('tbConj_Alim',(c,124,2,)) #Pão
	append('tbConj_Alim',(c,90,1,)) #Carne
	append('tbConj_Alim',(c,102,1,)) #Ovo
	append('tbConj_Alim',(c,103,4,)) #Azeite
	append('tbConj_Alim',(c,tomate,4,)) #Fatia de Tomate
	append('tbConj_Alim',(c,1,1,)) #Vegetal A
	append('tbConj_Alim',(c,36,1,)) #Vegetal B
	o = append('tbOpt',('Hamburguer de carne',))
	append('tbOpt_Conj',(o,c,))	
	
	c = append('tbConj',('Hamburguer de carne moída',0,))
	append('tbConj_Alim',(c,124,2,)) #Pão
	append('tbConj_Alim',(c,94,2,)) #Carne
	append('tbConj_Alim',(c,102,1,)) #Ovo
	append('tbConj_Alim',(c,103,4,)) #Azeite
	append('tbConj_Alim',(c,tomate,4,)) #Fatia de Tomate
	append('tbConj_Alim',(c,1,1,)) #Vegetal A
	append('tbConj_Alim',(c,36,1,)) #Vegetal B
	o = append('tbOpt',('Hamburguer de carne moída',))
	append('tbOpt_Conj',(o,c,))	


	# Crepioca
	c = append('tbConj',('Crepioca de Peru',0,))
	append('tbConj_Alim',(c,128,4,)) #Goma
	append('tbConj_Alim',(c,102,1,)) #Ovo
	append('tbConj_Alim',(c,145,1,)) 
	append('tbConj_Alim',(c,103,4,)) #Azeite
	append('tbConj_Alim',(c,tomate,4,)) #Fatia de Tomate
	append('tbConj_Alim',(c,1,1,)) #Vegetal A
	append('tbConj_Alim',(c,36,1,)) #Vegetal B
	o = append('tbOpt',('Crepioca de Peru',))
	append('tbOpt_Conj',(o,c,))	

	c = append('tbConj',('Crepioca de Presunto',0,))
	append('tbConj_Alim',(c,128,4,)) #Goma
	append('tbConj_Alim',(c,102,1,)) #Ovo
	append('tbConj_Alim',(c,146,1,)) 
	append('tbConj_Alim',(c,103,4,)) #Azeite
	append('tbConj_Alim',(c,tomate,4,)) #Fatia de Tomate
	append('tbConj_Alim',(c,1,1,)) #Vegetal A
	append('tbConj_Alim',(c,36,1,)) #Vegetal B
	o = append('tbOpt',('Crepioca de Presunto',))
	append('tbOpt_Conj',(o,c,))	

	c = append('tbConj',('Crepioca de Frango',0,))
	append('tbConj_Alim',(c,128,4,)) #Goma
	append('tbConj_Alim',(c,102,1,)) #Ovo
	append('tbConj_Alim',(c,85,4,)) 
	append('tbConj_Alim',(c,103,4,)) #Azeite
	append('tbConj_Alim',(c,tomate,4,)) #Fatia de Tomate
	append('tbConj_Alim',(c,1,1,)) #Vegetal A
	append('tbConj_Alim',(c,36,1,)) #Vegetal B
	o = append('tbOpt',('Crepioca de Frango',))
	append('tbOpt_Conj',(o,c,))	

	c = append('tbConj',('Crepioca de Carne Moída',0,))
	append('tbConj_Alim',(c,128,4,)) #Goma
	append('tbConj_Alim',(c,102,1,)) #Ovo
	append('tbConj_Alim',(c,94,2,)) 
	append('tbConj_Alim',(c,103,4,)) #Azeite
	append('tbConj_Alim',(c,tomate,4,)) #Fatia de Tomate
	append('tbConj_Alim',(c,1,1,)) #Vegetal A
	append('tbConj_Alim',(c,36,1,)) #Vegetal B
	o = append('tbOpt',('Crepioca de Carne Moída',))
	append('tbOpt_Conj',(o,c,))	

	c = append('tbConj',('Crepioca de Carne',0,))
	append('tbConj_Alim',(c,128,4,)) #Goma
	append('tbConj_Alim',(c,102,1,)) #Ovo
	append('tbConj_Alim',(c,90,1,)) 
	append('tbConj_Alim',(c,103,4,)) #Azeite
	append('tbConj_Alim',(c,tomate,4,)) #Fatia de Tomate
	append('tbConj_Alim',(c,1,1,)) #Vegetal A
	append('tbConj_Alim',(c,36,1,)) #Vegetal B
	o = append('tbOpt',('Crepioca de Carne',))
	append('tbOpt_Conj',(o,c,))	

	strN = 'Café (100 ml) c/ açucar demerara'
	c = append('tbConj',(strN,0,))
	append('tbConj_Alim',(c,189,100,)) #Café
	append('tbConj_Alim',(c,203,2,)) #Café
	o = append('tbOpt',(strN,))
	append('tbOpt_Conj',(o,c,))	
	
	strN = 'Café (100 ml) c/ açucar mascavo'
	c = append('tbConj',(strN,0,))
	append('tbConj_Alim',(c,189,100,)) #Café
	append('tbConj_Alim',(c,202,2,)) #Café
	o = append('tbOpt',(strN,))
	append('tbOpt_Conj',(o,c,))	

	strN = 'Café (100 ml) c/ açucar cristal'
	c = append('tbConj',(strN,0,))
	append('tbConj_Alim',(c,189,100,)) #Café
	append('tbConj_Alim',(c,201,2,)) #Café
	o = append('tbOpt',(strN,))
	append('tbOpt_Conj',(o,c,))	
	
def inserirOpcoesRonie():
	strN = '2 Ovos'
	c_2ovos = append('tbConj',(strN,0,))
	append('tbConj_Alim',(c_2ovos,102,2,)) #Ovo
	o_2ovos = append('tbOpt',(strN,))
	append('tbOpt_Conj',(o_2ovos,c_2ovos,))	

	strN = '2 Carnes'
	c_2carnes = append('tbConj',(strN,0,))
	append('tbConj_Alim',(c_2carnes,90,2,)) 
	o_2carnes = append('tbOpt',(strN,))
	append('tbOpt_Conj',(o_2carnes,c_2carnes,))	

	strN = '2 Frangos'
	c_2frangos = append('tbConj',(strN,0,))
	append('tbConj_Alim',(c_2frangos,91,2,)) 
	o_2frangos = append('tbOpt',(strN,))
	append('tbOpt_Conj',(o_2frangos,c_2frangos,))	

	strN = '2 Peixes'
	c_2peixes = append('tbConj',(strN,0,))
	append('tbConj_Alim',(c_2peixes,93,2,)) 
	o_2peixes = append('tbOpt',(strN,))
	append('tbOpt_Conj',(o_2peixes,c_2peixes,))	

	o = append('tbOpt',('Ovo ou Frango',))
	append('tbOpt_Conj',(o,c_2ovos,))	
	append('tbOpt_Conj',(o,85,))
	
	o = append('tbOpt',('Arroz ou Vegetais C',))
	append('tbOpt_Conj',(o,107,))	
	append('tbOpt_Conj',(o,106,))
	append('tbOpt_Conj',(o,109,))
	append('tbOpt_Conj',(o,111,))
	append('tbOpt_Conj',(o,113,))
	append('tbOpt_Conj',(o,120,))
	append('tbOpt_Conj',(o,108,))

	o = append('tbOpt',('Carne, Frango ou Peixe',))
	append('tbOpt_Conj',(o,c_2carnes,))	
	append('tbOpt_Conj',(o,c_2frangos,))
	append('tbOpt_Conj',(o,c_2peixes,))
	
	
	strN = 'Fruta Fresca c/ Castanha e Aveia'
	c = append('tbConj',(strN,0,))
	append('tbConj_Alim',(c,44,3,)) 
	append('tbConj_Alim',(c,162,1,)) 
	append('tbConj_Alim',(c,183,2,)) 
	o_ffca = append('tbOpt',(strN,))
	append('tbOpt_Conj',(o_ffca,c,))	
	c1 = c
	
	strN = 'Açaí batido c/ Fruta'
	c = append('tbConj',(strN,0,))
	append('tbConj_Alim',(c,44,2,)) 
	append('tbConj_Alim',(c,151,1,)) 
	o_ffca = append('tbOpt',(strN,))
	append('tbOpt_Conj',(o_ffca,c,))	
	c2 = c
	
	o = append('tbOpt',('Fruta OU Sanduiche OU Açai',))
	append('tbOpt_Conj',(o,c1,))	
	append('tbOpt_Conj',(o,213,))
	append('tbOpt_Conj',(o,c2,))

	
	# Atribuir Refeicoes a Opcoes

	# DESJEJUM
	append('tbRef_Opt',(1,226))
	append('tbRef_Opt',(1,124))
	append('tbRef_Opt',(1,233))

	# COLACAO
	append('tbRef_Opt',(2,44))
	append('tbRef_Opt',(2,158))

	#ALMOÇO
	append('tbRef_Opt',(3,1))
	append('tbRef_Opt',(3,36))
	append('tbRef_Opt',(3,234))
	append('tbRef_Opt',(3,131))
	append('tbRef_Opt',(3,235))
	
	#Lanche
	append('tbRef_Opt',(4,158))

	# Pre Treino A = 5
	append('tbRef_Opt',(5,226))
	append('tbRef_Opt',(5,213))
	
	# Intra-Treino = 6
	append('tbRef_Opt',(6,165))

	# Pos Treino = 7
	append('tbRef_Opt',(7,1))
	append('tbRef_Opt',(7,36))
	append('tbRef_Opt',(7,235))
	
	# Jantar A	= 8
	append('tbRef_Opt',(8,1))
	append('tbRef_Opt',(8,36))
	append('tbRef_Opt',(8,235))
	
	# 9 = PRE-DORMIR
	
	#10 = PRE-TREINO B 
	append('tbRef_Opt',(10,238))
	
	#11 = Jantar B
	append('tbRef_Opt',(11,229))
	append('tbRef_Opt',(11,1))
	append('tbRef_Opt',(11,36))
	
	
	# Todo dia tem Desjejum
	append('tbPlan_Ref',(1,1,1))
	append('tbPlan_Ref',(1,1,2))
	append('tbPlan_Ref',(1,1,3))
	append('tbPlan_Ref',(1,1,4))
	append('tbPlan_Ref',(1,1,5))
	append('tbPlan_Ref',(1,1,6))
	append('tbPlan_Ref',(1,1,7))

	# Todo dia tem colação	
	append('tbPlan_Ref',(1,2,1))
	append('tbPlan_Ref',(1,2,2))
	append('tbPlan_Ref',(1,2,3))
	append('tbPlan_Ref',(1,2,4))
	append('tbPlan_Ref',(1,2,5))
	append('tbPlan_Ref',(1,2,6))
	append('tbPlan_Ref',(1,2,7))
	
	# Todo dia tem almoço
	append('tbPlan_Ref',(1,3,1))
	append('tbPlan_Ref',(1,3,2))
	append('tbPlan_Ref',(1,3,3))
	append('tbPlan_Ref',(1,3,4))
	append('tbPlan_Ref',(1,3,5))
	append('tbPlan_Ref',(1,3,6))
	append('tbPlan_Ref',(1,3,7))
	
	# Lanche é só Segunda e Quarta
	append('tbPlan_Ref',(1,4,2))
	append('tbPlan_Ref',(1,4,4))

	# Pre Treino A = 5
	append('tbPlan_Ref',(1,4,2))
	append('tbPlan_Ref',(1,4,4))
	
	# Intra-Treino = 6 só 2 e 4
	append('tbPlan_Ref',(1,6,2))
	append('tbPlan_Ref',(1,6,4))
	
	# Pos Treino = 7 só 3,5,6
	append('tbPlan_Ref',(1,7,3))
	append('tbPlan_Ref',(1,7,5))
	append('tbPlan_Ref',(1,7,6))
	
	# Jantar A	= 8 só 2 e 4
	append('tbPlan_Ref',(1,8,2))
	append('tbPlan_Ref',(1,8,4))

	#10 = PRE-TREINO B  só 3,5 e 6
	append('tbPlan_Ref',(1,10,3))
	append('tbPlan_Ref',(1,10,5))
	append('tbPlan_Ref',(1,10,6))
	
	#11 = Jantar B só 3,5,6
	append('tbPlan_Ref',(1,11,3))
	append('tbPlan_Ref',(1,11,5))
	append('tbPlan_Ref',(1,11,6))
	
def inserirAlimentosExemplos():
	a1,c1,o1 = insAlimUn('Café','ml',0,0,1,0,0,100,)
	a2,c2,o2 = insAlimUn('Pão de forma integral','fatia',0,7,0,0,0,1,)
	a3,c3,o3 = insAlimUn('Cuscuz','col de sopa',0,7,0,0,0,2,)
	a4,c4,o4 = insAlimUn('Ovo','unid',0,5,0,0,0,2,)
	a5,c5,o5 = insAlimUn('Frango','col de sopa',0,4,0,0,0,3,)
	a6,c6,o6 = insAlimUn('Atum','col de sopa',0,4,0,0,0,3,)
	a7,c7,o7 = insAlimUn('Frutas Frescas','porção',0,3,0,0,0,1,)
	a8,c8,o8 = insAlimUn('Castanhas','porção',0,3,0,0,0,1,)

	c9 = append('tbConj',('Sanduiche c/ Ovo',0,))
	append('tbConj_Alim',(c9,a2,2,))
	append('tbConj_Alim',(c9,a4,1,))
	append('tbConj_Alim',(c9,a5,1,))
	o9 = append('tbOpt',('Sanduiche c/ ovo',))
	append('tbOpt_Conj',(o9,c9,))	

	c10 = append('tbConj',('Sanduiche s/ Ovo',0,))
	append('tbConj_Alim',(c10,a2,2,))
	append('tbConj_Alim',(c10,a5,1,))
	o10 = append('tbOpt',('Sanduiche s/ ovo',))
	append('tbOpt_Conj',(o10,c10,))	

	o11 = append('tbOpt',('Sanduiche c/ ovo OU Sanduiche s/ Ovo',))
	append('tbOpt_Conj',(o11,c9,))	
	append('tbOpt_Conj',(o11,c10,))

	# Refeições
	r1 = append('tbRef',('DESJEJUM',makeHora(7,0,0),))
	r2 = append('tbRef',('COLACAO',makeHora(10,0,0),))
	r3 = append('tbRef',('ALMOCO',makeHora(12,0,0),))
	r4 = append('tbRef',('JANTAR',makeHora(20,0,0),))
	
	append('tbRef_Opt',(r1,o1))
	append('tbRef_Opt',(r1,o11))
	append('tbRef_Opt',(r2,o7))
	append('tbRef_Opt',(r2,o8))
	append('tbRef_Opt',(r3,o9))
	append('tbRef_Opt',(r4,o2))
	append('tbRef_Opt',(r4,o4))
	
	# Plano
	p1 = append('tbPlan',(getDataAgora(),makeData(11,6,2018),makeData(11,8,2018),))

	#Plano e Refeicao
	# Coloquei as 4 refeicoes todos os dias de domingo a sabado
	append('tbPlan_Ref',(p1,r1,1))
	append('tbPlan_Ref',(p1,r2,1))
	append('tbPlan_Ref',(p1,r3,1))
	append('tbPlan_Ref',(p1,r4,1))
	
	append('tbPlan_Ref',(p1,r1,2))
	append('tbPlan_Ref',(p1,r2,2))
	append('tbPlan_Ref',(p1,r3,2))
	append('tbPlan_Ref',(p1,r4,2))

	append('tbPlan_Ref',(p1,r1,3))
	append('tbPlan_Ref',(p1,r2,3))
	append('tbPlan_Ref',(p1,r3,3))
	append('tbPlan_Ref',(p1,r4,3))

	append('tbPlan_Ref',(p1,r1,4))
	append('tbPlan_Ref',(p1,r2,4))
	append('tbPlan_Ref',(p1,r3,4))
	append('tbPlan_Ref',(p1,r4,4))

	append('tbPlan_Ref',(p1,r1,5))
	append('tbPlan_Ref',(p1,r2,5))
	append('tbPlan_Ref',(p1,r3,5))
	append('tbPlan_Ref',(p1,r4,5))

	append('tbPlan_Ref',(p1,r1,6))
	append('tbPlan_Ref',(p1,r2,6))
	append('tbPlan_Ref',(p1,r3,6))
	append('tbPlan_Ref',(p1,r4,6))

	append('tbPlan_Ref',(p1,r1,7))
	append('tbPlan_Ref',(p1,r2,7))
	append('tbPlan_Ref',(p1,r3,7))
	append('tbPlan_Ref',(p1,r4,7))	
	
def hardInsertExemplos():
	hardInsReset()
	inserirPlanoPadrao()
	inserirRefeicoesPadrao()
	inserirAlimentosNutricionista()
	inserirAlimentosOrdinarios()
	inserirConjuntosRonie()
	inserirOpcoesRonie()
	print('Exemplos criados')
	
def getConfig(strKey):
	conn=sqlite3.connect(strDbFilename)
	cur=conn.cursor()
	cur.execute("SELECT codigo,strKey,strValue FROM tbConfig Where strKey = ?",(strKey,))
	row = cur.fetchone()
	conn.close()
	if row == None:
		return ''
	else:
		return row[2]	
	
def setConfig (strKey,strValue):
	conn=sqlite3.connect(strDbFilename)
	cur=conn.cursor()
	cur.execute("SELECT codigo,strKey,strValue FROM tbConfig Where strKey = ?",(strKey,))
	row = cur.fetchone()
	conn.close()
	if row == None:
		return append('tbConfig',(strKey,strValue,))
	else:
		cod = row[0]
		conn=sqlite3.connect(strDbFilename)
		cur=conn.cursor()
		cur.execute("UPDATE tbConfig SET strValue=? WHERE codigo=?",(strValue,cod,))
		conn.commit()
		conn.close()
		return cod

def initDB():
	''' Inicia banco de dados '''
	defineTables()
	gerarDB()
	setConfig('DietaAlterada','1')
	
	#Verifica se já inicializei a data de hoje
	dtHoje = getDataHoje()
	strUltimoAcesso = getConfig('strUltimoAcesso')
	if strUltimoAcesso != sqlite3_DateForSQL(dtHoje):
		# Inicializações de novo dia: Preciso criar tbHistOpt
		numWeek = getWeekDay(dtHoje)
		numPlan = nC('tbPlan') - 1
		textSQL = '''
		SELECT
		tbPlan_Ref.codigo as codigo,
		tbPlan_Ref.codRef,
		tbRef.strRefeicao,
		tbRef.hrHora,
		tbRef_Opt.codOpt,
		tbOpt.strOpt
		FROM
		tbPlan_Ref, tbRef, tbRef_Opt, tbOpt
		WHERE
		tbPlan_Ref.codigo > 0
		AND tbRef.codigo = tbPlan_Ref.codRef
		AND tbPlan_Ref.codPlan = ''' + str(numPlan) + ' ' + '''
		AND tbPlan_Ref.diaSemana = ''' + str(numWeek) + ' ' + '''
		AND tbRef_Opt.codRef = tbPlan_Ref.codRef
		AND tbRef_Opt.codOpt = tbOpt.codigo
		ORDER BY hrHora
		'''
		df = retPandasDfFromSQL(textSQL)
		for index,row in df.iterrows():
			append('tbHistOpt',(dtHoje,row['hrHora'],row['strRefeicao'],int(row['codOpt']),0,))
		
		# Avisa que já inicializou o dia de hoje
		setConfig('strUltimoAcesso',sqlite3_DateForSQL(dtHoje))
		setConfig('DietaAlterada','1')

def	retDF_DietaAtual():
	textSQL = '''
	Select 
	tbHistOpt.codigo,
	tbHistOpt.dtData,
	tbHistOpt.hrHora,
	tbHistOpt.strRefeicao,
	tbHistOpt.codOpt,
	tbHistOpt.booC,
	tbOpt.strOpt
	From 
	tbHistOpt, tbOpt
	Where tbHistOpt.codOpt = tbOpt.codigo
	And booC = 0
	And tbHistOpt.dtData = ''' + getStrDataAgora() + ' ' + '''
	Order By tbHistOpt.hrHora
	'''
	#print(textSQL)
	df = retPandasDfFromSQL(textSQL)
	return df

def	retDF_DietaAtualFilterByStrRefeicao(strRefeicao):
	textSQL = '''
	Select 
	tbHistOpt.codigo as codigo,
	tbHistOpt.codigo as tbHistOpt_codigo,
	tbHistOpt.dtData,
	tbHistOpt.hrHora,
	tbHistOpt.strRefeicao,
	tbHistOpt.codOpt,
	tbHistOpt.booC,
	tbOpt.strOpt,
	tbOpt_Conj.codConj,
	tbConj.strConjunto
	From 
	tbHistOpt, tbOpt, tbOpt_Conj, tbConj
	Where tbHistOpt.codOpt = tbOpt.codigo
	And booC = 0
	And tbOpt_Conj.codOpt = tbHistOpt.codOpt
	And tbOpt_Conj.codConj = tbConj.codigo
	And tbHistOpt.dtData = ''' + sqlite3_DateForSQL(datetime.date.today()) + ' ' + '''
	And tbHistOpt.strRefeicao = ''' + '"' + strRefeicao + '"' + '''
	Order By tbHistOpt.hrHora
	'''
	df = retPandasDfFromSQL(textSQL)
	return df
	
def retDF_strConjuntoByCodOpt(codOpt): #Nao estou usando mais
	textSQL = '''
	SELECT
	tbConj.codigo,
	tbConj.strConjunto
	FROM
	tbOpt_Conj, tbConj, tbOpt
	WHERE
	tbConj.codigo > 0
	AND tbOpt_Conj.codConj = tbConj.codigo
	AND tbOpt_Conj.codOpt = tbOpt.codigo
	AND tbOpt_Conj.codOpt = ''' + str(codOpt) + ' ' + '''
	ORDER BY strConjunto
	'''
	df = retPandasDfFromSQL(textSQL)
	return df
	
def retStrOptByCodOpt(codOpt):  #Nao estou usando mais
	conn=sqlite3.connect(strDbFilename)
	cur=conn.cursor()
	textSQL = '''
	SELECT
	tbOpt.strOpt
	FROM
	tbOpt
	WHERE
	tbOpt.codigo = 	''' + str(codOpt) + ' '
	cur.execute(textSQL)
	row=cur.fetchone()
	conn.close()
	return row[0]
	
def tbHistOpt_ChecaOpt(tbHistOpt_codigo):
	conn=sqlite3.connect(strDbFilename)
	cur=conn.cursor()
	cur.execute("UPDATE tbHistOpt SET booC=1 WHERE codigo=?",(tbHistOpt_codigo,))
	conn.commit()
	conn.close()

def tbConj_incNumFreq(codConj):
	conn=sqlite3.connect(strDbFilename)
	cur=conn.cursor()
	cur.execute("SELECT numFreq FROM tbConj WHERE codigo = " + str(codConj))
	row = cur.fetchone()
	numFreq = row[0] + 1
	cur.execute("UPDATE tbConj SET numFreq=? WHERE codigo=?",(numFreq,codConj,))
	conn.commit()
	conn.close()
	
def getReceitaFromCodConj(codConj):
	strRet = ''
	numCals = 0
	textSQL = '''
	SELECT
	tbConj_Alim.codigo as codigo,
	tbConj_Alim.codConj as codConj,
	tbConj.strConjunto,
	tbConj_Alim.codAlim,
	tbConj_Alim.numQtd,
	tbAlim.strUnidade,
	tbAlim.strAlimento,
	tbConj_Alim.numQtd * tbAlim.numCaloria as qtdCalorias,
	tbAlim.numGrupo,
	tbAlim.booBebida,
	tbAlim.numTipo
	FROM
	tbConj_Alim, tbAlim, tbConj
	WHERE
	tbConj_Alim.codigo > 0
	AND tbConj_Alim.codAlim = tbAlim.codigo
	AND tbConj_Alim.codConj = tbConj.codigo
	AND tbConj_Alim.codConj = ''' + str(codConj)
	df = retPandasDfFromSQL(textSQL)
	len_df = len(df)
	if len_df > 0:
		c = 0
		for index,row in df.iterrows():
			c += 1
			strRet += str(row['numQtd']) + ' ' +  row['strUnidade']
			if row['numQtd'] > 1:
				strRet += 's'
			strRet += ' de ' + row['strAlimento'] 
			if c < len_df:
				strRet += ' + '

		# Falta o total de calorias dessa receita
		conn=sqlite3.connect(strDbFilename)
		cur=conn.cursor()
		textSQL = '''
		SELECT
		tbConj_Alim.codConj as codigo,
		SUM(tbConj_Alim.numQtd * tbAlim.numCaloria) as totalCalorias
		FROM
		tbConj_Alim, tbAlim
		WHERE
		tbConj_Alim.codigo > 0
		AND tbConj_Alim.codAlim = tbAlim.codigo
		AND tbConj_Alim.codConj = '''  + str(codConj) + ' ' + '''
		GROUP BY tbConj_Alim.codConj
		'''
		cur.execute(textSQL)
		row=cur.fetchone()
		conn.close()
		numCals = row[1]
	else:
		strRet = 'Erro: Conjunto sem alimentos'
	return strRet, numCals

def conjuntoDictToRV():
	textSQL = '''
	Select 
	tbConj.codigo as codigo,
	tbConj.strConjunto
	From 
	tbConj
	'''
	df = retPandasDfFromSQL(textSQL)
	listaDict = []
	dictR = {}
	for index,row in df.iterrows():
		auxReceita, numCals = getReceitaFromCodConj(index)
		dictR['text'] = '[b][color=ffd700]{0}[/color][/b]\n[i][color=ffff33]{1} = {2} Kcal[/color][/i]'.format(row['strConjunto'],auxReceita,numCals)
		dictR['codigo'] = index
		dictR['booSel'] = 0
		listaDict.append(dictR)
		dictR = {}
	return listaDict

def getListDictForTableRVFromTbTable(tbTable,strFilter):
	global dictTables
	hab = False
	# Valida
	if tbTable in dictTables:
		hab = True
	else:
		print('Erro no append: Tabela não existe')
	# Passou nos testes
	if hab:
		# Cria código SQL para a tabela
		textSQL = 'SELECT '
		textSQL += tbTable + '.' + 'codigo as codigo, '
		for strField,strType in dictTables[tbTable].items():
			textSQL += tbTable + '.' + strField + ', '
		textSQL = textSQL[:-2] + ' '
		textSQL += 'FROM '
		textSQL += tbTable
		if strFilter != '':
			textSQL += ' ' + strFilter
		
		# Cria ListDict	
		df = retPandasDfFromSQL(textSQL)
		listaDict = []
		dictR = {}
		strSep = ' '
		for index,row in df.iterrows():
			auxText = '{0:5}'.format(str(index)) + strSep		
			for strField,strType in dictTables[tbTable].items():
				nF = ''
				if strType == 'INTEGER':
					nF = '5'
				elif strType == 'TEXT':
					nF = '10'
				else:
					nF = '10'
		
				strFormat = '{0:' + str(nF) + '}' 
				auxText += strFormat.format(row[strField]) + strSep
				dictR[strField] = row[strField]
			# Depois posso melhorar pegando para cada coluna o maior length e usando isso como nF
			auxText = auxText[:-1 * len(strSep)]
			dictR['text'] = auxText
			dictR['codigo'] = index
			dictR['booSel'] = 0
			listaDict.append(dictR)
			dictR = {}
		return listaDict
	else:
		return []
		
def getListDictForTableRVFromTextSQL(textSQL):
	df = retPandasDfFromSQL(textSQL)
	listaDict = []
	dictR = {}
	strSep = ' '
	for index,row in df.iterrows():
		auxText = '{0}'.format(str(index)) + strSep		
		for strField in df.columns:
			dictR[strField] = row[strField]
			auxText += str(row[strField]) + strSep
		auxText = auxText[:-1 * len(strSep)]
		dictR['text'] = auxText
		dictR['codigo'] = index
		dictR['booSel'] = 0
		listaDict.append(dictR)
		dictR = {}
	return listaDict