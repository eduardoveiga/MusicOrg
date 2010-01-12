#!/usr/bin/python
# -*- coding: latin1 -*-
#       mp3org-0.0.5
#       
#       Copyright 2010 Eduardo Veiga <edu@bsd.com.br>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

import shutil,tagpy,os,sys

    
def erros(erro):
	if erro == "sem saída":
		print "você não especificou qual o diretório de saída"
		print "ex: -o /home/usuário/diretório/"
		exit()
	elif erro == "usage":
		print "USAGE: musorg -i diretorio_de_entrada/ -o diretorio_de_saida"
		exit(1)
	elif erro == "help":
		print "USAGE: musorg -i diretorio_de_entrada/ -o diretorio_de_saida"
		print "-i especifica o diretório onde estao as entradas"
		print "-r busca recursiva de entradas (PADRÃO)"
		print "-o especifica diretório de saída"
		print "ao especificar entradas e saidas inserir o caminho completo do diretório incluindo a barra no final do ultimo subdiretório"
		exit(1)

def setdirdst(tag,saida):
	if(tag.artist and tag.album) != "" and (tag.year)!=0:
	
		dirdst = saida+"%s%s%s - %s%s"%(tag.artist,os.sep,tag.year,tag.album,os.sep)
		print "tags is true"
	elif(tag.artist and tag.album) != "":
		dirdst = saida+"%s%s%s%s"%(tag.artist,os.sep,tag.album,os.sep)
	elif(tag.artist) != "":
		dirdst = saida+"%s%s"%(tag.artist,os.sep)
	else:
		print "faixa sem tags"
		dirdst = 0
	return dirdst

def setfiledst(tag,extensao):
	if(tag.title) != "" and (tag.title)!=0:
		
		filedst = "%s - %s.%s"%(tag.track,tag.title,extensao)
		
		
	elif(tag.title) != "":
		filedst = "%s.%s"%(tag.title,extensao)
		
	else:
		print "faixa sem tags"
		filedst = 0
	return filedst
			
def copiar(dirdst,filedst,arquivo,tag,extensao,n=0):
	if (os.path.isfile(dirdst+filedst)) is False:
		 
		shutil.copyfile(arquivo, dirdst+filedst)
	else: 
		
		extensao2 ="%s.%s"%(n+1,extensao)
		filedst2=setfiledst(tag,extensao2)
		
		if os.path.isfile(dirdst+filedst2):
			copiar(dirdst,filedst,arquivo,tag,extensao,n+1)
		else:
			shutil.copyfile(arquivo, dirdst+filedst2)

def run(arquivo,extensao,saida):
	a = tagpy.FileRef(arquivo)
	tag = a.tag()
	print "artista:",tag.artist
	print "ano",tag.year
	print "album:",tag.album
	print "faixa:",tag.track
	print "título:",tag.title
	
	dirdst = setdirdst(tag,saida)
	if dirdst == 0:
		return 0
		
	print "dirdst: ",dirdst
	
	filedst = setfiledst(tag,extensao)
	if filedst == 0:
		return 0	
	print "filedst: ",filedst
	#print dirdst+filedst
	
	try:
		os.makedirs(dirdst)
	except :
		pass
	copiar(dirdst,filedst,arquivo,tag,extensao)
	
	
	
	
def main():
	entrada = ""
	saida = ""
	ext = ["mp3","mp4","m4a""aac","ogg","oga"]
	if len(sys.argv) == 1:
		erros("usage")
	if ((sys.argv[1] ==  "-h") or (sys.argv[1] == "--help")):

		erros("help")
	else:
		pass
	for index,item in enumerate(sys.argv):
		if item == "-i":
			entrada = sys.argv[index+1]
	if entrada is "":
		entrada = os.getcwd()
	
	for index,item in enumerate(sys.argv):
		if item == "-o":
			saida = sys.argv[index+1]
	if saida is "":
		erros("sem saída")	
	
	for item in os.walk(entrada):
		#print item
		diretorio = item[0] 
		for arquivo in item[2]:
			print "arquivo: ",arquivo
			try:
				fileext = arquivo[arquivo.rindex(".")+1:].lower()
			except:
				pass
			if fileext in ext:
				run("%s%s%s"%(diretorio, os.sep, arquivo),fileext,saida)
	
	
		

	print "argv = ",sys.argv
	print "entrada = ",entrada
	print "saida = ",saida


main()

