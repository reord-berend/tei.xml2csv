#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import csv
with open('.csv', 'r', encoding='utf8') as csvfile:
    reader = csv.reader(csvfile)
    new_list = []
    for row in reader:
        new_list.append(row)


# In[ ]:


from google_trans_new import google_translator
translator = google_translator()


# In[ ]:


for row in new_list[1:300]:
    titles = translator.translate(row[12])
    row[12] = titles
    dates = translator.translate(row[14])
    row[14] = dates
    materials = translator.translate(row[18])
    row[18] = materials
    places = translator.translate(row[19])
    row[19] = places
    manuscript_binding = translator.translate(row[33])
    row[33] = manuscript_binding


# In[ ]:


for row in new_list[300:600]:
    titles = translator.translate(row[12])
    row[12] = titles
    dates = translator.translate(row[14])
    row[14] = dates
    materials = translator.translate(row[18])
    row[18] = materials
    places = translator.translate(row[19])
    row[19] = places
    manuscript_binding = translator.translate(row[33])
    row[33] = manuscript_binding


# In[ ]:


for row in new_list[600:900]:
    titles = translator.translate(row[12])
    row[12] = titles
    dates = translator.translate(row[14])
    row[14] = dates
    materials = translator.translate(row[18])
    row[18] = materials
    places = translator.translate(row[19])
    row[19] = places
    manuscript_binding = translator.translate(row[33])
    row[33] = manuscript_binding


# In[ ]:


for row in new_list[900:1200]:
    titles = translator.translate(row[12])
    row[12] = titles
    dates = translator.translate(row[14])
    row[14] = dates
    materials = translator.translate(row[18])
    row[18] = materials
    places = translator.translate(row[19])
    row[19] = places
    manuscript_binding = translator.translate(row[33])
    row[33] = manuscript_binding


# In[ ]:


for row in new_list[1200:1500]:
    titles = translator.translate(row[12])
    row[12] = titles
    dates = translator.translate(row[14])
    row[14] = dates
    materials = translator.translate(row[18])
    row[18] = materials
    places = translator.translate(row[19])
    row[19] = places
    manuscript_binding = translator.translate(row[33])
    row[33] = manuscript_binding


# In[ ]:


for row in new_list[1500:1800]:
    titles = translator.translate(row[12])
    row[12] = titles
    dates = translator.translate(row[14])
    row[14] = dates
    materials = translator.translate(row[18])
    row[18] = materials
    places = translator.translate(row[19])
    row[19] = places
    manuscript_binding = translator.translate(row[33])
    row[33] = manuscript_binding


# In[ ]:


for row in new_list[1800:1951]:
    titles = translator.translate(row[12])
    row[12] = titles
    dates = translator.translate(row[14])
    row[14] = dates
    materials = translator.translate(row[18])
    row[18] = materials
    places = translator.translate(row[19])
    row[19] = places
    manuscript_binding = translator.translate(row[33])
    row[33] = manuscript_binding


# In[ ]:


with open('', 'w', encoding='utf8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(new_list)

