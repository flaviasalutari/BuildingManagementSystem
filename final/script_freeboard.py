# -*- coding: utf-8 -*-
import cherrypy
import os, os.path
import json

class StringGeneratorWebService():
	exposed=True

	def GET(self, *uri,**params):
		htmlpage=open('freeboard/index.html','r')
		return htmlpage.read()

	def POST(self, *uri, **params):
#quando salvo, la stringa Json non lo passa nel body ma in params.
		Json_file=open('freeboard/dashboard/dashboard.json','w')
		Json_file.write(params['json_string'])
		Json_file.close()
#ogni volta che faccio il refresh deve comparire il widget
if __name__=='__main__':

	conf={
		'/':{
			'request.dispatch':cherrypy.dispatch.MethodDispatcher(),
			'tools.sessions.on': True,
			'tools.staticdir.root':	os.path.abspath(os.getcwd()) #qui sto dicendo qual'e' la root della cartella di contenuti statici. os.getcwd() ritorna il path dov'e' python in questo momento.
		},
		'/static':{
			'tools.staticdir.on':	True,	
			'tools.staticdir.dir':	'./freeboard'
		},
		'/css':{
			'tools.staticdir.on':	True,	
			'tools.staticdir.dir':	'./freeboard/css'
		},
		'/js':{
			'tools.staticdir.on':	True,	
			'tools.staticdir.dir':	'./freeboard/js'
		},
		'/dashboard':{
			'tools.staticdir.on':	True,	
			'tools.staticdir.dir':	'./freeboard/dashboard'
		},
		'/plugins':{
			'tools.staticdir.on':	True,	
			'tools.staticdir.dir':	'./freeboard/plugins'
		},
		'/img':{
			'tools.staticdir.on':	True,	
			'tools.staticdir.dir':	'./freeboard/img'
		}
	  }
cherrypy.quickstart(StringGeneratorWebService(),'/',conf)

#questa esperienza di laboratorio ci serve per capire come gestire dal nostro web-service una qualsiasi web app che ci viene data. quindi dobbiamo sapere aprire la sua pagina html e tutto cio' che serve ad html che sono css, js, etc.
