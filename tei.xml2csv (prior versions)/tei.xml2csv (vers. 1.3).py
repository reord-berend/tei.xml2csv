#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Import Beautiful Soup library
from bs4 import BeautifulSoup


# In[ ]:


path = '.xml'
with open(path, 'r', encoding="utf8") as tei:
    soup = BeautifulSoup(tei, 'lxml')


# In[ ]:


print('SOURCE:')

source_date = soup.find('source').find('date')
print('Source_date:', source_date['when'])

source_catalog_or_lot_number = soup.idno.string
print ('Source_catalog_or_lot_number =', source_catalog_or_lot_number)

institution = soup.find('institution')
repository = soup.find('repository')
print('Institution =', repository.string, ',', institution.string)

print('MANUSCRIPT DETAILS:')

titles = soup.mscontents.title
print('Title =', titles.string)

authors = soup.author
print('Authors =', authors.string)

# Dates may be given as attributes of 'origDate' element
date_range = soup.origdate
if date_range.has_attr('notbefore') and date_range.has_attr('notafter'):
    print('Dates =', date_range.string, '(', date_range['notbefore'], '-', date_range['notafter'], ')')
else:
    print('Dates =', date_range.string)

languages = soup.textlang
print('Languages =', languages.string)

materials = soup.supportdesc.support.p
print('Materials =', materials.string)


places = soup.origplace
print('Places =', places.string)


for el in soup.find_all('layout'):
    if el.has_attr('columns'):
        print('Num_columns =', el.attrs['columns'])
        
for el in soup.find_all('layout'):
    if el.has_attr('writtenlines'):
        print('Num_lines =', el.attrs['writtenlines'])
        
# For height and width, unit of measurement may be found as attributes of 3 possible elements
height = soup.find('height')
width = soup.find('width')

check_units = soup.find('dimensions') or soup.find('extent') or soup.find('height')
if check_units.has_attr('unit'):
    if check_units['unit'] == 'mm':
        print('Height =', height.string, 'mm')
        print('Width =', width.string, 'mm')
    
# Code to generate URL hyperlink to source record
manuscript_link = soup.find('msdesc')['xml:id']
is_vers = manuscript_link.endswith('-is')
if is_vers == True:
    manuscript_link = 'http://handrit.is/manuscript/view/is/' + manuscript_link[0:-3]
    print('Manuscript_link =', manuscript_link)
en_vers = manuscript_link.endswith('-en')
if en_vers == True:
    manuscript_link = 'http://handrit.is/manuscript/view/en/' + manuscript_link[0:-3]
    print('Manuscript_link =', manuscript_link)

