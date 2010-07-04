#!/usr/bin/python
# -*- coding: utf8 -*-
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
		print "USAGE: musorg -i diretorio_de_entrada/ -o diretorio_de_saida  {modo de operação}"

		exit(1)
	elif erro == "help":
		print "USAGE: musorg -i diretorio_de_entrada/ -o diretorio_de_saida {modo de operação}"
		print "-i especifica o diretório onde estao as entradas"
		print "-r busca recursiva de entradas (PADRÃO)"
		print "-o especifica diretório de saída"
		print "ao especificar entradas e saidas inserir o caminho completo do diretório incluindo a barra no final do ultimo subdiretório"
		print"modo de operação:"
		print"-m: move arquivos para um novo diretório"
		print"-c: copia arquivos para um novo diretório"
		exit(1)
	elif erro =="sem modo":
		print"selecione um modo de operação:"
		print"-m: move arquivos para um novo diretório"
		print"-c: copia arquivos para um novo diretório"
		exit(1)
		
		
		
def print_all(dirdst=None,filedst=None,arquivo=None,tag=None,extensao=None):
	if (tag!=None and dirdst!=None and filedst!=None and arquivo!=None and extensao):
		try:
			print "\tcopiando arquivo %s -->> %s"%(arquivo,dirdst+filedst)
		except:
			print"error"
		print "\tMusica: %s"%(tag.title)
		print "\tArtista: %s"%(tag.artist)
		print "\tAlbum: %s"%(tag.album)
		print "\tfaixa: %d"%(tag.track)
		print "\tano: %d"%(tag.year)
	else: 
		#print "algo"
		print "%s:	faixa sem tags"%(arquivo)
	



def setdirdst(tag,saida):
	if(tag.artist and tag.album) != "" and (tag.year)!=0:
	
		dirdst = saida+"%s%s%s%s - %s%s"%(os.sep,tag.artist,os.sep,tag.year,tag.album,os.sep)
	elif(tag.artist and tag.album) != "":
		dirdst = saida+"%s%s%s%s"%(tag.artist,os.sep,tag.album,os.sep)
	elif(tag.artist) != "":
		dirdst = saida+"%s%s"%(tag.artist,os.sep)
	else:
		dirdst = 0
	return dirdst





def setfiledst(tag,extensao):
	if(tag.title) != "" and (tag.title)!=0:
		
		filedst = "%s - %s.%s"%(tag.track,tag.title,extensao)
		
		
	elif(tag.title) != "":
		filedst = "%s.%s"%(tag.title,extensao)
		
	else:
		filedst = 0
	return filedst
			

def mover(dirdst,filedst,arquivo,tag,extensao,n=0):
	if (os.path.isfile(dirdst+filedst)) is False:
		 
		try:
			shutil.move(arquivo, dirdst+filedst)
		except:
			print "erro de E/S"
	else: 
		
		extensao2 ="%s.%s"%(n+1,extensao)
		filedst2=setfiledst(tag,extensao2)
		
		if os.path.isfile(dirdst+filedst2):
			mover(dirdst,filedst,arquivo,tag,extensao,n+1)
		else:
			try:
				shutil.move(arquivo, dirdst+filedst2)
			except:
				print"erro de E/S"	
						
def copiar(dirdst,filedst,arquivo,tag,extensao,n=0):
	if (os.path.isfile(dirdst+filedst)) is False:
		 
		try:
			shutil.copyfile(arquivo, dirdst+filedst)
		except:
			print "erro de E/S"
	else: 
		
		extensao2 ="%s.%s"%(n+1,extensao)
		filedst2=setfiledst(tag,extensao2)
		
		if os.path.isfile(dirdst+filedst2):
			copiar(dirdst,filedst,arquivo,tag,extensao,n+1)
		else:
			try:
				shutil.copyfile(arquivo, dirdst+filedst2)
			except:
				print"erro de E/S"
				
				
				
				
				

def run(arquivo,extensao,saida,mode):
	a = tagpy.FileRef(arquivo)
	tag = a.tag()
	
	dirdst = setdirdst(tag,saida)
	if dirdst == 0:
		print_all(arquivo)
		return 0
		
		
	
	filedst = setfiledst(tag,extensao)
	if filedst == 0:
		print_all()
		return 0	
	#print dirdst+filedst
	
	try:
		os.makedirs(dirdst)
	except :
		pass
	print_all(arquivo,dirdst,filedst,tag,extensao)
	if mode ==1:
		mover(dirdst,filedst,arquivo,tag,extensao)
	elif mode ==2:
		copiar(dirdst,filedst,arquivo,tag,extensao)
	else:
		pass
	
	
	
	
	
	
	
def main():
	entrada = ""
	saida = ""
	ext = ["mp3","mp4","m4a""aac","ogg","oga"]
	mode = 0
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
	
	if '-m' in sys.argv:
		mode = 1
	elif '-c' in sys.argv:
		mode = 2
	else:
		erros("sem modo")
	for item in os.walk(entrada):
		#print item
		diretorio = item[0] 
		for arquivo in item[2]:
			try:
				fileext = arquivo[arquivo.rindex(".")+1:].lower()
				print arquivo
				
			except:
				fileext = ""
				print"erro ao processar %s	arquivo sem extensão"%(arquivo)
			if fileext in ext:
				print arquivo
				run("%s%s%s"%(diretorio, os.sep, arquivo),fileext,saida,mode)
	
	
		
		
		
		


main()
