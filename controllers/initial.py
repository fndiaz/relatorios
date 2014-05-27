# coding=UTF-8
import os, time, base64

def show_gravacoes():
	if session.usuario == '':
		redirect(URL("login"))

	response.app='Gravções'
	response.title = 'lista'
	db.cdr.recid.readable=False
	db.cdr.lastapp.readable=False
	db.cdr.disposition.readable=False
	db.cdr.AD2_uniqueid.readable=False
	db.cdr.userfield.readable=False
	db.cdr.duration.filter_out= lambda duration: time.strftime('%H:%M:%S', time.gmtime(duration))

	query1 = (db.cdr.origem.like ('%'+ str(session.origem) +'%'))
	query2 = (db.cdr.dst.like ('%'+ str(session.destino) +'%'))
	query3 = (db.cdr.calldate.like ('%'+ str(session.data) +'%'))
	query4 = (db.cdr.disposition == 'ANSWERED')
	query5 = ~(db.cdr.dst.like('%''s''%'))
	#query4 = (orderby='db.cdr.calldate DESC')
	queryset = (query1) & (query2) & (query3) & (query4) & (query5)
	print queryset

	if session.usuario != 'diretoria':
		queryset = add_query(queryset)
	print '-----------'
	print queryset


	links = [dict(header='',body=lambda row: 
			A(IMG(_src=URL("relatorios", "static/images", "audio_ok2.png")), #imagem
				  _href =URL("link_player", vars=dict(date=row.calldate, unique=row.AD2_uniqueid, link='player')), _target='_blank') ),
			dict(header='',body=lambda row: 
			A(IMG(_src=URL("relatorios", "static/images", "down4.png")), #imagem
				  _href =URL("link_player", vars=dict(date=row.calldate, unique=row.AD2_uniqueid, link='down')), _target='_blank') )
	]
	headers = { 'cdr.calldate' : 'Data', 'cdr.clid' : 'Caller ID', 
		'cdr.origem' : 'Origem', 'cdr.dst' : 'Destino' }


	grid = SQLFORM.grid(query=queryset,
		paginate=30, searchable=True, create=False, details=False,
		links_placement="left", orderby=~db.cdr.calldate , headers=headers,
		csv=False, links=links)
	
	return response.render("initial/principal.html", grid=grid)

def link_player():
	date = request.vars.date
	unique = request.vars.unique

	date = date.split(' ')[0]
	datef=''
	for i in range(0,3):
		dt = date.split('-')[i]
		datef = datef + dt
		i=i+1

	if request.vars.link == 'player':	
		redirect(("http://"+ request.env.server_addr +"/wavplayer/index.php?audio=GRAVACOES/"+ datef +"/"+ unique +".WAV"))
		#***TROCAR por request.env.server_addr****
	elif request.vars.link == 'down':
		#redirect(("http://"+ request.env.remote_addr +"/GRAVACOES/"+ datef +"/"+ unique +".WAV"))
		redirect(("http://"+ request.env.server_addr +"/download_audio.php/?diretorio="+ datef +"&arquivo="+ unique +".WAV"))
		#***TROCAR por request.env.server_addr****


def form_gravacoes():
	if session.usuario == '':
		redirect(URL("login"))

	response.app='Gravções'
	response.title="busca"
	
	return response.render("initial/show_form.html")

def submit_form():
	session.origem = request.vars['origem']
	session.destino = request.vars['destino']
	session.data = request.vars['data']

	redirect(URL("show_gravacoes"))

def principal():
	redirect(URL("form_gravacoes"))
####Fim Gravações #var Global

####Saintes #var funcao 
def form_saintes():
	if session.usuario == '':
		redirect(URL("login"))

	response.app='Realizadas'
	response.title='busca'
	ramal=[]
	busca=db(db.ramal_virtual).select()
	for row in busca:
		ramal.append(row.ramal_virtual)

	form = SQLFORM.factory(
			Field("ramal", requires=IS_IN_SET(ramal, error_message=T('selecione um ramal'))),
			Field("data", "date", requires=IS_NOT_EMPTY(error_message=T('selecione uma data'))),
			submit_button='Buscar'
			)

	if form.process().accepted:
		ramal = request.vars['ramal']
		data = request.vars['data']

		query1=(db.cdr.lastapp == "Dial")
		query2=(db.cdr.origem == ramal)
		query3=(db.cdr.calldate.like ('%'+ data +'%'))
		queryset=(query1) & (query2) & (query3)
		print queryset

		grid = show_grid(queryset, title='Realizadas')#funçao que cria a grid
		response.flash="processado"

		return response.render("initial/show_grid_saintes.html", grid=grid)

	elif form.errors:
		print 'no'
		response.flash="algo está errado"

	return response.render("initial/show_grid.html", form=form)

####Entrantes #var funcao 
def form_entrantes():
	if session.usuario == '':
		redirect(URL("login"))

	response.app='Recebidas'
	response.title='busca'
	ramal=[]
	busca=db(db.ramal_virtual).select()
	for row in busca:
		ramal.append(row.ramal_virtual)

	form = SQLFORM.factory(
			Field("ramal", requires=IS_IN_SET(ramal, error_message=T('selecione um ramal'))),
			Field("data", "date", requires=IS_NOT_EMPTY(error_message=T('selecione uma data'))),
			submit_button='Buscar'
			)

	if form.process().accepted:
		ramal = request.vars['ramal']
		data = request.vars['data']

		query1=(db.cdr.userfield.like ('%''ENTRANTE''%'))
		query2=(db.cdr.dst == ramal)
		query3=(db.cdr.calldate.like ('%'+ data +'%'))
		queryset=(query1) & (query2) & (query3)
		print queryset

		grid = show_grid(queryset, title='Entrantes')#funçao que cria a grid
		response.flash="processado"

		return response.render("initial/show_grid_saintes.html", grid=grid)

	elif form.errors:
		print 'no'
		response.flash="algo está errado"

	return response.render("initial/show_grid.html", form=form)

def show_grid(queryset, title):
	#Criação da grid
	response.app=title
	response.title="lista"
	db.cdr.recid.readable=False
	db.cdr.lastapp.readable=False
	db.cdr.disposition.readable=False
	db.cdr.AD2_uniqueid.readable=False
	db.cdr.userfield.readable=False
	db.cdr.duration.filter_out= lambda duration: time.strftime('%H:%M:%S', time.gmtime(duration))

	headers = { 'cdr.calldate' : 'Data', 'cdr.clid' : 'Caller ID', 
		'cdr.origem' : 'Origem', 'cdr.dst' : 'Destino', 'cdr.duration' : 'Duração' }

	grid = SQLFORM.grid(query=queryset,
		paginate=99999, searchable=True, create=False, details=False,
		orderby=~db.cdr.calldate, csv=False, headers=headers
		)

	return(grid)

def login():
	print 'entrou login'
	form = SQLFORM.factory(
		Field("usuario", requires = IS_NOT_EMPTY(error_message=
			T("valor não pode ser nulo"))),
		Field("senha", "password"),
		formstyle="divs",
		)

	response.app="login"
	response.title=""
	if form.process().accepted:
		usuario_dig = form.vars.usuario
		senha_dig = form.vars.senha
		print 'usuario digitado:%s  senha digitada:%s' %(usuario_dig, senha_dig) 

		#con = teste(usuario_dig)#funçao usuario admanager
		aut = autentica(usuario_dig, senha_dig)
		if aut is False:
			session.flash='login incorreto'
			redirect(URL("login"))
		if aut is True:
			session.usuario = usuario_dig
			session.flash='Logado com %s' %(usuario_dig)
			redirect(URL("form_gravacoes"))
		
		#Logando por usuario admanager
		#if con == 'nulo':
		#	print "Usuario incorreto"
		#	response.flash = 'Usuário não existe'
		#else:
		#	usuario = con[0][0]
		#	senha = con[0][1]
		#	print base64.b64decode(senha)
		#	senha = base64.b64decode(senha)
		#	if senha_dig == senha:
		#		print 'senha ok'
		#		session.usuario = usuario
		#		session.senha = senha
		#		session.flash='Logado com %s' %(usuario)
		#		redirect(URL("form_gravacoes"))
		#	else:
		#		print 'senha errata'
		#		session.flash='Senha incorreta'
		#		redirect(URL("login"))
	elif form.errors:
		response.flash = 'Ops, algo não está correto'			
					
	return response.render("initial/login.html", form=form)

def logout():
	session.flash='Sessao de %s finalizada' %(session.usuario)
	session.usuario=''
	session.senha=''
	redirect("login")

def teste(usuario_dig):
	con = db.executesql("SELECT usuario, senha FROM  usuario_admanager WHERE usuario = '%s'" %(usuario_dig))
	#print con

	if con == ():
		#print 'nulo'
		con = 'nulo'
	
	return (con)

def autentica(usuario_dig, senha_dig):
	print 'autentica'
	users = [{'nome': 'diretoria', 'senha': '210845'}, 
			 {'nome':'tecnologia', 'senha': '123456'},
			 {'nome': 'admin', 'senha':'123456'}]

	for user in users:
		if user['nome'] == usuario_dig:
			if user['senha'] == senha_dig:
				return True
	return False

def add_query(queryset):
	for ramal in session.ls_ramais:
		queryset=queryset & ~(db.cdr.origem == ramal)
		queryset=queryset & ~(db.cdr.dst == ramal)
	return queryset



def user(nome):
	if request.args(0) == 'register':
        	db.auth_user.bio.writable = db.auth_user.bio.readable = False
	return response.render("initial/user.html", user=auth())

def loginn():
        return auth.login()

def account():
    return dict(register=auth.register(),
                login=auth.login())
	
def download():
	return response.download(request, db)

	



