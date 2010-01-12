#!/usr/bin/python
# -*- coding: latin1 -*-
#       mp3org-0.0.0001
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

import shutil,tagpy
import re, os, sys, random, bz2, urllib, time, shelve
from unicodedata import normalize


try:
    import psyco
    psyco.full()
    psy = True
except:
    psy = False
    pass
    
    
def erros(erro):
	if erro == "sem saída":
		print "você não especificou qual o diretório de saída"
		print "ex: -o /home/usuário/diretório/"
		exit()
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
	
	
	os.makedirs(dirdst)
	
		
	
		 
	shutil.copyfile(arquivo, dirdst+filedst)
	
	
	
	
	
def main():
	entrada = ""
	saida = ""
	lista = ""
	ext = ["mp3","mp4","m4a""aac","ogg","oga"]
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
			fileext = arquivo[arquivo.rindex(".")+1:].lower()
			if fileext in ext:
				mover("%s%s%s"%(diretorio, os.sep, arquivo),fileext,saida)
	
	
		

	print "argv = ",sys.argv
	print "entrada = ",entrada
	print "saida = ",saida


main()
