#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Import Beautiful Soup library
from bs4 import BeautifulSoup


# In[ ]:


# Import regular expressions module
import re
# Text in certain fields is sometimes separated by superfluous whitespace, which must be removed
# Whitespace typically consists of new lines, tabs, or repeated spaces
# To ensure that normal spacing is maintained between words, all whitespace characters are replaced with a single space
def clean_string(string):
    
    """Function to replace 1 or more whitespace chars ('\s+') with a single
    space (' ') and strip leading and trailing whitespace.

    Usage:

        string = " This is\tsome   string\r\n    to clean.     \r\n"
        clean_string(string)  # => "This is some string to clean."
    """
    # \s = whitespace characters
    # \s = [ \t\n\r\f\v]
    # \s = space, tab, newline, carriage return, form feed, vertical space
    # \s+ = one or more repetitions of regular expression
    new_string = re.sub('\s+', ' ', string)
    # Now remove any leading or trailing whitespace characters
    new_string = new_string.strip()
    
    return new_string


# In[ ]:


def get_attr(tag, attr, default=''):
    """Write a function to return the attribute if 'tag.has_attr(attr)' or
    return 'default'.
    """
    pass


# In[ ]:


# Open file handle and read with lxml parser
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

# To find manuscript author (which is often unknown, and thus element is not present)
authors = soup.find('author')
if authors is not None:
    authors = authors.string
    print('Authors =', authors)

# To find manuscript dates
find_dates = soup.find('origdate')
dates = ''
dates_range = ''
# Element 'origDate' is sometimes (albeit rarely) not present
if find_dates is not None:
    # There may also be values given as attributes of 'origDate' element
    if find_dates.has_attr('notbefore') and find_dates.has_attr('notafter'):
        # Date range to be included in parentheses
        dates_range = '(' + find_dates['notbefore'] + '-' + find_dates['notafter'] + ')'
    # Now that attribute values have been extracted, we can remove elements and attributes
    dates = find_dates.string
    # If there are multiple values in this element, it will not be clear what .string should refer to and will return 'None'
    if dates is None:
        # Using .text will get all child strings and return concatenated
        dates = find_dates.text
        # As alternative, try find_dates.get_text(separator=' ', strip=True)
        # The parameters:
        # strip=True ensures that we don’t have any newlines from the original XML document
        # separator=' ' specifies which character (or string) we want to use as delimiter between subelements/children
    # Text in this field is sometimes separated by superfluous whitespace, which must be removed
    dates = clean_string(dates)
    # Now we can combines 'dates' with 'date range' (if present)
    if dates_range != '':
        dates = dates + ' ' + dates_range
        print('Dates =', dates)
    else:
        print('Dates =', dates)
if find_dates is None:
    # Sometimes date is not given in 'origDate' element, but simply in 'origin'
    find_dates = soup.find('origin')
    if find_dates is not None:
    # There may also be values given as attributes of 'origin' element
        if find_dates.has_attr('when') and find_dates.has_attr('to'):
            dates = find_dates['when'] + '-' + find_dates['to']
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
    # Text in this field is sometimes separated by superfluous whitespace, which must be removed
    languages = clean_string(languages)
    # Language codes, if present, are included in parentheses
    if language_codes != '':
        languages = languages + ' (' + language_codes + ')'
# If 'textLang' is not present, an empty value is desired (instead of 'None')
if languages == None:
    languages = ''
print('Languages =', languages)
    
    
# To find manuscript material
find_materials = soup.find('supportdesc').find('support')

# Pre-defined abbreviated data for manuscript material may also be given as attribute of 'supportDesc' element
find_materials_value = soup.find('supportdesc')
if find_materials_value.has_attr('material'):
    material_value = find_materials_value['material']

# Primary data may be found within 3 possible child tags (to be checked in succession)
for el in find_materials.children:
    if soup.p.material:
        materials = soup.p.material
        materials = materials.string
        if material_value is not None:
            # Abbreviated data to be included here in parentheses
            materials = materials + " (" + material_value + ")"
    if soup.p.material is None:
        if soup.support.p:
            materials = soup.support.p
            materials = materials.string
            if material_value is not None:
                # Abbreviated data to be included here in parentheses
                materials = materials + " (" + material_value + ")"
        if soup.support.p is None:
            if soup.support:
                materials = soup.support
                materials = materials.string
                if material_value is not None:
                    # Abbreviated data to be included here in parentheses
                    materials = materials + " (" + material_value + ")"

print('Materials =', materials)
    

places = soup.find('origplace')
if places is not None:
    places = places.string
# If data not present, replace 'None' with empty value
if places is None:
    places = ''
print('Places =', places)

# For number of columns and written lines, these are found as possible attributes within the 'layout' element
for el in soup.find_all('layout'):
    if el.has_attr('columns'):
        num_columns = el.attrs['columns']
        print('Num_columns =', num_columns)
    else:
        # If data not present, replace 'None' with empty value
        num_columns = ''
for el in soup.find_all('layout'):
    if el.has_attr('writtenlines'):
        num_lines = el.attrs['writtenlines']
        print('Num_lines =', num_lines)
    else:
        # If data not present, replace 'None' with empty value
        num_lines = ''
# If data not present, replace 'None' with empty value
if soup.layout is None:
    num_lines = ''
    num_columns = ''

        
# To find height and width measurements
height = soup.find('height')
width = soup.find('width')

# For height and width, unit of measurement may be found as attributes of several possible elements 
check_units = (soup.height and soup.width) or soup.dimensions or soup.extent
if check_units.has_attr('unit'):
    if check_units['unit'] == 'mm':
        height = height.string + ' ' + 'mm'
        print('Height =', height)
        width = width.string + ' ' + 'mm'
        print('Width =', width)
# If data not present, replace 'None' with empty value
if height is None:
    height = ''
if width is None:
    width = ''
    
# To generate URL hyperlink to source record
manuscript_link = soup.find('msdesc')['xml:id']
is_vers = manuscript_link.endswith('-is')
if is_vers == True:
    manuscript_link = 'http://handrit.is/manuscript/view/is/' + manuscript_link[0:-3]
    print('Manuscript_link =', manuscript_link)
en_vers = manuscript_link.endswith('-en')
if en_vers == True:
    manuscript_link = 'http://handrit.is/manuscript/view/en/' + manuscript_link[0:-3]
    print('Manuscript_link =', manuscript_link)
da_vers = manuscript_link.endswith('-da')
if da_vers == True:
    manuscript_link = 'http://handrit.is/manuscript/view/da/' + manuscript_link[0:-3]
    print('Manuscript_link =', manuscript_link)

print('IMPORT TO CSV:')

# To generate list for import into CSV file
new_row = ['', '', '', 'TBD', 'Handrit.org', source_catalog_or_lot_number, institution, titles, dates, languages, materials, places, num_columns, num_lines, height, width, manuscript_link]
print('New_row =', new_row)

