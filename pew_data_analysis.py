# Prepare a version the data from Pew for analysis

from pylab import *
import pandas as pd
#pd.set_printoptions(max_columns=0)

def read_pew_txt(pew_txt, codebook_csv, fips_csv):
    """
    Read the Pew.txt file and return a version for simple analysis.

    pew_txt: path to Pew.txt file
    codebook_csv: path to Merge_Codebook.csv file
    fips_csv: path to US_FIPS_Codes.csv file

    example: read('Pew.txt','data/Merge_Codebook.csv','data/US_FIPS_Codes.csv')
    """

    # Read into dataframe.

    pew = pd.read_csv(pew_txt,delimiter=' ')

    pew['fips_county'] = pew.fips.apply(lambda code: code%1000 if code != NaN else NaN)
    pew[['state','fips','fips_county']][pew.fips_county.notnull()].sort('fips').tail(2)

    # A separate file with FIPS codes.  Use it to get state and county names.

    fips = pd.read_csv(fips_csv)

    # Get the state names.

    fips_states = fips[['State','FIPS State']].drop_duplicates()

    pew2 = pew.merge(fips_states, how='left', left_on='state', right_on='FIPS State')
    pew2['state_name'] = pew2.State

    # Get the county names.

    pew3 = pew2.merge(fips, how='left', left_on=['state','fips_county'], right_on=['FIPS State','FIPS County'])
    pew3[['state','fips','fips_county','state_name','County Name']][pew3.fips.notnull()].sort('fips').tail(5)

    # Clean up.

    pew4 = pew3.copy()
    del pew4['fips']
    del pew4['State_x']
    del pew4['FIPS State_x']
    del pew4['FIPS State_y']
    del pew4['State_y']
    del pew4['FIPS County']
    pew4 = pew4.rename(columns={'County Name':'county_name',
                                'fips_county':'fipsco',
                                'state':'fipsst'})

    # ## Codebook 

    # Take a copy of the codes and meanings in CSV form drawn from the Merge Codebook PDF file, 
    #and merge its information with the pew data so we can see what the meanings of the values.

    codes = pd.read_csv(codebook_csv).groupby('column')
    code_columns = dict(list(codes))

    # #### Do the merge.

    pew5 = pew4.copy().sort('id')
    for column,df_orig in code_columns.items():
        
        df = df_orig.copy()
        #print "#"*40
        #print column
        del df['column']
        df2 = df.rename(columns={'code':column})
        #print df2
        #print df2.dtypes
        
        pew5[column] = pew5[column].astype(np.character)
        
        #print "#"*20
        pew5 = pew5.merge(df2,how='left')
        del pew5[column]
        pew5 = pew5.rename(columns={'meaning':column})
        
        pew5 = pew5.sort('id')
        #print pew5[pew5[column].notnull()].tail()

    pew6 = pew5[[
            'id',
            'rid',
            'weight',
            'year',
            'date',
            'survey',
            'language',
            'age',
            'age2',
            'sex',
            'race',
            'racethn',
            'hisp',
            'income',
            'income2',
            'educ',
            'fipsst',
            'state_name',
            'fipsco',
            'county_name',
            'usr',
            'density',
            'partyln',
            'party',
            'partysum',
            'regvoter'
            ]]    

    return pew6
