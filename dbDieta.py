#Cria a estrutura de banco de dados e insere os dados HARD CODED

import sqlite3
import datetime

import numpy as np
import pandas as pd


strDbFilename = "dbDieta.db"
dictTables = dict()


################################################################################
								# Funções Auxiliares
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
	#return datetime.date(2018,1,16)

def sqlite3_DateTimeForSQL(dtData):
	strRet = "'{0:04}-{1:02}-{2:02}'".format(dtData.year,dtData.month,dtData.day)
	return strRet

################################################################################
								# Funções Principais
################################################################################

def defineTables():
	'Define the tables and fields'
	global dictTables
	dictAuxFields = dict()
	#----------------------------------------
	# Tabela Alimento
	#----------------------------------------
	strAuxTable = 'tbAlim'
	dictAuxFields = {
	'strAlimento':'TEXT',
	'strUnidade':'TEXT',
	'numCaloria':'INTEGER',
	'numGrupo':'INTEGER',
	'booBebida':'INTEGER',
	'numTipo':'INTEGER'
	}
	dictTables[strAuxTable] = dictAuxFields
	#----------------------------------------
	# Tabela Conjunto
	#----------------------------------------
	strAuxTable = 'tbConj'
	dictAuxFields = {
	'strConjunto':'TEXT'
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
	'hrHora':'INTEGER'
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
	'dataCria':'INTEGER',
	'dataInicio':'INTEGER',
	'dataFinal':'INTEGER'
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
	'hrHora':'INTEGER',
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
	'hrHora':'INTEGER',
	'codConj':'INTEGER',
	'codOpt':'INTEGER'
	}
	dictTables[strAuxTable] = dictAuxFields

	
	
	
	
	
def inicializar(drop,gera):
	global dictTables
	defineTables()
	if drop:
		dropAllTables()
	if gera:
		gerarDB()

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
	print('Tabelas criadas')
	
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

def insAlimUn(strAlimento,strUnidade,numCaloria,numGrupo,booBebida,numTipo,numQtd):
	a = append('tbAlim',(strAlimento,strUnidade,numCaloria,numGrupo,booBebida,numTipo,))
	c = append('tbConj',(strAlimento,))
	append('tbConj_Alim',(c,a,numQtd,))
	o = append('tbOpt',(strAlimento,))
	append('tbOpt_Conj',(o,c))	
	return a,c,o
	
def hardInsertExemplos():
	# Alimentos, Conjuntos e Opções
	a1,c1,o1 = insAlimUn('Café','ml',0,0,1,0,100)
	a2,c2,o2 = insAlimUn('Pão de forma integral','fatia',0,7,0,0,1)
	a3,c3,o3 = insAlimUn('Cuscuz','col de sopa',0,7,0,0,2)
	a4,c4,o4 = insAlimUn('Ovo','unid',0,5,0,0,2)
	a5,c5,o5 = insAlimUn('Frango','col de sopa',0,4,0,0,3)
	a6,c6,o6 = insAlimUn('Atum','col de sopa',0,4,0,0,3)
	a7,c7,o7 = insAlimUn('Frutas Frescas','porção',0,3,0,0,1,)
	a8,c8,o8 = insAlimUn('Castanhas','porção',0,3,0,0,1,)

	c9 = append('tbConj',('Sanduiche c/ Ovo',))
	append('tbConj_Alim',(c9,a2,2,))
	append('tbConj_Alim',(c9,a4,1,))
	append('tbConj_Alim',(c9,a5,1,))
	o9 = append('tbOpt',('Sanduiche c/ ovo',))
	append('tbOpt_Conj',(o9,c9,))	

	c10 = append('tbConj',('Sanduiche s/ Ovo',))
	append('tbConj_Alim',(c10,a2,2,))
	append('tbConj_Alim',(c10,a5,1,))
	o10 = append('tbOpt',('Sanduiche s/ ovo',))
	append('tbOpt_Conj',(o10,c10,))	

	o11 = append('tbOpt',('Sanduiche c/ ovo OU Sanduiche s/ Ovo',))
	append('tbOpt_Conj',(o11,c9,))	
	append('tbOpt_Conj',(o11,c10,))

	# Refeições
	r1 = append('tbRef',('DESJEJUM',7))
	r2 = append('tbRef',('COLACAO',10))
	r3 = append('tbRef',('ALMOCO',12))
	r4 = append('tbRef',('JANTAR',20))
	
	append('tbRef_Opt',(r1,o1))
	append('tbRef_Opt',(r1,o11))
	append('tbRef_Opt',(r2,o7))
	append('tbRef_Opt',(r2,o8))
	append('tbRef_Opt',(r3,o9))
	append('tbRef_Opt',(r4,o2))
	append('tbRef_Opt',(r4,o4))
	
	# Plano
	p1 = append('tbPlan',(0,0,0,))

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
	
	

################################################################################
								# Funções Programação
################################################################################

		
def mostrarTabela(tbTable):
	df = retPandasDfFromSQL('Select * From ' + tbTable)
	print("")
	print("....................")
	print(tbTable)
	print("....................")
	display(df)
	print("-------------------")
		
		
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

inicializar(True,True)
hardInsertExemplos()
mostrarTodasTabelas()
