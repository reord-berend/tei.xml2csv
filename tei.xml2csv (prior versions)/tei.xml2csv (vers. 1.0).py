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


titles = soup.summary.title
authors = soup.find('author')
dates = soup.origdate.string
materials = soup.material
languages = soup.textlang.string
height = soup.height.string
width = soup.width.string


print('Title =', titles.string)
print('Authors =', authors)
print('Dates =', dates)
print('Materials =', materials.string)
print('Languages =', languages)
print('Height =', height, 'mm')
print('Width =', width, 'mm')
