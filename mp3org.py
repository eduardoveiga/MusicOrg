#!/usr/bin/python
# -*- coding: latin1 -*-
#       mp3org-0.0.0002
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
		print "Help...I Need Somebody"
		exit(1)
		
def mover(arquivo,extensao,saida):
	a = tagpy.FileRef(arquivo)
	tag = a.tag()
	print "artista:",tag.artist
	print "ano",tag.year
	print "album:",tag.album
	print "faixa:",tag.track
	print "título:",tag.title
	
	if(tag.artist and tag.year and tag.album) != "":
	
		dirdst = saida+"%s%s%s - %s%s"%(tag.artist,os.sep,tag.year,tag.album,os.sep)
		print "tags is true"
	elif(tag.artist and tag.album) != "":
		dirdst = saida+"%s%s%s%s"%(tag.artist,os.sep,tag.album,os.sep)
	elif(tag.artist) != "":
		distsf = saida+"%s%s"%(tag.artist,os.sep)
	else:
		print "faixa sem tags"
		return 0
	if(tag.track and tag.title) != "":
		
		filedst = "%s - %s.%s"%(tag.track,tag.title,extensao)
	elif(tag.title) != "":
		filedst = "%s.%s"%(tag.title,extensao)
	else:
		print "faixa sem tags"
		return 0
	print dirdst+filedst
	
	try:
		os.makedirs(dirdst)
	except :
		pass
	if (os.path.isfile(dirdst+filedst)) is False:
		 
		shutil.copyfile(arquivo, dirdst+filedst)
	else: 
		shutil.copyfile(arquivo, dirdst+filedst+extensao)
	
	
	
	
def main():
	entrada = ""
	saida = ""
	ext = ["mp3","mp4","m4a""aac","ogg","oga"]
	if len(sys.argv) is 1:
		erros("usage")
	if sys.argv[1] is "-h" or "--help":
		erros("help")
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
				mover("%s%s%s"%(diretorio, os.sep, arquivo),fileext,saida)
	
	
		

	print "argv = ",sys.argv
	print "entrada = ",entrada
	print "saida = ",saida


main()
