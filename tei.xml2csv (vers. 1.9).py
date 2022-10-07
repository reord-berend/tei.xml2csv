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


# Elements might exist in some records but not others
# If we reference an element that does not exist, BeautifulSoup will yield an AttributeError 
# This can be bypassed by defining a function which retrieves the text only if the tag exists
def elem_to_text(elem, default=''):
    """ Function to retrieve text only if tag exists. """
    # To pass the argument, use soup.elem
    # e.g., element_to_text(soup.title)
    if elem:
        # Call clean_string function to remove superfluous whitespace
        return clean_string(elem.getText())
    else:
        return default


# In[ ]:


# Some elements have attributes which might exist in some records but not others
def get_attr(tag, attr, default=''):
    """Function to return the attribute value if present 
    or return 'default'.
    """
    # First we check if the element exists
    tag = soup.find(tag)
    if tag:
        # Next we check if the element has the desired attribute
        if tag.has_attr(attr):
            return tag[attr]
        else:
            return default
    else:
        return default


# In[ ]:


# Import python API for google translate
# Google_trans_new package already included in Anaconda, no install necessary
# Documentation can be found at https://github.com/lushan88a/google_trans_new
# Further documentation at https://pypi.org/project/google-trans-new/
""" Would not run on 8/17/22, received error message: "JSONDecodeError: Extra data: line 1 column 343 (char 342)"
in file /lib/python3.10/site-packages/google_trans_new/google_trans_new.py, 
line 151 was changed from "response = (decoded_line + ']')" to "response = (decoded_line + '')"
"""
from google_trans_new import google_translator
translator = google_translator()  

def translate_text(string):
    # To determine source language 
    lang_code = get_attr('msdesc', 'xml:lang')
    if lang_code == 'is':
        translated_text = translator.translate(string, lang_src='is', lang_tgt='en') 
        return translated_text
    if lang_code == 'da':
        translated_text = translator.translate(string, lang_src='da', lang_tgt='en') 
        return translated_text
    if lang_code == 'en':
        return string


# In[ ]:


# Define a function to open a TEI-XML document and read with lxml parser
def read_tei(tei_file):
    with open(tei_file, 'r', encoding="utf8") as tei:
        soup = BeautifulSoup(tei, 'lxml')
        return soup
    raise RuntimeError('Cannot generate a soup from the input')


# In[ ]:


path = '.xml'
soup = read_tei(path)


# In[ ]:


print('SOURCE:')

# Find source catalogue number
source_catalog_or_lot_number = elem_to_text(soup.idno)
print ('Source_catalog_or_lot_number =', source_catalog_or_lot_number)

# Find source institution data (pulling values from two different elements)
find_repository = elem_to_text(soup.repository)
find_institution = elem_to_text(soup.institution)

# Sometimes these data are only given in abbreviated form as an attribute
# If the aforementioned fields are blank, then we must search for these attributes
if find_repository == '':
    find_repository = get_attr('repository', 'key')
if find_institution == '':
    find_institution = get_attr('institution', 'key')

# Finally, we combine the two values   
institution = find_repository + ', ' + find_institution
print('Institution =', institution)


print('MANUSCRIPT DETAILS:')

# To find manuscript title
titles = elem_to_text(soup.mscontents.title)
print('Titles =', titles)

# To find manuscript author
authors = elem_to_text(soup.author)
print('Authors =', authors)

# To find manuscript dates
find_dates = elem_to_text(soup.origdate)
# Dates may also be given as attributes of this element
dates_start_range = get_attr('origdate', 'notbefore')
# While 'notBefore' is the most common attribute, this can also be given as 'from'
if dates_start_range == '':
    dates_start_range = get_attr('origdate', 'from')
    # Rarely, this can be given as 'when'
    if dates_start_range == '':
        dates_start_range = get_attr('origdate', 'when')
dates_end_range = get_attr('origdate', 'notafter')
# While 'notAfter' is the most common attribute, this can also be given as 'to'
if dates_start_range == '':
    dates_start_range = get_attr('origdate', 'to')
# Date range, if these values exist, are to be combined and included in parentheses
if dates_start_range != '' and dates_end_range != '':
    dates_range = '(' + dates_start_range + '-' + dates_end_range + ')'
    dates = find_dates + ' ' + dates_range
    print('Dates =', dates)
else:
    dates = find_dates
    print('Dates =', dates)
    
# Sometimes (albeit rarely) the date is not given in 'origDate' element, but simply as attributes of 'origin'
if find_dates == '':
    dates_start = get_attr('orig', 'when')
    if dates_start == '':
        dates_start = get_attr('orig', 'from')
    dates_end = get_attr('orig', 'to')
    if dates_start != '' and dates_end != '':
        dates = dates_start + '-' + dates_end
        print('Dates =', dates) 
    

# To find manuscript language
languages = elem_to_text(soup.textlang)
languages = translate_text(languages)
# Languages may also be given as two-letter codes, differentiated by 'main' and 'other'
lang_code_main = get_attr('textlang', 'mainlang')
lang_code_other = get_attr('textlang', 'otherlangs')
# If both codes are present, they are to be included in parentheses
if lang_code_main != '' and lang_code_other != '':
    lang_codes = ' (' + lang_code_main + ', ' + lang_code_other + ')'
# Otherwise, if main code is present, its value is to be assigned as the language code
elif lang_code_main != '' and lang_code_other == '':
    lang_codes = ' (' + lang_code_main + ')'
else:
    lang_codes = ''
# If language code is present, they are to be included
if lang_codes != '':
        languages = languages + lang_codes   
print('Languages =', languages)


# To find manuscript material
# Within the 'support' element, this data can often be found within paragraph tags
# Sometimes other data (e.g., watermarks) can be included within the support element, but separated by additional <p> tags
# This will only retrieve data from within the first <p> tag found (thus excluding other undesired data)
materials = elem_to_text(soup.supportdesc.support.p)
# If not found within paragraph tags, then retrieve from parent 'support' element
if materials == '':
    materials = elem_to_text(soup.supportdesc.support)
# Sometimes periods are included in the text, which serve no purpose and should be removed
if '.' in materials:
    materials = materials.replace('.', '')
# Pre-defined abbreviated data for manuscript material may also be given as attribute of 'supportDesc' element
materials_value = get_attr('supportdesc', 'material')
# If this data is present, it is to be included in parentheses
if materials_value != '':
    materials = materials + " (" + materials_value + ")"
# This descriptive information may require translation
materials = translate_text(materials)
print('Materials =', materials)
    
# To find place of origin
places = elem_to_text(soup.origplace)
places = translate_text(places)
print('Places =', places)


# For number of columns and written lines, these are found as possible attributes within the 'layout' element
num_columns = get_attr('layout', 'columns')
print('Num_columns =', num_columns)
num_lines = get_attr('layout', 'writtenlines')
print('Num_lines =', num_lines)

        
# To find height and width measurements
height = elem_to_text(soup.height)
width = elem_to_text(soup.width)

# For height and width, unit of measurement may be found as attributes of several elements
# Only millimeters are accepted units
meas_units = (get_attr('height', 'unit') and get_attr('width', 'unit')) or get_attr('dimensions', 'unit') or get_attr('extent', 'unit')
if meas_units == 'mm':
        height = height
        print('Height =', height, 'mm')
        width = width
        print('Width =', width, 'mm')
else:
    height = ''
    width = ''


# To find manuscript binding description
binding_desc = soup.bindingdesc
if binding_desc:
    # The child element 'dimensions' contains measurements (already retrieved for 'height'/'width'), which must be removed
    if binding_desc.find('dimensions'):
        remove_dimensions = binding_desc.find('dimensions')
        remove_dimensions.extract()
binding = elem_to_text(binding_desc)
# This descriptive information may require translation
binding = translate_text(binding)
print('Manuscript_binding =', binding)

    
# To generate URL hyperlink to source record
manuscript_link = get_attr('msdesc', 'xml:id')
is_vers = manuscript_link.endswith('-is')
if is_vers:
    manuscript_link = 'http://handrit.is/manuscript/view/is/' + manuscript_link[0:-3]
    print('Manuscript_link =', manuscript_link)
en_vers = manuscript_link.endswith('-en')
if en_vers:
    manuscript_link = 'http://handrit.is/manuscript/view/en/' + manuscript_link[0:-3]
    print('Manuscript_link =', manuscript_link)
da_vers = manuscript_link.endswith('-da')
if da_vers:
    manuscript_link = 'http://handrit.is/manuscript/view/da/' + manuscript_link[0:-3]
    print('Manuscript_link =', manuscript_link)

# To find provenance agent
provenance_data = soup.acquisition or soup.provenance
if provenance_data:
    # The only desire datum from these elements is any personal name, which is tagged accordingly
    if provenance_data.find('name'):
        if get_attr('name', 'type') == 'person':
            provenance_agent = elem_to_text(provenance_data.find('name'))
        # For all other circumstances, a blank value is desired
        else:
            provenance_agent = ''
    else:
        provenance_agent = ''
else:
    provenance_agent = ''
print('Provenance =', provenance_agent)


# In[ ]:


print('IMPORT TO CSV:')

# To generate list for import into CSV file
''' This list is created to import the extracted values in appropriate order
as a new line of a CSV file for batch upload into the Schoenberg Database of Manuscripts (SDBM).
The following index positions correspond to the SDBM fields:
o = id
1 = manuscript
2 = groups
3 = source_date
4 = source_title
5 = source_catalog_or_lot_number
6 = institution
7 = sale_selling_agent
8 = sale_seller_or_holder
9 = sale_buyer
10 = sale_sold
11 = sale_ price
12 = titles
13 = authors
14 = dates
15 = artists
16 = scribes
17 = languages
18 = materials
19 = places
20 = uses
21 = folios
22 = num_columns
23 = num_lines
24 = height
25 = width
26 = alt_size
27 = miniatures_fullpage
28 = miniatures_large
29 = miniatures_small
30 = miniatures_unspec_size
31 = initials_historiated
32 = initials_decorated
33 = manuscript_binding
34 = manuscript_link
35 = other_info
36 = provenance
'''

# First we create a list and populate it with blank values
new_CSV_row = ['']
new_CSV_row = new_CSV_row * 37
# Now we replace the blank values with our data where appropriate by index number
# For indices 0-2, these fields are generated internally by SDBM; no data to import
new_CSV_row[0] = ''
new_CSV_row[1] = ''
new_CSV_row[2] = ''
# 'Source date' [3] to be set as date of batch upload to SDBM (yet to be determined) [per LR]
new_CSV_row[3] = '[TBD]'
# 'Source title' [4] to be assigned the following for all records [per LR]
new_CSV_row[4] = 'Handrit.org'
new_CSV_row[5] = source_catalog_or_lot_number
new_CSV_row[6] = institution
# Indices 7-11 are to be left blank; transaction data not available in records
new_CSV_row[7] = ''
new_CSV_row[8] = ''
new_CSV_row[9] = ''
new_CSV_row[10] = ''
# 'Sale price' [11] to be left blank; no elements/attributes in TEI encoding scheme pertain to concept
new_CSV_row[11] = ''
new_CSV_row[12] = titles
new_CSV_row[13] = authors
new_CSV_row[14] = dates
# 'Scribes'[15] to be left blank; no elements/attributes in TEI encoding scheme pertain to concept
new_CSV_row[15] = ''
# 'Artists'[16] to be left blank; no elements/attributes in TEI encoding scheme pertain to concept
new_CSV_row[16] = ''
new_CSV_row[17] = languages
new_CSV_row[18] = materials
new_CSV_row[19] = places
# 'Uses' [20] to be left blank; no elements/attributes in TEI encoding scheme pertain to concept
new_CSV_row[20] = ''
# 'Folios' [21] to be left blank; expects a single numerical value, which cannot reliably be extracted
new_CSV_row[21] = ''
new_CSV_row[22] = num_columns
new_CSV_row[23] = num_lines
new_CSV_row[24] = height
new_CSV_row[25] = width
# 'Alt size' [26] to be left blank; used for other measurements within restrited values
new_CSV_row[26] = ''
# Indices 27-32 (miniatures and intitials) are to be left blank; expects numerical values, which cannot reliably be extracted
new_CSV_row[27] = ''
new_CSV_row[28] = ''
new_CSV_row[29] = ''
new_CSV_row[30] = ''
new_CSV_row[31] = ''
new_CSV_row[32] = ''
new_CSV_row[33] = binding
new_CSV_row[34] = manuscript_link
new_CSV_row[35] = ''
new_CSV_row[36] = provenance_agent

print('New_CSV_row =', new_CSV_row)


# In[ ]:


import csv
f = open('.csv')
reader = csv.reader(f)
# Open our existing CSV file in append mode
with open('.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(new_CSV_row)
f.close()

