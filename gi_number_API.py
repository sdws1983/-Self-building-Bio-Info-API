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
			h = "useages:\nget the max length in all contigs or transcripts\n-i : inputfile\n-o : outputfile        "
	return input_file,output_file,h

def get_html(url):
	send_headers = {
		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36',
		'Accept':'*/*',
		'Connection':'keep-alive',
		'Host':'www.ncbi.nlm.nih.gov'
	}

	req = urllib.request.Request(url,headers = send_headers)
	response = urllib.request.urlopen(req)
	html = response.read().decode('utf-8')

	return html

def analyse(html):
	soup = BeautifulSoup(html,'lxml')
	for i in soup.find_all('pre'):
		#print (i)
		i = str(i)
		define_st = i.find('DEFINITION  ') + len('DEFINITION  ')
		define_en = i.find('[', define_st)
		define = i[define_st:define_en]
		#print (define)
		accession_st = i.find('ACCESSION   ') + len('ACCESSION   ')
		accession_en = i.find('\n', accession_st)
		accession = i[accession_st:accession_en]
		#print(accession)
		source_st = i.find('SOURCE      ') + len('SOURCE      ')
		source_en = i.find('\n', source_st)
		source = i[source_st:source_en]
		#print (source)
		geneid_st = (i.find('GeneID:') + len('GeneID:'))# if i.find('GeneID:') != -1 else 0
		geneid_en = i.find('</a>', geneid_st)
		geneid_soup = i[geneid_st:geneid_en]
		g_st = geneid_soup.find('>') + 1
		geneid = geneid_soup[g_st:] if geneid_st != 6 else "none"
		#print (geneid)
		symbol_st = i.find('gene_synonym="') + len('gene_synonym="')
		symbol_en = i.find('"', symbol_st)
		symbol = i[symbol_st:symbol_en] if symbol_st != 13 else "none"

		#break
	out = (define + "\t" + accession + "\t" + source + "\t" + geneid + "\n")
	return out, geneid, symbol

def analyse_geneid(html):
	soup = BeautifulSoup(html,'lxml')
	for i in soup.find_all('dl'):
		try:
			if i['id'] == "summaryDl":
				i = str(i)
				describe_st = (i.find('<dd>',i.find('Gene description')) + 4 )#if i.find('Gene description') != 0 else 0
				describe_en = i.find('</dd>',describe_st)
				describe = i[describe_st:describe_en] if i.find('Gene description') != -1 else "none"
				#print (describe)
				also_st = (i.find('<dd>', i.find('Also known as')) + 4 )# if i.find('Also known as') != 0 else 0
				also_en = i.find('</dd>', also_st)
				also = i[also_st:also_en] if i.find('Also known as') != -1 else "none"
				#print (also)


		except:
			describe = also = "none"
		return (describe + "\t" + also)

def parse_geneid(geneid):
	url_geneid = "https://www.ncbi.nlm.nih.gov/gene/" + geneid + "/data/"
	html_geneid = get_html(url_geneid)
	out_name = analyse_geneid(html_geneid)
	return out_name

if __name__ == "__main__":
	input_file,output_file,h = get_option()
	
	if input_file == "":
		gi = input("gi id:")
		print("gi-id\tdefine\taccession\tsource\tgeneid\tdescribe\talsoknowas")
		url = "https://www.ncbi.nlm.nih.gov/sviewer/viewer.fcgi?id=" + gi + "&db=protein"
		html = get_html(url)
		out, geneid, symbol = analyse(html)
		out2 = gi + "\t" + out
		if symbol == "none":
			try:
				print (out2[:-1] + "\t" + parse_geneid(geneid))
			except:
				print (out2[:-1] + "\t" + "none\tnone")
		else:
			print (out2[:-1] + "\t" + "none\t" + symbol)
	elif h == "":
		fh = open(output_file, 'w')
		fh.write("gi-id\tdefine\taccession\tsource\tgeneid\tdescribe\talsoknowas\n")
		with open(input_file) as f:
			for i in f:
				gi = i[:-1]
				print ("gi number:" + gi + " added...")
				url = "https://www.ncbi.nlm.nih.gov/sviewer/viewer.fcgi?id=" + gi + "&db=protein"
				html = get_html(url)
				out, geneid, symbol = analyse(html)
				out2 = gi + "\t" + out
				if symbol == "none":
					try:
						fh.write(out2[:-1] + "\t" + parse_geneid(geneid) + "\n")
					except:
						fh.write(out2[:-1] + "\t" + "none\tnone" + "\n")
				else:
					fh.write(out2[:-1] + "\t" + "none\t" + symbol + "\n")

