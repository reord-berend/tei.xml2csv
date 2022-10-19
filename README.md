# tei.xml2csv
BeautifulSoup code to extract metadata from TEI-conformant XML files and export to CSV file.

<b>Background:</b>

This project was created as part of the <a href="https://cci.drexel.edu/mrc/leading/">2022 LEADING Fellowship</a> through Drexel University's <a href="https://cci.drexel.edu/mrc/">Metadata Research Center (MRC)</a> in collaboration with the <a href="https://schoenberginstitute.org/">Schoenberg Institute of Manuscript Studies</a> at the <a href="https://www.library.upenn.edu/kislak">Kislak Center for Special Collections, Rare Books and Manuscripts (University of Pennsylvania Libraries)</a>.

<b>Goal:</b>

The goal of the project was to contribute metadata records for medieval Scandinavian manuscripts from <a href="https://handrit.is/?lang=en">Handrit.org</a>, a joint electronic catalogue of holdings from several Nordic institutions (including the <a href="https://nors.ku.dk/english/research/centres-and-groups/arnamagnaean/">Arnamagnæan Institute</a> at the University of Copenhagen, the <a href="http://landsbokasafn.is/index.php/english">National and University Library of Iceland</a>, and the <a href="https://www.arnastofnun.is/en/language">Árni Magnússon Institute for Icelandic Studies</a>), to the <a href="https://sdbm.library.upenn.edu/">Schoenberg Database of Manuscripts (SDBM)</a>, an open-access resource that aggregates observations of premodern manuscripts from around the world. 

<b>Methodology:</b>

The Handrit.org records are publically available via their <a href="https://github.com/Handrit">GitHub repository</a> as <a href="https://tei-c.org/">TEI</a>-conformant XML files. For source-to-target data mapping, these files were reviewed using <a href="https://www.oxygenxml.com/">Oxygen XML Editor</a> and the <a href="https://tei-c.org/release/doc/tei-p5-doc/en/html/MS.html">TEI P5 Guidelines for Manuscript Description</a> were studied to develop a <a href="https://github.com/reord-berend/tei.xml2csv/blob/main/SDBM%20Fields%20to%20TEI-XML%20Path%20Equivalencies%20Table.pdf">schema crosswalk</a> documenting the <a href="https://en.wikipedia.org/wiki/XPath">XPath</a> where data corresponding to the SDBM fields may be retrieved.

This was achieved in <a href="https://jupyter.org/">Jupyter Notebook</a> through the <a href="https://www.anaconda.com/">Anaconda Distribution Platform</a> using the Python library <a href="https://www.crummy.com/software/BeautifulSoup/bs4/doc/">Beautiful Soup</a>, which can parse HTML/XML and is often utilized for web scraping. In the first phase (version 1), the Beautiful Soup code was developed based on individual records. The retrieved data was assigned to variables named after the SDBM fields. Once the code worked for one file, another file was attempted, which typically required modification to account for variations. This process was continued until the data could be successfully retrieved for each of the sample files. 

In the second phase (version 2), in order to run the code on the entire Handrit.org catalogue, a Python class was created for TEI-XML files, so that every file with the appropriate extension found with a given directory will be considered an instance of that class. The former variables corresponding to each SDBM field were then made into properties of that class, so the same data would be retrieved for each file. The SDBM allows for batch upload from a CSV file. Thus, for each TEI-XML file, a list was generated with indexing positions matching the order of the SDBM column headings, which could then be written as a new row in the CSV file, thereby generating a spreadsheet.

Once the code had been run successfully on the entire catalogue, the resulting CSV file was then imported into Microsoft Excel to ensure character encoding fidelity: <a href=" https://en.wikipedia.org/wiki/UTF-8"> UTF-8</a> had to be specified throughout the process (e.g., reading and writing files) to account for the unique orthography of the North Germanic languages (namely, the letters <a href="https://en.wikipedia.org/wiki/Eth">‘eth’ <ð></a>, <a href="https://en.wikipedia.org/wiki/Thorn_(letter)">‘thorn’ <Þ></a>, and <a href="https://en.wikipedia.org/wiki/Æ"> ‘ash’ <æ></a>). This document was then imported into <a href="https://openrefine.org/">OpenRefine</a> for data pre-processing (cleaning and transformation).

The full Handrit.org catalogue was downloaded on 8/17/2022. Of the total 15,189 records, only 1,951 fell within the chronological parameters (i.e., pre-1600 CE) of the SDBM, the rest were excluded. Being of Nordic origin, many of the records were written in Icelandic or Danish, and thus needed to be translated for an English-speaking audience. The spreadsheet of pre-1600 records was imported back into Jupyter Notebook, and the Python API for Google Translate (<a href="https://pypi.org/project/google-trans-new/">google_trans_new</a>, included with the Anaconda site packages) was run on specific fields (namely: titles, dates, materials, places, and binding) using indexing notation.

<b>Funding:</b>
  
This project was supported by the Institute of Museum and Library Services (IMLS) RE-246450-OLS-20.

<b>Credits:</b>

My sincerest thanks to my mentors <a href="https://www.library.upenn.edu/detail/person/lynn-ransom">Dr. Lynn Ransom</a> (Project Director of the SDBM) and <a href="https://www.library.upenn.edu/detail/person/douglas-emery">Doug Emery</a> (Digital Content Programmer for Special Collections at UPenn, who introduced me to Beautiful Soup and helped me grow as a coder), as well as <a href="https://www.linkedin.com/in/kate-topham">Kate Topham</a> (my colleague in the LEADING Fellowship). I'm fortunate to have worked with such a wonderful team, whose guidance, encouragement, and support made this project possible.

Thanks to <a href="https://drexel.edu/cci/about/directory/G/Greenberg-Jane/">Dr. Jane Greenberg</a> (Director of the MRC), <a href="https://drexel.edu/cci/about/directory/G/Grabus-Samantha/">Sam Grabus</a> (LEADING Project Manager), and the rest of the team at Drexel University. The LEADING Fellowship has been such an amazing opportunity for me, and I'm grateful to have been a part of it.

A special mention goes to <a href="https://de.linkedin.com/in/maximilian-konzack-a94314a5">Maximilian Konzack</a> (computer scientist/software engineer), whose post on <a href="https://komax.github.io/blog/text/python/xml/parsing_tei_xml_python/">'Parsing TEI XML documents with Python'</a> provided the roadmap for this project.

Last but not least, thank you to my teacher <a href="https://www.linkedin.com/in/brian-dobreski-939b42b8">Dr. Brian Dobreski</a>, professor at the University of Tennessee, whose courses sparked my interest in metadata and started me on the path that lead me here.
