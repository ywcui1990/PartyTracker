# -*- coding: utf-8 -*-
# <nbformat>2</nbformat>

# <markdowncell>

# # Read the Pew.txt file as analyze some of the data

# <markdowncell>

# We have a Pew.txt file that was exported from the SPSS file from Paul.
# 
# See if we can parse it and visualize some of the data.

# <codecell>

import pandas as pd
pd.set_printoptions(max_columns=0)

# <markdowncell>

# Read into dataframe.

# <codecell>

#pew = pd.read_csv('Pew.txt',delimiter=' ', dtype={'fips':object})
#pew = pd.read_csv('Pew.txt',delimiter=' ', dtype={'fips':np.character})
pew = pd.read_csv('Pew.txt',delimiter=' ')

# <codecell>

pew.head(2)

# <markdowncell>

# Some basic summary statistics.

# <codecell>

pew.describe()

# <codecell>

pew.info()

# <markdowncell>

# ## Looking at each column

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

# <codecell>

pew[pew.survey=='Heat4B']

# <markdowncell>

# We could parse these *date* strings.  They look like mddyy.

# <codecell>

pew.date.value_counts()[:5]

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

# <markdowncell>

# It would be good to have dictionary for these category numbers into a file that could be joined with this Pew.txt file so we know what the values, e.g., *2*, mean.

# <codecell>

pew.hisp.value_counts()

# <codecell>

pew.race.value_counts()

# <codecell>

#pew[pew.race==1].head()

# <markdowncell>

# Why are there two *income* columns?

# <codecell>

pew.income.value_counts()

# <codecell>

pew.income2.value_counts()

# <markdowncell>

# ### Locations

# <codecell>

print pew.fips.value_counts().head()
print pew.fips.value_counts().tail()
#pew.fips.value_counts().plot()

# <codecell>

#pew[['state','fips']][pew.fips.isnull() == False].plot('state','fips')

# <codecell>

#pew[['state','fips',]][pew.fips.isnull() == False].head()

# <codecell>

#pew.info()

# <codecell>

#print pew[pew.fips.isnull() == False].fips.head()
#pew[pew.fips.isnull() == False].fips[122824]
#type(pew[pew.fips.notnull()].fips[122824])

# <markdowncell>

# Why is the *fips* column loading as a float?

# <codecell>

#pew['fips'] = pew.fips.astype(np.character)

# <codecell>

#pew.fips.tail(1)

# <codecell>

#'oops'.rjust(40,'0')

# <codecell>

#pew['FIPS_6-4'] = pew.fips.apply(lambda fips: "%05d"%int(fips))
#pew['FIPS_6-4'] = pew.fips.apply(lambda code: str(code).rjust(5,'0') if type(code)==str else NaN)
#pew.head()

# <codecell>

#pew.info()

# <markdowncell>

# *state* is present whenever *fips* is present.  So, just get the county from *fips* whenever it is available.

# <codecell>

print 'state but not fips:', len(pew[pew.state.notnull() & pew.fips.isnull()])
print 'fips but not state:', len(pew[pew.state.isnull() & pew.fips.notnull()])

# <markdowncell>

# Get the FIPS county code from the 5-digit FIPS 6-4 code.

# <codecell>

pew['fips_county'] = pew.fips.apply(lambda code: code%1000 if code != NaN else NaN)
pew[['state','fips','fips_county']][pew.fips_county.notnull()].sort('fips').tail(2)

# <markdowncell>

# ####FIPS

# <markdowncell>

# A separate file with FIPS codes.  Use it to get state and county names.

# <codecell>

!head -n 2 data/US_FIPS_Codes.csv
fips = pd.read_csv('data/US_FIPS_Codes.csv')
fips.head(2)

# <codecell>

fips.info()

# <codecell>

#fips['FIPS_6-4'] = fips.apply(lambda row: "%02d%03d"%(row['FIPS State'],row['FIPS County']), axis=1)
#fips.head()

# <markdowncell>

# Get the state names.

# <codecell>

fips_states = fips[['State','FIPS State']].drop_duplicates()
fips_states.head(2)

# <codecell>

pew2 = pew.merge(fips_states, how='left', left_on='state', right_on='FIPS State')
pew2['state_name'] = pew2.State
pew2[pew2.fips.notnull()].sort('fips').head(2)

# <markdowncell>

# Get the county names.

# <codecell>

pew3 = pew2.merge(fips, how='left', left_on=['state','fips_county'], right_on=['FIPS State','FIPS County'])
pew3[['state','fips','fips_county','state_name','County Name']][pew3.fips.notnull()].sort('fips').tail(5)
#pew3[pew3.fips.notnull()].tail(5)

# <codecell>

pew3.head()

# <markdowncell>

# ### ????

# <codecell>

pew.usr.value_counts()

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

# <codecell>

pew[pew.regvoter.isnull()].year.hist(bins=20)

# <codecell>

pew[pew.regvoter.isnull() == False].year.hist(bins=20)

# <codecell>

pew3[pew3['County Name'].notnull()].head()

# <markdowncell>

# Clean up.

# <codecell>

#pew3['FIPS_6-4'] = pew.apply(lambda row: "%02f%03f"%(row['state'],row['fips_county']) if ((row['state']!=NaN) and (row['fips_county']!=NaN)) else NaN,axis=1)

# <codecell>

pew4 = pew3.copy()
del pew4['fips']
#del pew4['state']
#del pew4['fips_county']
del pew4['State_x']
del pew4['FIPS State_x']
del pew4['FIPS State_y']
del pew4['State_y']
del pew4['FIPS County']
pew4 = pew4.rename(columns={'County Name':'county_name',
                            'fips_county':'fipsco',
                            'state':'fipsst'})
pew4[pew4.county_name.notnull()].head()

# <markdowncell>

# ## Codebook 

# <markdowncell>

# Take a copy of the codes and meanings in CSV form drawn from the Merge Codebook PDF file, and merge its information with the pew data so we can see what the meanings of the values.

# <codecell>

codes = pd.read_csv('data/Merge_Codebook.csv').groupby('column')
codes.head(2)

# <codecell>

code_columns = dict(list(codes))
print code_columns['party'].dtypes
code_columns['party'].head()

# <markdowncell>

# #### Debugging

# <codecell>

column,df_orig = code_columns.items()[1]
df = df_orig.copy()
print column
del df['column']
df = df.rename(columns={'code':column})
print df.dtypes
df

# <codecell>

pew5 = pew4.copy()
pew5 = pew5[['id','rid',column]]
pt = pew5[pew5[column].notnull()][-5:]
#pt[column] = pt[column].astype(object)
pt[column] = pt[column].astype(np.character)
print pt.dtypes
pt

# <codecell>

pt.merge(df, how='left')

# <codecell>

#df = pd.DataFrame({'partyln':['0','1','2','9'], 'meaning':['m0','m1','m2','m9']})
#df

# <markdowncell>

# #### Do the merge.

# <codecell>

pew5 = pew4.copy().sort('id')
for column,df_orig in code_columns.items():
    #pew5 = pew4.copy().sort('id')
    #pew5 = pew5[['id','rid',column]]
    
    #pew5 = pew5[pew5[column].notnull()][-5:]
    
    df = df_orig.copy()
    print "#"*40
    print column
    del df['column']
    df2 = df.rename(columns={'code':column})
    print df2
    print df2.dtypes
    
    #print "#"*20
    #pew5 = pew5.merge(df,how='left', left_on=column, right_on='code')
    #print pew5[column].dtype
    #print pew5[pew5[column].notnull()].tail()
    
    #print "#"*20
    #pew5[column] = pew5[column].astype(object)
    pew5[column] = pew5[column].astype(np.character)
    #print pew5[column].dtype
    #print pew5[pew5[column].notnull()].tail()
    
    print "#"*20
    #pew5 = pew5.merge(df2,how='left',on=column)
    pew5 = pew5.merge(df2,how='left')
    del pew5[column]
    #pew5 = pew5.rename(columns={'meaning':column+'_new'})
    pew5 = pew5.rename(columns={'meaning':column})
    
    pew5 = pew5.sort('id')
    print pew5[pew5[column].notnull()].tail()
    

# <codecell>

pew5.tail(100)

# <codecell>


