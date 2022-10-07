#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Import Beautiful Soup library
from bs4 import BeautifulSoup


# In[ ]:


def read_tei(tei_file):
    """Function to open a TEI-XML document and read with lxml parser
    """
    with open(tei_file, 'r', encoding="utf8") as tei:
        soup = BeautifulSoup(tei, 'lxml')
        return soup
    raise RuntimeError('Cannot generate a soup from the input')


# In[ ]:


class TEIFile(object):
    def __init__(self, filename):
        self.filename = filename
        self.soup = read_tei(filename)
        self._source_catalog_or_lot_number = ''
        self._institution = ''
        self._titles = ''
        self._authors = ''
        self._dates = ''
        self._languages = ''
        self._materials = ''
        self._places = ''
        self._num_columns = ''
        self._num_lines = ''
        self._height = ''
        self._width = ''
        self._binding = ''
        self._manuscript_link = ''
        self._provenance =''
        
    # Import regular expressions module
    import re    
    # Text in certain fields is sometimes separated by superfluous whitespace, which must be removed
    # Whitespace typically consists of new lines, tabs, or repeated spaces
    # To ensure that normal spacing is maintained between words, all whitespace characters are replaced with a single space
    def clean_string(self, string):
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
        new_string = self.re.sub('\s+', ' ', string)
        # Now remove any leading or trailing whitespace characters
        new_string = new_string.strip()
        return new_string
    
    # Elements might exist in some records but not others
    # If we reference an element that does not exist, BeautifulSoup will yield an AttributeError 
    # This can be bypassed by defining a function which retrieves the text only if the tag exists
    def elem_to_text(self, elem, default=''):
        """ Function to retrieve text only if tag exists. """
        # To pass the argument, use soup.elem
        # e.g., element_to_text(soup.title)
        if elem:
            # Call clean_string function to remove superfluous whitespace
            return self.clean_string(elem.getText())
        else:
            return default
    
    # Some elements have attributes which might exist in some records but not others
    def get_attr(self, tag, attr, default=''):
        """Function to return the attribute value if present 
        or return 'default'.
        """
        # First we check if the element exists
        tag = self.soup.find(tag)
        if tag:
        # Next we check if the element has the desired attribute
            if tag.has_attr(attr):
                return tag[attr]
            else:
                return default
        else:
            return default
    
    # Import python API for google translate
    # Google_trans_new package already included in Anaconda, no install necessary
    # Documentation can be found at https://github.com/lushan88a/google_trans_new
    # Further documentation at https://pypi.org/project/google-trans-new/
    """ Would not run on 8/17/22, received error message: "JSONDecodeError: Extra data: line 1 column 343 (char 342)"
    in file== anaconda3\lib\site-packages\google_trans_new\google_trans_new.py, 
    line 151 was changed from: 
    response = (decoded_line + ']')
    to:
    response = (decoded_line + '')
    """
    from google_trans_new import google_translator
    translator = google_translator()  

    def translate_text(self, string):
        # To determine source language 
        lang_code = self.get_attr('msdesc', 'xml:lang')
        # The 3 posibilities are Icelandic, Danish, and English
        if lang_code == 'is':
            translated_text = self.translator.translate(string, lang_src='is', lang_tgt='en') 
            return translated_text
        if lang_code == 'da':
            translated_text = self.translator.translate(string, lang_src='da', lang_tgt='en') 
            return translated_text
        if lang_code == 'en':
            return string
    
    @property
    # Find source catalogue number
    def source_catalog_or_lot_number(self):
        source_catalog_or_lot_number = self.soup.idno
        source_catalog_or_lot_number = self.elem_to_text(source_catalog_or_lot_number)
        self._source_catalog_or_lot_number = source_catalog_or_lot_number
        return self._source_catalog_or_lot_number
    
    @property
    # Find source institution data (pulling values from two different elements)
    def institution(self):
        find_repository = self.soup.repository
        find_repository = self.elem_to_text(find_repository)
        find_institution = self.soup.institution
        find_institution = self.elem_to_text(find_institution)
        # Sometimes these data are only given in abbreviated form as an attribute
        # If the aforementioned fields are blank, then we must search for these attributes
        if find_repository == '':
            find_repository = self.get_attr('repository', 'key')
        if find_institution == '':
            find_institution = self.get_attr('institution', 'key')
        # Finally, we combine the two values 
        institution = find_repository + ', ' + find_institution
        self._institution = institution
        return self._institution
    
    @property
    # To find manuscript title
    def titles(self):
        titles = self.soup.mscontents.title
        titles = self.elem_to_text(titles)
        self._titles = titles
        return self._titles
    
    @property
    # To find manuscript author
    def authors(self):
        authors = self.soup.author
        authors = self.elem_to_text(authors)
        self._authors = authors
        return self._authors
    
    @property
    # To find manuscript dates
    def dates(self):
        find_dates = self.soup.origdate
        find_dates = self.elem_to_text(find_dates)
        # Dates may also be given as attributes of this element
        dates_start_range = self.get_attr('origdate', 'notbefore')
        # While 'notBefore' is the most common attribute, this can also be given as 'from'
        if dates_start_range == '':
            dates_start_range = self.get_attr('origdate', 'from')
            # Rarely, this can be given as 'when'
            if dates_start_range == '':
                dates_start_range = self.get_attr('origdate', 'when')
        dates_end_range = self.get_attr('origdate', 'notafter')
        # While 'notAfter' is the most common attribute, this can also be given as 'to'
        if dates_start_range == '':
            dates_start_range = self.get_attr('origdate', 'to')
        # Date range, if these values exist, are to be combined and included in parentheses
        if dates_start_range != '' and dates_end_range != '':
            dates_range = '(' + dates_start_range + '-' + dates_end_range + ')'
            dates = find_dates + ' ' + dates_range
        else:
            dates = find_dates
        self._dates = dates
        return self._dates
        # Sometimes (albeit rarely) the date is not given in 'origDate' element, but simply as attributes of 'origin'
        if find_dates == '':
            dates_start = self.get_attr('orig', 'when')
            if dates_start == '':
                dates_start = self.get_attr('orig', 'from')
        dates_end = self.get_attr('orig', 'to')
        if dates_start != '' and dates_end != '':
            dates = dates_start + '-' + dates_end
            self._dates = dates
        return self._dates 
    
    @property
    # To find manuscript language
    def languages(self):
        languages = self.soup.textlang
        languages = self.elem_to_text(languages)
        languages = self.translate_text(languages)
        # Languages may also be given as two-letter codes, differentiated by 'main' and 'other'
        lang_code_main = self.get_attr('textlang', 'mainlang')
        lang_code_other = self.get_attr('textlang', 'otherlangs')
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
        self._languages = languages
        return self._languages
    
    @property
    # To find manuscript material
    def materials(self):
        # Within the 'support' element, this data can often be found within paragraph tags
        # Sometimes other data (e.g., watermarks) can be included within <support>, but separated by additional <p> tags
        # The following will only retrieve data from within the first <p> tag found (thus excluding other undesired data)
        materials = self.soup.supportdesc.support.p
        materials = self.elem_to_text(materials)
        # If not found within paragraph tags, then retrieve from parent 'support' element
        if materials == '':
            materials = self.soup.supportdesc.support
            materials = self.elem_to_text(materials)
        # Sometimes periods are included in the text, which serve no purpose and should be removed
        if '.' in materials:
            materials = materials.replace('.', '')
        # Pre-defined abbreviated data for manuscript material may also be given as attribute of 'supportDesc' element
        materials_value = self.get_attr('supportdesc', 'material')
        # If this data is present, it is to be included in parentheses
        if materials_value != '':
            materials = materials + " (" + materials_value + ")"
        # This descriptive information may require translation
        materials = self.translate_text(materials)
        self._materials = materials
        return self._materials
    
    @property
    # To find place of origin
    def places(self):
        places = self.soup.origplace
        places = self.elem_to_text(places)
        places = self.translate_text(places)
        self._places = places
        return self._places
    
    @property
    # For number of columns, this is found as possible attribute within the 'layout' element
    def num_columns(self):
        num_columns = self.get_attr('layout', 'columns')
        self._num_columns = num_columns
        return self._num_columns
        
    @property
    # For number of lines, this is found as possible attribute within the 'layout' element
    def num_lines(self):
        num_lines = self.get_attr('layout', 'writtenlines')
        self._num_lines = num_lines
        return self._num_lines
    
    @property
    # To find height measurements
    def height(self):
        height = self.soup.height
        height = self.elem_to_text(height)
        # The unit of measurement may be found as attributes of several elements
        meas_units = self.get_attr('height', 'unit') or self.get_attr('dimensions', 'unit') or self.get_attr('extent', 'unit')
        # Only millimeters are accepted units
        if meas_units == 'mm':
            height = height
        else:
            height = ''
        self._height = height
        return self._height
    
    @property
    # To find width measurements
    def width(self):
        width = self.soup.width
        width = self.elem_to_text(width)
        # The unit of measurement may be found as attributes of several elements
        meas_units = self.get_attr('width', 'unit') or self.get_attr('dimensions', 'unit') or self.get_attr('extent', 'unit')
        # Only millimeters are accepted units
        if meas_units == 'mm':
            width = width
        else:
            width = ''
        self._width = width
        return self._width
    
    @property
    def binding(self):
        binding_desc = self.soup.bindingdesc
        if binding_desc:
        # The child element 'dimensions' contains measurements (already retrieved for 'height'/'width'), which must be removed
            if binding_desc.find('dimensions'):
                remove_dimensions = binding_desc.find('dimensions')
                remove_dimensions.extract()
        binding = self.elem_to_text(binding_desc)
        # This descriptive information may require translation
        binding = self.translate_text(binding)
        self._binding = binding
        return self._binding

    @property
    # To generate URL hyperlink to source record
    def manuscript_link(self):
        manuscript_link = self.get_attr('msdesc', 'xml:id')
        # Records are in 3 possible languages: Icelandic, English, and Danish
        # The language code at the end of the identifier must be made into a sub-folder of the URL, then removed
        is_vers = manuscript_link.endswith('-is')
        if is_vers:
            manuscript_link = 'http://handrit.is/manuscript/view/is/' + manuscript_link[0:-3]
        en_vers = manuscript_link.endswith('-en')
        if en_vers:
            manuscript_link = 'http://handrit.is/manuscript/view/en/' + manuscript_link[0:-3]
        da_vers = manuscript_link.endswith('-da')
        if da_vers:
            manuscript_link = 'http://handrit.is/manuscript/view/da/' + manuscript_link[0:-3]
        self._manuscript_link = manuscript_link
        return self._manuscript_link
    
    @property
    # To find provenance agent
    def provenance(self):
        provenance_data = self.soup.acquisition or self.soup.provenance
        if provenance_data:
            # The only desired datum from these elements is any personal name, which is tagged accordingly
            if provenance_data.find('name'):
                if self.get_attr('name', 'type') == 'person':
                    provenance_agent = provenance_data.find('name')
                    provenance_agent = self.elem_to_text(provenance_agent)
                # For all other circumstances, a blank value is desired
                else:
                    provenance_agent = ''
            else:
                provenance_agent = ''
        else:
            provenance_agent = ''
        self._provenance = provenance_agent
        return self._provenance


# In[ ]:


# To generate list for import into CSV file
def tei_to_csv_entry(tei_file):
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
    tei = TEIFile(tei_file)
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
    new_CSV_row[5] = tei.source_catalog_or_lot_number
    new_CSV_row[6] = tei.institution
    # Indices 7-11 are to be left blank; transaction data not available in records
    new_CSV_row[7] = ''
    new_CSV_row[8] = ''
    new_CSV_row[9] = ''
    new_CSV_row[10] = ''
    # 'Sale price' [11] to be left blank; no elements/attributes in TEI encoding scheme pertain to concept
    new_CSV_row[11] = ''
    new_CSV_row[12] = tei.titles
    new_CSV_row[13] = tei.authors
    new_CSV_row[14] = tei.dates
    # 'Scribes'[15] to be left blank; no elements/attributes in TEI encoding scheme pertain to concept
    new_CSV_row[15] = ''
    # 'Artists'[16] to be left blank; no elements/attributes in TEI encoding scheme pertain to concept
    new_CSV_row[16] = ''
    new_CSV_row[17] = tei.languages
    new_CSV_row[18] = tei.materials
    new_CSV_row[19] = tei.places
    # 'Uses' [20] to be left blank; no elements/attributes in TEI encoding scheme pertain to concept
    new_CSV_row[20] = ''
    # 'Folios' [21] to be left blank; expects a single numerical value, which cannot reliably be extracted
    new_CSV_row[21] = ''
    new_CSV_row[22] = tei.num_columns
    new_CSV_row[23] = tei.num_lines
    new_CSV_row[24] = tei.height
    new_CSV_row[25] = tei.width
    # 'Alt size' [26] to be left blank; used for other measurements within restrited values
    new_CSV_row[26] = ''
    # Indices 27-32 (miniatures and intitials) are to be left blank; expects numerical values, which cannot reliably be extracted
    new_CSV_row[27] = ''
    new_CSV_row[28] = ''
    new_CSV_row[29] = ''
    new_CSV_row[30] = ''
    new_CSV_row[31] = ''
    new_CSV_row[32] = ''
    new_CSV_row[33] = tei.binding
    new_CSV_row[34] = tei.manuscript_link
    new_CSV_row[35] = ''
    new_CSV_row[36] = tei.provenance

    return new_CSV_row


# In[ ]:


# To select all TEI-XML documents
import pathlib
from pathlib import Path

file_path = Path.home()/'*.xml'
file_path = str(file_path)
print(file_path)


# In[ ]:


import glob
files = glob.glob(file_path, recursive=True)
for tei_file in files:
    new_entries = tei_to_csv_entry(tei_file)
    for entry in new_entries:
        write_new_CSV_entry(entry)


# In[ ]:


import csv
def write_new_CSV_entry(new_CSV_row):
    f = open('.csv')
    reader = csv.reader(f)
    # Open our existing CSV file in append mode
    with open('.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(new_CSV_row)

