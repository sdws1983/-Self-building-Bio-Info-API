from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import re
import os
import sys, getopt

def get_option():
	opts, args = getopt.getopt(sys.argv[1:], "hi:o:")
	input_file = ""
	output_file = ""
	h = ""
	for op, value in opts:
		if op == "-i":
			input_file = value
		elif op == "-o":
			output_file = value
		elif op == "-h":
			h = "useages:\nget the max length in all contigs or transcripts\n-i : inputfile\n-o : outputfile"
	return input_file,output_file,h

def get_html(url):
	send_headers = {
		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36',
		'Accept':'*/*',
		'Connection':'keep-alive',
		'Host':'rest.kegg.jp'
	}

	req = urllib.request.Request(url,headers = send_headers)
	response = urllib.request.urlopen(req)
	html = response.read().decode('utf-8')

	return html

if __name__ == "__main__":
	url = "http://rest.kegg.jp/find/genes/"
	input_file,output_file,h = get_option()
	if input_file != "":
		fh = open(output_file, 'w')
		with open(input_file) as f:
			for gene in f:
				gene = gene[:-1]
				try:
					fh.write(get_html(url + gene))
				except:
					pass
		fh.close()
	else:
		try:
			gene = input("gene:")
			print (get_html(url + gene)[:-1])
		except:
			print ("gene name error!")

