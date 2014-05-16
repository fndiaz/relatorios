#gravacao_lg = db.define_table("gravacao_lg",
#      Field("datetime"),
#      Field("acao"),
#      Field("pastas"),
#      #auth.signature
#      format="%(nome)s")

Cdr = db.define_table("cdr",
	Field("recid", "id"),
	Field("calldate"),
	Field("clid"),
	Field("origem"),
	Field("dst"),
	Field("duration"),
	Field("lastapp"),
	Field("userfield"),
	Field("disposition"),
	Field("AD2_uniqueid"),
	migrate=False)

Ramal_vitual = db.define_table("ramal_virtual",
	Field("id_ramalvirtual", "id"),
	Field("ramal_virtual"),
	Field("nome"),
	migrate=False)

Usuario_admanager = db.define_table("usuario_admanager",
	Field("id_usuario", "id"),
	Field("usuario"),
	Field("senha"),
	migrate=False)







