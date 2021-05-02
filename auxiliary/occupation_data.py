"""
Individual questionaire on occupation from 1984 to 2018
"""
import numpy as np
import pandas as pd

def load_pgen():
    #load data
    pgen = pd.read_csv('data\pgen.csv', usecols=['pid',
                                                 'cid',
                                                 'syear',
                                                 'pgstib',
                                                 'pgisco88',
                                                 'pgisco08',
                                                 'pgemplst',
                                                 'pglfs',
                                                 'pgjobch',
                                                 'pgbilzeit',
                                                 'pgbilztev',
                                                 'pgexpft',
                                                 "pgexpue",
                                                 ]
                       )
     #rename the columns
    pgen = pgen.rename(columns={"pgstib": "occupation",
                            "pgemplst": "employment_status",
                            "pgjobch": "occupational_change",
                            'pgisco88': "isco88",
                            "pgisco08": "isco08",
                           "pgexpue": "unemployment_experience",
                           "pgbilzeit": "years_education",
                           "pgbilztev": "change_in_education",
                           'pgexpft':"full_time_experience",
                           "pglfs" : "labor_force_stt"
                           }
                        )

    return pgen

def merge_ppathl_paren(pgen):
    
    ppathl =  pd.read_csv("data\ppathl.csv", usecols=['pid',
                                                      'syear',
                                                      'gebjahr',
                                                      'sex',
                                                      'immiyear',
                                                      'germborn',
                                                      'migback',
                                                      'sampreg',
                                                      "birthregion",
                                                      "loc1989",
                                                      ]
                          )
    bioparen = pd.read_csv("data/bioparen.csv", usecols=['pid',
                                                         'morigin',
                                                         'forigin',
                                                         "fisco88",
                                                         "misco88",
                                                         "freli",
                                                         "mreli"
                                                         ]
                           )
    """
    'fsedu',
                                                         'msedu',
                                                         'fprofstat',
                                                         'mprofstat',
                                                         'fprofedu',
                                                         'mprofedu'
                                                         """
    _df = pd.merge(ppathl,pgen,
                   on = ['pid','syear'],
                   how ='inner'
                   )
    data = pd.merge(_df, bioparen,
                   on = 'pid',
                   how ='inner'
                   )
    #create info of individual age at survey year
    data['bioage'] = data['syear'] - data['gebjahr']
    
    return data
def generation_effect(df):
    #df['gen3'] = np.where(df['gebjahr']<1964,'baby_boomer',np.where(df['gebjahr']<80,'gen_X','millinials'))
    df['baby_boomer'] = np.where(df['gebjahr']<1964,1,0)
    df['gen_X'] = np.where(df['gebjahr'].between(1965,1973,inclusive = True),1,0)
    df['millennials'] = np.where(df['gebjahr'].between(1974,1988,inclusive = True),1,0)

    return df

def occupation_position(pgen):
    """
    Re-classify occupation on pgstib 'occupation'
    """
    pgen.drop(pgen[pgen['occupation'] == 13].index,inplace=True) #drop retirement
    
    pgen['blue_collar'] = np.where(pgen['occupation'].between(210,330,inclusive = True),1,0)
    pgen['white_collar'] = np.where(pgen['occupation'].isin([340,510,520,521,522,530,540,550]),1,0)
    pgen['military'] = np.where(pgen['occupation']==15,1,0)
    pgen['civil_servant'] = np.where(pgen['occupation'].between(610,660 , inclusive = True),1,0)
    pgen['self_employment'] = np.where(pgen['occupation'].between(410,440, inclusive = True),1,0)
    pgen['unemployed'] = np.where(pgen['occupation'].isin([10,12]),1,0)
    pgen['schooling'] = np.where(pgen['occupation']==11,1,0)
    pgen['apprentice'] = np.where(pgen['occupation'].between(110,150, inclusive = True),1,0)

    conditions = [pgen['occupation'].between(210,330,inclusive = True),
                  pgen['occupation'].isin([340,510,520,521,522,530,540,550]),
                  pgen['occupation']==15,
                  pgen['occupation'].between(410,440,inclusive = True),
                  pgen['occupation'].between(610,660 ,inclusive = True),
                  pgen['occupation']==11,
                  pgen['occupation'].between(110,150, inclusive = True),
                  pgen['occupation'].isin([10,12])
             ]
    choices  = ['blue_collar', 'white_collar','military','self_employment','civil_servant', 'training_schooling','training_schooling','unemployed']
    pgen['occ_choices'] =  np.select(conditions,choices, default=np.nan)

    return pgen

def poccupation_isco88(pgen):
    """
     Classify occupational choice based on four-digit isco88 code only
     """
    conditions = [pgen['isco88'].between(1000,2999, inclusive = True),
    pgen['isco88'].between(3000,3999,inclusive = True),
    pgen['isco88'].between(4000,5999,inclusive = True),
    pgen['isco88'].between(6000,8999,inclusive = True),
    pgen['isco88'].between(9000,9999 ,inclusive = True),
    pgen['isco88']== 100
    ]

    choices  = ['professionals','technicians','white_collar_worker','blue_collar_worker','elementary','military']
    pgen['isco88_choices'] =  np.select(conditions,choices, default=np.nan)

    return pgen

def isco88_toisco08(df,isco08_88):
    " outdated"

    dict_isco08 = {row['isco-88'] : row['ISCO-08-skill-level'] for i, row in isco08_88.iterrows()}  # dictionary

    df['isco08_skill_level'] = df['isco-88'].replace(to_replace=dict_isco08.keys(), value=dict_isco08.values())

    return df

def isco08_skill_level(df,isco08_88):

    dict_isco08 = {row['ISCO08'] : row['ISCO08_skilllevel'] for i, row in isco08_88.iterrows()}  # dictionary 08
    dict_isco88 = {row['ISCO88'] : row['ISCO08_skilllevel'] for i, row in isco08_88.iterrows()}  # dictionary 88

    df['ISCO08_skilllevel'] = df['isco08'].replace(to_replace=dict_isco08.keys(), value=dict_isco08.values())
    df['ISCO08_skilllevel'] = df['isco88'].replace(to_replace=dict_isco88.keys(), value=dict_isco88.values())

    return df

def poccupation_isco08(df):
    """
    Classify based on skill_level isco08

    """
    conditions = (df['ISCO08_skilllevel']==4,
                    df['ISCO08_skilllevel']==3,
                    df['ISCO08_skilllevel']==21,
                    df['ISCO08_skilllevel']==22,
                    df['ISCO08_skilllevel']==1,
    )
    choices = ['Professionals','Technicians','"White-Collar"','Blue-collar','Elementary']

    df['isco08_choices'] =  np.select(conditions,choices, default=np.nan)

    return df

def convert_fm_country_origin(df,dict):
    """
    Classify country of origin based on father country of origin, when nan value appear then take mother country of origin

    df: target dataset
    dict: dictionary to group country of origin
    """
    # Create columns of father country of origin
    dict_forigin = {row['value'] : row['group'] for i, row in dict.iterrows()}  # dictionary

    #Then replace categorical variables in dataset
    df['forigin_group'] = df['forigin'].replace(to_replace=dict_forigin.keys(), value=dict_forigin.values())
    df['morigin_group'] = df['morigin'].replace(to_replace=dict_forigin.keys(), value=dict_forigin.values())

    #Default country of natives (some NA value)
    df['forigin_group'] = np.where(df['migback']==1,'German_native',df['forigin_group'])
    df['morigin_group'] = np.where(df['migback']==1,'German_native',df['morigin_group'])

    return df
    
def ethnic_origin(df):

    df["ethnic_origin"] = np.where(df['forigin_group'] =="invalid",
                                                  df['morigin_group'],
                                                  df['forigin_group']
                                                  )
    df["ethnic_origin"] = np.where(df['migback']==1,'Germany_native',df["ethnic_origin"])
    
    return df

def convert_father_training(df):
    conditions = [df['fprofedu']==10,
                  df['fprofedu'].between(20,23,inclusive = True),
                  df['fprofedu']==24,
                  df['fprofedu']==25,
                  df['fprofedu']==26,
                  df['fprofedu']==28,
                  df['fprofedu'].isin([27,30]),
                  df['fprofedu'].isin([31,32]),
                  df['fprofedu'] == 40,
                  df['fprofedu'].isin([50,51])
             ]
    choices  = ['no_vocational_degree','gen_vocational_degree','trade_farm','business','healthcare', 'civil_service','tech_engineer','college_uni','others','in_training']
    df['father_training'] =  np.select(conditions,choices, default=np.nan)

    return df

def classify_migback(df):
    """
    Classify 2nd generation of immigrant
    """

    df['mig_age7'] = df['immiyear'] - df['gebjahr']

    migconditions = [df['migback']==1,
                    (df['migback']==2)&(df['mig_age7'].between(0,7,inclusive = True)),
                    df['migback']==3,
                    ]
    migchoices = [0,1,1]
    df['gen2_migration'] =  np.select(migconditions,migchoices,default=np.nan)

    return df

def convert_ling_distance(df,forigin_info):

    # Create columns of father country of origin
    dict_ling = {row['value'] : row['ling_distance'] for i, row in forigin_info.iterrows()}  # dictionary
    
    #Then replace categorical variables in dataset
    df['fling_distance'] = df['forigin'].replace(to_replace=dict_ling.keys(), value=dict_ling.values())
    df['mling_distance'] = df['morigin'].replace(to_replace=dict_ling.keys(), value=dict_ling.values())
    
    return df

def cohort_effect_interaction(df):
    ch_list = ["millennials"] #'baby_boomer',
    cou_list = ['forigin_group_Balkans',
                'forigin_group_German_native',
                'forigin_group_German_group',
                'forigin_group_South_Europe',
                'forigin_group_Turkish_group'
                ]
    for i in ch_list:
        for j in cou_list:
            df[i+j] = df[j] * df[i]
    return df

def cohort_effect_interaction_ethnic(df):
    ch_list = ["millennials"] #'baby_boomer',
    cou_list = ['ethnic_origin_Balkans',
                'ethnic_origin_German_native',
                'ethnic_origin_German_group',
                'ethnic_origin_South_Europe',
                'ethnic_origin_Turkish_group'
                ]
    for i in ch_list:
        for j in cou_list:
            df[i+j] = df[j] * df[i]
    return df