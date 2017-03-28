from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import re

def get_html(url):
	send_headers = {
		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36',
		'Accept':'*/*',
		'Connection':'keep-alive',
		'Host':'www.maizegdb.org'
	}

	req = urllib.request.Request(url,headers = send_headers)
	response = urllib.request.urlopen(req)
	html = response.read().decode('utf-8')

	return html

def analyse(html):
	all = []
	a = b = c = d = e = 'none'
	soup = BeautifulSoup(html,'lxml')
	for i in soup.find_all('div'):
		all.append(i)
	product = str(all[0]).split('\n')
	ortholog = str(all[1]).split('\n')
	for i in ortholog:
		t1 = i.find('target="_blank">') + len('target="_blank">')
		t2 = i.find('</a>', t1)
		t = i[t1:t2] if t1 != 15 else "none"
		if 'Sorghum' in str(i) and 'found' not in str(i):
			a = (t)
		if 'Foxtail millet' in str(i) and 'found' not in str(i):
			b = (t)
		if 'Rice' in str(i) and 'found' not in str(i):
			c = (t)
		if 'Brachypodium' in str(i) and 'found' not in str(i):
			d = (t)

	for i in product:
		if 'gene_product' in str(i):
			t1 = i.find('>') + 1
			t2 = i.find('</a')
			e = (i[t1:t2])

	return (a + "\t" + b + "\t" + c + "\t" + d + "\t" + e)

if __name__ == "__main__":
	fh = open('maizeGDB-ortholog-and-product-annotation.txt', 'w')
	with open('Zmays_V3-genes-list.txt') as f:
		for gene in f:
			gene = gene[:-1]
			url = "http://ajax1.maizegdb.org/record_data/gene_data.php?id=" + str(gene) + "&type=overview"
			html = get_html(url)
			try:#print (html)
				annotation = analyse(html)
				fh.write(gene + "\t" + annotation + "\n")
			except:
				fh.write("error" + "\t" + gene + "\n")
