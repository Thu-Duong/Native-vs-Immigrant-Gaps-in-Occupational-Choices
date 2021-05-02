import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def plot_occupations_by_year(df):
    """Plot decisions by year.

    Parameters:
    -----------
    df: pd.DataFrame
        Dataframe consisting of decision data.
        
    Returns:
    --------
        Figure.
    """
    labels = ['Professionals','Technicians','White-Collar','Blue-Collar','Elementary']
    #'training_schooling','unemployed','maternity_leave'

    fig, ax = plt.subplots(figsize=(12,8))

    shares = df.groupby("year").isco_modified.value_counts(normalize=True).unstack()[labels] * 100
    # Choices should be ordered: blue_collar, white_collar, military, school, home
    # Black white will be determined via colors here.
    shares.plot.bar(stacked=True, ax=ax, width=0.8, cmap='RdBu')

    #ax.set_xticklabels(np.arange(35, 27, 1), rotation="horizontal")
    ax.yaxis.get_major_ticks()[0].set_visible(False)

    ax.set_ylabel("Share (in %)")
    ax.set_xlabel("Year")
    ax.set_ylim(0, 100)

    ax.legend(
        labels=[label.split("_")[0].capitalize() for label in labels],
        loc="lower center",
        bbox_to_anchor=(0.5, 1.04),
        ncol=6,
    )
    return fig

def plot_occupations_by_age(df):
    """Plot decisions by age < 60.

    Parameters:
    -----------
    df: pd.DataFrame
        Dataframe consisting of decision data.
        
    Returns:
    --------
        Figure.
    """
    #labels = ['training_schooling','unemployed','maternity_leave']
    labels = ['Professionals','Technicians','White-Collar','Blue-Collar','Elementary']

    fig, ax = plt.subplots(figsize=(12,8))

    # Choices should be ordered: 'professionals','technicians','white_collar_worker','blue_collar_worker','elementary','military'
    shares = df.groupby("age").isco_modified.value_counts(normalize=True).unstack()[labels] * 100
    shares.plot.bar(stacked=True, ax=ax, width=0.8, cmap='RdBu')

    #ax.set_xticklabels(np.arange(35, 27, 1), rotation="horizontal")
    ax.set_xlabel("Age")

    ax.yaxis.get_major_ticks()[0].set_visible(False)
    ax.set_ylabel("Share (in %)")
    ax.set_ylim(0, 100)

    ax.legend(
        labels=[label.split("_")[0].capitalize() for label in labels],
        loc="lower center",
        bbox_to_anchor=(0.5, 1.04),
        ncol=6,
    )
    return fig

def plot_occupations_by_yearbirth(df):
    """Plot decisions by age < 60.

    Parameters:
    -----------
    df: pd.DataFrame
        Dataframe consisting of decision data.
        
    Returns:
    --------
        Figure.
    """
    #labels = ['training_schooling','unemployed','maternity_leave']
    labels = ['Professionals','Technicians','White-Collar','Blue-Collar','Elementary']

    fig, ax = plt.subplots(figsize=(12,8))

    # Choices should be ordered: 'professionals','technicians','white_collar_worker','blue_collar_worker','elementary','military'
    shares = df.groupby('gebjahr').isco_modified.value_counts(normalize=True).unstack()[labels] * 100
    shares.plot.bar(stacked=True, ax=ax, width=0.8, cmap='RdBu')

    #ax.set_xticklabels(np.arange(35, 27, 1), rotation="horizontal")
    ax.set_xlabel("year of birth")

    ax.yaxis.get_major_ticks()[0].set_visible(False)
    ax.set_ylabel("Share (in %)")
    ax.set_ylim(0, 100)

    ax.legend(
        labels=[label.split("_")[0].capitalize() for label in labels],
        loc="lower center",
        bbox_to_anchor=(0.5, 1.04),
        ncol=6,
    )
    return fig
    
def plot_ethnic_group_by_year(df,labels):
    """Plot decisions by age.

    Parameters:
    -----------
    df: pd.DataFrame
        Dataframe consisting of decision data.
        
    Returns:
    --------
        Figure.
    """

    fig, ax = plt.subplots(figsize=(10,8))

    shares = df.groupby("year").ethnic_group.value_counts(normalize=True).unstack()[labels]*100
    # Black white will be determined via colors here.
    shares.plot.bar(stacked=True, ax=ax, width=0.8, cmap='RdBu')

    ax.set_xlabel("Year")
    #ax.yaxis.get_major_ticks()[0].set_visible(False)

    ax.set_ylabel("Share (in %)")
    ax.set_ylim(0, 100)

    ax.legend(
        labels=[label.capitalize() for label in labels],
        loc="lower center",
        bbox_to_anchor=(0.5, 1.04),
        ncol=5,
    )
    return fig

def plot_fcountry_origin_by_year(df,labels):
    """Plot decisions by age.

    Parameters:
    -----------
    df: pd.DataFrame
        Dataframe consisting of decision data.
        
    Returns:
    --------
        Figure.
    """

    fig, ax = plt.subplots(figsize=(12,8))

    shares = df.groupby("syear").forigin_group.value_counts(normalize=True).unstack()[labels]*100
    # Black white will be determined via colors here.
    shares.plot.bar(stacked=True, ax=ax, width=0.8, cmap='RdBu')

    ax.set_xlabel("Year")
    #ax.yaxis.get_major_ticks()[0].set_visible(False)

    ax.set_ylabel("Share (in %)")
    ax.set_ylim(0, 100)

    ax.legend(
        labels=[label.capitalize() for label in labels],
        loc="lower center",
        bbox_to_anchor=(0.5, 1.04),
        ncol=5,
    )
    return fig

def plot_mcountry_origin_by_year(df,labels):
    """Plot decisions by age.

    Parameters:
    -----------
    df: pd.DataFrame
        Dataframe consisting of decision data.
        
    Returns:
    --------
        Figure.
    """

    fig, ax = plt.subplots(figsize=(12,8))

    shares = df.groupby("syear").morigin_group.value_counts(normalize=True).unstack()[labels]*100
    # Black white will be determined via colors here.
    shares.plot.bar(stacked=True, ax=ax, width=0.8, cmap='RdBu')

    ax.set_xlabel("Year")
    #ax.yaxis.get_major_ticks()[0].set_visible(False)

    ax.set_ylabel("Share (in %)")
    ax.set_ylim(0, 100)

    ax.legend(
        labels=[label.capitalize() for label in labels],
        loc="lower center",
        bbox_to_anchor=(0.5, 1.04),
        ncol=5,
    )
    return fig

def plot_corr_occupation_by_ethnic_group(df):
    
    heatmap = pd.crosstab(df.ethnic_group, df.isco_modified, normalize='index')
    
    fig, ax = plt.subplots(figsize=(12,8))
    sns.heatmap(heatmap,cmap='PuBu', annot=True)
    
    ax.set_xlabel("Occupation")
    ax.set_ylabel("Ethnic group")
    return fig
    
def plot_corr_occupation_by_fcountry_origin(df):
    
    heatmap = pd.crosstab(df.forigin_group, df.isco08_choices, normalize='index')
    
    fig, ax = plt.subplots(figsize=(12,8))
    sns.heatmap(heatmap,cmap='PuBu', annot=True)
    
    ax.set_xlabel("Occupation")
    ax.set_ylabel("Father country of origin")
    return fig

def plot_corr_freli_by_mreli(df):
    
    heatmap = pd.crosstab(df.freli, df.mreli, normalize='index')
    
    fig, ax = plt.subplots(figsize=(12,8))
    sns.heatmap(heatmap,cmap='PuBu', annot=True)
    
    ax.set_xlabel("Religion Mother")
    ax.set_ylabel("Religion Father")
    return fig
    
def plot_corr_freli_by_fcountry_origin(df):
    
    heatmap = pd.crosstab(df.forigin_group, df.freli, normalize='index')
    
    fig, ax = plt.subplots(figsize=(12,8))
    sns.heatmap(heatmap,cmap='PuBu', annot=True)
    
    ax.set_xlabel("Religion Father")
    ax.set_ylabel("Country of origin")
    return fig