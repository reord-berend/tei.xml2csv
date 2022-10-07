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

# Source date can be found as value of 'when' attribute within two possible elements
find_source_date = soup.find('publicationstmt').find_all('date') or soup.find('source').find_all('date')
for date in find_source_date:
    if date.has_attr('when'):
        source_date = date['when']
        print('Source_date =', source_date)


source_catalog_or_lot_number = soup.idno.string
print ('Source_catalog_or_lot_number =', source_catalog_or_lot_number)

find_institution = soup.find('institution')
find_repository = soup.find('repository')
institution = find_repository.string + ', ' + find_institution.string
print('Institution =', institution)

print('MANUSCRIPT DETAILS:')

titles = soup.mscontents.title
titles = titles.string
print('Titles =', titles)

authors = soup.author
if authors == True:
    authors = authors.string
    print('Authors =', authors)

# Code to find manuscript dates
find_dates = soup.origdate
# Dates values may be given as attributes of 'origDate' element
if find_dates.has_attr('notbefore') and find_dates.has_attr('notafter'):
    dates = find_dates
    # Text in this field is sometimes separated by new lines or repeated tabs, which must be removed
    dates = dates.replace('\n', '')
    dates = dates.replace('\t', '')
    # Date range is included in parentheses
    dates_range = '(' + find_dates['notbefore'] + '-' + find_dates['notafter'] + ')'
    dates = dates + ' ' + dates_range
    print('Dates =', dates)
else:
    dates = find_dates.string
    # Text in this field is sometimes separated by new lines or repeated tabs, which must be removed
    dates = dates.replace('\n', '')
    dates = dates.replace('\t', '')
    print('Dates =', dates)

# Code to find the manuscript language    
languages = soup.textlang
# Languages may also be given as two-letter codes
if languages.has_attr('mainlang') or languages.has_attr('otherlangs'):
    language_codes = languages['mainlang'] + ', ' + languages['otherlangs']
languages = languages.string
# Text in this field is sometimes separated by new lines or repeated tabs, which must be removed
languages = languages.replace('\n', '')
languages = languages.replace('\t', '')
# Language codes are included here in parentheses
languages = languages + ' (' + language_codes + ')'
print('Languages =', languages)

    
# Code to find manuscript material
find_materials = soup.find('supportdesc').find('support')

# Pre-defined abbreviated data for manuscript material may also be given as attribute of 'supportDesc' element
find_materials_value = soup.find('supportdesc')
if find_materials_value.has_attr('material'):
    material_value = find_materials_value['material']

# Primary data may be found w/in 3 possible child tags
for el in find_materials.children:
    if el == soup.find('support'):
        materials = el.string
        # Abbreviated data to be included here in parentheses
        materials = materials + " (" + material_value + ")"
        print('Materials =', materials)
    if el == soup.find('support').find('p'):
        materials = el.string
        # Abbreviated data to be included here in parentheses
        materials = materials + " (" + material_value + ")"
        print('Materials =', materials)
    if el ==soup.find('support').find('p').find('material'):
        materials = el.string
        # Abbreviated data to be included here in parentheses
        materials = materials + " (" + material_value + ")"
        print('Materials =', materials)

places = soup.origplace
places = places.string
print('Places =', places)

# For number of columns and written lines, these are found as possible attributes within the 'layout' element
for el in soup.find_all('layout'):
    if el.has_attr('columns'):
        num_columns = el.attrs['columns']
        print('Num_columns =', num_columns)       
for el in soup.find_all('layout'):
    if el.has_attr('writtenlines'):
        num_lines = el.attrs['writtenlines']
        print('Num_lines =', num_lines)
        
# Code to find height and width measurements
height = soup.find('height')
width = soup.find('width')
# For height and width, unit of measurement may be found as attributes of 3 possible elements
check_units = soup.find('dimensions') or soup.find('extent') or soup.find('height')
if check_units.has_attr('unit'):
    if check_units['unit'] == 'mm':
        height = height.string + ' ' + 'mm'
        print('Height =', height)
        width = width.string + ' ' + 'mm'
        print('Width =', width)
        
        
    
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

print('IMPORT TO CSV:')
# To generate list for import into CSV file
new_row = [source_date, source_catalog_or_lot_number, institution, titles, dates, languages, materials, places, num_columns, num_lines, height, width, manuscript_link]
print('New_row =', new_row)

