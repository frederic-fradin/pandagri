import os
import requests
import pandas as pd

from zipfile import ZipFile
from datetime import date

today = date.today()
current_year = today.year

def load_com_disagg(year:int=current_year) -> None:
    #  Download the data behind the URL
    url = f'https://www.cftc.gov/files/dea/history/com_disagg_txt_{year}.zip'
    response = requests.get(url)

    #  Open the response generated into a new file in your local called image.jpg
    open("../data/raw/cftc.zip", "wb").write(response.content)

    # loading the temp.zip and creating a zip object 
    with ZipFile('../data/raw/cftc.zip', 'r') as zObject: 
        zObject.extractall(path='../data/raw/')
        zObject.extract("c_year.txt", path='../data/raw/') 
        zObject.close()

    # rename file with year to loop through a period
    try:
        os.rename("../data/raw/c_year.txt", f"../data/raw/cftc_{year}.txt")
    except FileExistsError:
        print("File already Exists")
        print("Removing existing file")
        # skip the below code if you don't' want to forcefully rename
        os.remove(f"../data/raw/cftc_{year}.txt")
        # rename it
        os.rename("../data/raw/c_year.txt", f"../data/raw/cftc_{year}.txt")
        print('Done renaming a file')

    print(f'CFTC {year} download with success!')

def consolidate_com_disagg() -> None:
    # assign directory
    directory = '../data/raw/'
    init = pd.DataFrame()

    # iterate over files in that directory
    for filename in os.listdir(directory):
        file = os.path.join(directory, filename)
        split_tup = os.path.splitext(filename)
        # checking if it is a file
        if os.path.isfile(file) and split_tup[1] == '.txt':
            raw = pd.read_table(file, delimiter=",", low_memory=False)
            first_23_columns = raw.iloc[:, :23]
            last_6_columns = raw.iloc[:, -6:]
            select = pd.concat([first_23_columns, last_6_columns], axis=1)
            init = pd.concat([init, select], axis=0)
            init.replace('.', 0, inplace=True)
    
    print(f'Concatenate dataframe with success!', end='\n\n')
    init.to_parquet('../data/processed/cftc.parquet', engine='fastparquet')

    keep_columns = ['Market_and_Exchange_Names', 'As_of_Date_In_Form_YYMMDD',
       'Report_Date_as_YYYY-MM-DD', 'CFTC_Contract_Market_Code',
       'CFTC_Market_Code', 'CFTC_Region_Code', 'CFTC_Commodity_Code',
       'Contract_Units', 'CFTC_Contract_Market_Code_Quotes',
       'CFTC_Market_Code_Quotes', 'CFTC_Commodity_Code_Quotes',
       'CFTC_SubGroup_Code', 'FutOnly_or_Combined']

    # Melting the DataFrame to transform other columns into rows
    df_melted = init.melt(id_vars=keep_columns, 
                        var_name='argument', 
                        value_name='value')

    df_melted['Market_and_Exchange_Names'] = df_melted['Market_and_Exchange_Names'].str.rstrip()
    df_melted['CFTC_Market_Code'] = df_melted['CFTC_Market_Code'].str.rstrip()
    df_melted['Market_and_Exchange_Names'] = df_melted.apply(lambda row: row['Market_and_Exchange_Names'].split(' - ')[0], axis=1)
                                                   
    df_melted['Classifications'] = df_melted.apply(lambda row: row['argument'].split('_')[0] 
                                                    if row['argument'].split('_')[0] in ['Swap', 'NonRept'] else
                                                    row['argument'].split('_')[0] + row['argument'].split('_')[1], axis=1)
    
    df_melted['Position_type'] = df_melted.apply(lambda row: row['argument'].split('_')[-2], axis=1)
    
    df_melted['Value_signed'] = df_melted.apply(lambda row: row['value'] * -1 if row['Position_type'] == 'Short'
                                                    else row['value'], axis=1)

    print(f'Melt dataframe with success!', end='\n\n')
    df_melted.to_parquet('../data/cleaned/cftc.parquet', engine='fastparquet')


if __name__ == "__main__":
    # load_com_disagg(current_year)
    consolidate_com_disagg()