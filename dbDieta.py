#Cria a estrutura de banco de dados e insere os dados HARD CODED

import sqlite3
import datetime

strDbFilename = "dbDieta.db"
listTables = []


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

def conectarDB():
	global listTables
	conn=sqlite3.connect(strDbFilename)
	cur=conn.cursor()
	# Tabela Alimento
	listTables.append("tbAlim")
	strExec = '''
	CREATE TABLE IF NOT EXISTS
	tbAlim
	(
	codigo INTEGER PRIMARY KEY,
	strAlimento VARCHAR,
	numCaloria INTEGER,
	numGrupo INTEGER
	)
    '''
	cur.execute(strExec)
	# Tabela Conjunto
	listTables.append("tbConj")
	strExec = '''
	CREATE TABLE IF NOT EXISTS
	tbConj
	(
	codigo INTEGER PRIMARY KEY,
	strConjunto VARCHAR
	)
    '''
	cur.execute(strExec)
	# Tabela Vinculo Conj_Alim
	listTables.append("tbConj_Alim")
	strExec = '''
	CREATE TABLE IF NOT EXISTS
	tbConj_Alim
	(
	codigo INTEGER PRIMARY KEY,
	codConjunto INTEGER,
	codAlimento INTEGER,
	qtdNum INTEGER,
	qtdUnid VARCHAR
	)
	'''
	cur.execute(strExec)
	# Tabela Opcao
	listTables.append("tbOpt")
	strExec = '''
	CREATE TABLE IF NOT EXISTS
	tbOpt
	(
	codigo INTEGER PRIMARY KEY,
	strOpt VARCHAR
	)
	'''
	cur.execute(strExec)
	# Tabela Vinculo Opt_Conj
	listTables.append("tbOpt_Conj")
	strExec = '''
	CREATE TABLE IF NOT EXISTS
	tbOpt_Conj
	(
	codigo INTEGER PRIMARY KEY,
	codOpt INTEGER,
	codConj INTEGER
	)
	'''
	cur.execute(strExec)
	# Tabela Refeicao
	listTables.append("tbRef")
	strExec = '''
	CREATE TABLE IF NOT EXISTS
	tbRef
	(
	codigo INTEGER PRIMARY KEY,
	strRefeicao VARCHAR,
	hrHora INTEGER
	)
	'''
	cur.execute(strExec)
	# Tabela Vinculo Ref_Opt
	listTables.append("tbRef_Opt")
	strExec = '''
	CREATE TABLE IF NOT EXISTS
	tbRef_Opt
	(
	codigo INTEGER PRIMARY KEY,
	codRef INTEGER,
	codOpt INTEGER
	)
	'''
	cur.execute(strExec)
	# Tabela Plano
	listTables.append("tbPlan")
	strExec = '''
	CREATE TABLE IF NOT EXISTS
	tbPlan
	(
	codigo INTEGER PRIMARY KEY,
	dataCria INTEGER,
	dataInicio INTEGER,
	dataFinal INTEGER
	)
	'''
	cur.execute(strExec)
	# Tabela Vinculo Plan_Ref
	listTables.append("tbPlan_Ref")
	strExec = '''
	CREATE TABLE IF NOT EXISTS
	tbPlan_Ref
	(
	codigo INTEGER PRIMARY KEY,
	codPlan INTEGER,
	codRef INTEGER,
	diaSemana INTEGER
	)
	'''
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
	
	
conectarDB()
mostrarTodasTabelas()
