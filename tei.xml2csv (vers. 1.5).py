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

# Find source catalogue number
source_catalog_or_lot_number = soup.idno.string
print ('Source_catalog_or_lot_number =', source_catalog_or_lot_number)

# Find source institution data
find_repository = soup.repository.string
find_institution = soup.institution.string

# This data can also be given as abbreviations in element attribute
find_repository_code = soup.repository
find_institution_code = soup.institution

# Sometimes this data is only given as attribute
if find_repository == None or find_institution == None:
    if find_repository_code.has_attr('key'):   
        find_repository = find_repository_code['key']
    if find_institution_code.has_attr('key'):    
        find_institution = find_institution_code['key']   
# Here we combine the two elements    
institution = find_repository + ', ' + find_institution
print('Institution =', institution)


print('MANUSCRIPT DETAILS:')

titles = soup.mscontents.title
titles = titles.string
print('Titles =', titles)

authors = soup.author
if authors == True:
    authors = authors.string
    print('Authors =', authors)

# To find manuscript dates
find_dates = soup.origdate
# May also have values given as attributes of 'origDate' element
if find_dates.has_attr('notbefore') and find_dates.has_attr('notafter'):
    # Date range to be included in parentheses
    dates_range = '(' + find_dates['notbefore'] + '-' + find_dates['notafter'] + ')'
    # Now that attribute values have been extracted, we can remove elements and attributes
    dates = find_dates.string
    # Text in this field is sometimes separated by new lines or repeated tabs, which must be removed
    if '\n' in dates or '\t' in dates == True:
        dates = dates.replace('\n', '')
        dates = dates.replace('\t', '')
   # Now we can combines text with 
    dates = dates + ' ' + dates_range
    print('Dates =', dates)
else:
    dates = find_dates.string
    # Text in this field is sometimes separated by new lines or repeated tabs, which must be removed
    if '\n' in dates or '\t' in dates == True:
        dates = dates.replace('\n', '')
        dates = dates.replace('\t', '')
    print('Dates =', dates)

# To find manuscript language
languages = soup.find('textlang')
# Element 'textLang' is not always present
if languages is not None:
# Languages may also be given as two-letter codes, differentiated by 'main' and 'other'
    if languages.has_attr('mainlang'):
        language_codes = languages['mainlang']
    if languages.has_attr('otherlangs'):
        language_codes = languages['otherlangs']
    if languages.has_attr('mainlang') and languages.has_attr('otherlangs'):
        language_codes = languages['mainlang'] + ', ' + languages['otherlangs']
    # Now that attribute values have been extracted, we can remove elements and attributes
    languages = languages.string
    # Text in this field is sometimes separated by new lines or repeated tabs, which must be removed
    if '\n' in languages or '\t' in languages:
        languages = languages.replace('\n', '')
        languages = languages.replace('\t', '')
    # Language codes, if present, are included in parentheses
    if language_codes != '':
        languages = languages + ' (' + language_codes + ')'
# If 'textLang' is not present, an empty value is desired (instead of 'None')
if languages == None:
    languages = ''
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
    else:
        num_columns = None
for el in soup.find_all('layout'):
    if el.has_attr('writtenlines'):
        num_lines = el.attrs['writtenlines']
        print('Num_lines =', num_lines)
    else:
        num_lines = None

if soup.layout == None:
    num_lines = None
    num_columns = None
        
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
new_row = ['', '', '', 'TBD', 'Handrit.org', source_catalog_or_lot_number, institution, titles, dates, languages, materials, places, num_columns, num_lines, height, width, manuscript_link]
print('New_row =', new_row)

