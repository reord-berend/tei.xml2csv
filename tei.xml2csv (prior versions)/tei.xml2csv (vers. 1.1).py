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


source_date = soup.source.date.string
source_catalog_or_lot_number = soup.idno.string
titles = soup.summary.title
authors = soup.find('author')
dates = soup.origdate.string
languages = soup.textlang.string
materials = soup.material
places = soup.origplace.string
height = soup.height.string
width = soup.width.string

print('Source Date =', source_date)
print ('Source Catalog or Lot Number =', source_catalog_or_lot_number)
print('Title =', titles.string)
print('Authors =', authors)
print('Dates =', dates)
print('Languages =', languages)
print('Materials =', materials.string)
print('Places =', places)
print('Height =', height, 'mm')
print('Width =', width, 'mm')


country = soup.msidentifier.country.string
for el in soup.find_all('institution'):
    if el.has_attr('key'):
        print('Institution =', el.attrs['key'], country)

for el in soup.find_all('layout'):
    if el.has_attr('columns'):
        print('Number of Columns =', el.attrs['columns'])
for el in soup.find_all('layout'):
    if el.has_attr('writtenlines'):
        print('Number of Lines =', el.attrs['writtenlines'])

