#Cria a estrutura de banco de dados e insere os dados HARD CODED

import sqlite3
import datetime

strDbFilename = "dbDieta.db"
listTables = []
dictTables = dict()


################################################################################
								# Funções Auxiliares
################################################################################
def nC(tbTable):
	# Verifica maior codigo da tabela tbTable e retorna esse codido incrementado de 1
    conn=sqlite3.connect(strDbTree)
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
	'strAlimento':'VARCHAR',
	'numCaloria':'INTEGER',
	'numGrupo':'INTEGER'
	}
	dictTables[strAuxTable] = dictAuxFields
	#----------------------------------------
	# Tabela Conjunto
	#----------------------------------------
	strAuxTable = 'tbConj'
	dictAuxFields = {
	'strConjunto':'VARCHAR'
	}
	dictTables[strAuxTable] = dictAuxFields
	#----------------------------------------
	# Tabela Vinculo Conj_Alim
	#----------------------------------------
	strAuxTable = 'tbConj_Alim'
	dictAuxFields = {
	'codConjunto':'INTEGER',
	'codAlimento':'INTEGER',
	'qtdNum':'INTEGER',
	'qtdUnid':'VARCHAR'
	}
	dictTables[strAuxTable] = dictAuxFields
	#----------------------------------------	
	# Tabela Opcao
	#----------------------------------------
	strAuxTable = 'tbOpt'
	dictAuxFields = {
	'strOpt':'VARCHAR'
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
	'strRefeicao':'VARCHAR',
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

def conectarDB():
	global dictTables
	global listTables
	defineTables()
	conn=sqlite3.connect(strDbFilename)
	cur=conn.cursor()
	for strTable,dictAuxFields in dictTables.items():
		listTables.append(strTable)
		strExec = 'CREATE TABLE IF NOT EXISTS ' + strTable + ' ('
		strExec += 'codigo INTEGER PRIMARY KEY, '
		for strField,strType in dictAuxFields.items():
			strExec += strField + ' ' + strType + ', '
		strExec = strExec[:-2] #Tira último ", "
		strExec += ')'
		cur.execute(strExec)
	# Commita tudo
	conn.commit()
	
	
def view(tbTable):
	conn=sqlite3.connect(strDbFilename)
	cur=conn.cursor()
	cur.execute("SELECT * FROM " + tbTable)
	rows=cur.fetchall()
	conn.close()
	return rows
	
	
def mostrarTodasTabelas():
	global listTables
	for i in listTables:
		v = view(i)
		print("")
		print("....................")
		print(i)
		print("....................")
		print(v)
		print("-------------------")
	
	
