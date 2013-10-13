# -*- coding: utf-8 -*-
# <nbformat>2</nbformat>

# <markdowncell>

# # Analyze the Pew.txt file

# <markdowncell>

# This time using separate function to read in the file.

# <codecell>

import pandas as pd
%load_ext autoreload
%autoreload 2
from pew_data_analysis import *
pd.set_printoptions(max_columns=0)

# <codecell>

%time pew = read_pew_txt('Pew.txt','data/Merge_Codebook.csv','data/US_FIPS_Codes.csv')

# <codecell>

pew.describe()

# <codecell>

pew.head(2)

# <markdowncell>

# ## Analyze each column

# <markdowncell>

# ### Dates

# <codecell>

pew.year.hist()

# <markdowncell>

# There are lots of surveys!

# <codecell>

print len(pew.survey.value_counts())
print pew.survey.value_counts().head(2)
print pew.survey.value_counts().tail(2)

# <markdowncell>

# We could parse these *date* strings.  They look like mddyy.

# <codecell>

pew.date.value_counts()[:5]

# <codecell>

#pew['date_new'] = pew.date.apply(lambda d: 

# <markdowncell>

# ### Demographics

# <codecell>

pew.language.value_counts()

# <markdowncell>

# These ages seem strange.

# <codecell>

pew.age.value_counts()[:5]

# <markdowncell>

# There are spikes at regular intervals, e.g., 45 and 50, and at ages with special significance, e.g. 18.  Perhaps some surveys were done on people with specific ages, or the people or the poll data collector was rounding down (or up).

# <codecell>

pew.age.hist(bins=100)

# <codecell>

pew.age2.value_counts()

# <codecell>

pew.sex.value_counts()

# <markdowncell>

# Females are *more* likely to answer DK\Refused.

# <codecell>

pew[pew.age2 == 'DK\Refused'].sex.value_counts()

# <codecell>

pew.racethn.value_counts()

# <codecell>

pew.hisp.value_counts()

# <codecell>

pew.race.value_counts()

# <markdowncell>

# Why are there two *income* columns?

# <codecell>

pew.income.value_counts()

# <codecell>

pew.income2.value_counts()

# <codecell>

pew.educ.value_counts()

# <codecell>

pew.head(2)

# <markdowncell>

# ### Locations

# <markdowncell>

# States, then counties, with most and least responses.

# <codecell>

print pew.state_name.value_counts()[:3]
print pew.state_name.value_counts()[-3:]

# <codecell>

print pew.county_name.value_counts()[:3]
print pew.county_name.value_counts()[-3:]

# <markdowncell>

# Mostly suburbanites.

# <codecell>

pew.usr.value_counts()

# <markdowncell>

# According to the Merge Codebook document, the scale goes from lowest population densith (1) to greatest (5).  Not sure what a *9* indicates; no data?

# <codecell>

pew.density.value_counts()

# <markdowncell>

# ### Politics

# <codecell>

pew.party.value_counts()

# <codecell>

pew.partyln.value_counts()

# <markdowncell>

# Fairly well balanced between those leaning Dem and those leaning Rep.

# <codecell>

pew.partysum.value_counts()

# <markdowncell>

# All are registered voters?

# <codecell>

pew.regvoter.value_counts()

# <codecell>

print len(pew.regvoter)
print len(pew[pew.regvoter.isnull()])

# <markdowncell>

# The number of responses with *regvoter* seems to be increasing over the years compared to the number with *regvoter* missing.

# <codecell>

pew[pew.regvoter.isnull()].year.hist(bins=20)

# <codecell>

pew[pew.regvoter.notnull()].year.hist(bins=20)

# <markdowncell>

# ## Write to CSV

# <codecell>

%time pew.to_csv('data/Pew_for_analysis.csv', index=False)

# <codecell>


