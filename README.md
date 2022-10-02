# tei.xml2csv
BeautifulSoup code to extract metadata from TEI-conformant XML files and export to CSV file.

<b>Background:</b>
This project was created as part of the <a href="https://cci.drexel.edu/mrc/leading/">2022 LEADING Fellowship</a> through Drexel University's <a href="https://cci.drexel.edu/mrc/">Metadata Research Center (MRC)</a> in collaboration with the <a href="https://schoenberginstitute.org/">Schoenberg Institute of Manuscript Studies</a> at the <a href="https://www.library.upenn.edu/kislak">Kislak Center for Special Collections, University of Pennsylvania Libraries</a>.

<b>Goal:</b>
The goal of the project was to contribute metadata records for medieval Scandinavian manuscripts from <a href="https://handrit.is/?lang=en">Handrit.is</a>, a joint electronic catalogue of holdings from several academic and national institutions in Iceland, Denmark, and Sweden, to the <a href="https://sdbm.library.upenn.edu/">Schoenberg Database of Manuscripts (SDBM)</a>, an open-access resource that aggregates observations of premodern manuscripts from around the world. 

<b>Methodology:</b>
The Handrit.is records are publically available via <a href="https://github.com/Handrit">GitHub</a> as <a href=" https://tei-c.org/">TEI</a>-conformant XML files. For source-to-target data mapping, these files were reviewed using <a href=" https://www.oxygenxml.com/">Oxygen XML Editor</a> and the <a href=" https://tei-c.org/release/doc/tei-p5-doc/en/html/MS.html ">TEI P5 Guidelines for Manuscript Description</a> were studied in order to develop a schema crosswalk documenting the <a href="https://en.wikipedia.org/wiki/XPath">XPath</a> whence data corresponding to the SDBM fields may be retrieved.

This was achieved in <a href="https://jupyter.org/">Jupyter Notebook</a> through the <a href="https://www.anaconda.com/">Anaconda Distribution Platform</a> using the Python library <a href="https://www.crummy.com/software/BeautifulSoup/bs4/doc/">Beautiful Soup</a>, which can parse HTML/XML and is often utilized for web scraping. A class was created for TEI-XML files, with properties corresponding to each applicable SDBM field. The SDBM allows for batch upload from a CSV file. Thus, for each instance object, a list was generated with indexing positions matching the order of the SDBM column headings, which would represent a new row in the CSV file.

<b>Credits:</b>

First and foremost, my most sincere thanks and gratitude to my mentors <a href="https://www.library.upenn.edu/detail/person/lynn-ransom">Dr. Lynn Ransom</a>, Project Director of the SDBM, and <a href="https://www.library.upenn.edu/detail/person/douglas-emery">Doug Emery</a>, Digital Content Programmer for Special Collections at UPenn, for their guidance and support throughout this process.

The computer scientist/software engineer <a href="https://de.linkedin.com/in/maximilian-konzack-a94314a5">Maximilian Konzack</a>, whose post on <a href="https://komax.github.io/blog/text/python/xml/parsing_tei_xml_python/">'Parsing TEI XML documents with Python'</a> paved the way for this project.

Finally, my teacher <a href="https://www.linkedin.com/in/brian-dobreski-939b42b8">Dr. Brian Dobreski</a>, professor at University of Tennessee, whose courses on metadata and Knowledge Organization Systems put me on this path.
