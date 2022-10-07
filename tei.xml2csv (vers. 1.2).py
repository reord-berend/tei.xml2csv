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
source_date = soup.source.date.string
print('Source Date =', source_date)
source_catalog_or_lot_number = soup.idno.string
print ('Source Catalog or Lot Number =', source_catalog_or_lot_number)
country = soup.msidentifier.country.string
for el in soup.find_all('institution'):
    if el.has_attr('key'):
        print('Institution =', el.attrs['key'], country)
print('MANUSCRIPT DETAILS:')
titles = soup.mscontents.title
print('Title =', titles.string)
authors = soup.find('author')
print('Authors =', authors)
dates = soup.origdate.string
print('Dates =', dates)
languages = soup.textlang.string
print('Languages =', languages)
materials = soup.support.material
print('Materials =', materials.string)
places = soup.origplace.string
print('Places =', places)
for el in soup.find_all('layout'):
    if el.has_attr('columns'):
        print('Number of Columns =', el.attrs['columns'])
for el in soup.find_all('layout'):
    if el.has_attr('writtenlines'):
        print('Number of Lines =', el.attrs['writtenlines'])
height = soup.height.string
print('Height =', height, 'mm')
width = soup.width.string
print('Width =', width, 'mm')

