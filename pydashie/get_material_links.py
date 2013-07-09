from bs4 import BeautifulSoup
import infofile
import urllib
import googleanalytics_apiaccess_timeseries_try as gatt 

# correct response?
def get_material_links(course_mat_pg=infofile.pgpath):
	html_doc = urllib.urlopen('http://open.umich.edu%s/materials' % course_mat_pg)

	soup = BeautifulSoup(html_doc)
	#print soup.prettify()
	filenames = []
	begin = len("http://open.umich.edu/sites/default/files/")
	for link in soup.find_all('a'):
		#if 'sites/default/files' in link.get('href'):
		the_href = str(link.get('href'))
		if 'sites/default/files' in the_href:
			#print the_href # finding all downloads links/event places -- currently printing to console
			# in all of these, want a list of the strings that come after the /files/ bit
			filenames.append(the_href[begin:])
	# for x in filenames:
	# 	print x
	return filenames

if __name__ == '__main__':

	get_material_links()