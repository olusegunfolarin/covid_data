import logging
import pandas as pd
import os


logger = logging.getLogger(__name__)


def load_csv(csv_path):
    """Load CSVs fr transformation from temporary storage

    Parameters
    ---------
    csv_path: str
        Path to CSV to be loaded
    
    Returns: dataFrame
        A pandas dataframe
    """
    df = pd.read_csv(csv_path)
    return df

def parse_dates(df, cols_to_parse, format="%Y-%m-%d"):
    """Parses the dataframe colums listed as date objects

    Parameters
    ----------
    df: DataFrame
        A dataframe object
    
    cols_to_parse: list
        A list of columns that need to be parsed as a date object
    
    format: str
        The format of the date output default is "YYYY-MM-DD"

    Returns
    -------
    df: DataFrame
        A dataframe with date colums parsed as Date objects
    """

    if len(cols_to_parse) > 1:
        for col in cols_to_parse:
            df[col] = pd.to_datetime(df[col], format=format)
    else:
        df[cols_to_parse[-1]] = pd.to_datetime(df[cols_to_parse[-1]], format=format)
    
    return df

def create_country_col(df, col="areaCode"):
    """Creates a Country column from the Area code

    Parameters
    ---------
    df: Dataframe
        Dataframe object with areaCode column
    
    Returns
    -------
    Dataframe
    """
    # create a nations dictionary mapping first letter
    nation_dict = {
        'E': 'England',
        'S': 'Scotland',
        'W': 'Wales',
        'N' : 'Northern Ireland'
    }
    if col in df.columns:
        df["nation"] = df[col].str[0]
        # map nations dict to nation
        df["nation"] = df.nation.map(nation_dict)
        
    else:
        logger.error(f"Schema changed. \"{col}\" not in Datframe")
        
    return df
    
def create_unique_from_columns(df):
    """Creates a unique ID from the columns in the table
    """
    df['id'] = df['areaCode'] + "-"  + df['date'].astype(str)
    return df


if __name__ == "__main__":
    df = load_csv("/home/olusegun/projects/covid_data/dev.csv")
    df = create_country_col(df)
    df = parse_dates(df, ['date'])
    df = create_unique_from_columns(df)
    print(df[['date', 'id']].head(2))
    # print(df[['areaCode', 'date']].duplicated().sum() == 0)
    # print((df['date'] <= "2021-10-11").all())
