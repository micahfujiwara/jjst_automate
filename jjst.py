import pandas as pd
import numpy as np
import re
from datetime import datetime, timedelta


sharepointFilepath = '/Users/micahfujiwara/Desktop/ht/SharepointJJST.csv'
sfdFilepath = '/Users/micahfujiwara/Desktop/ht/JJST.xlsx'


def sharepoint_file():
    """getting relevant data from sharepoint file"""
    df = pd.read_csv(sharepointFilepath)
    df.drop(columns=[
        'Resolved date', 'Attachments', 'Customer Name', 'Request Type', 'Order Number', 'Reason for NO SALE', 'Account', 'Working TN', 'ACO',
        'Order Due Date', 'Service Type', 'Status', 'Received from', 'Root Cause', 'SAID', 'Terminal ID', 'FDH', 
        'Doors Fiber Enabled',	'Latitude', 'Longitude', 'CAF', 'Referred by', 'Resolved By'], 
        inplace=True)
    
    df = df.fillna(0)
    df['Created'] = pd.to_datetime(df['Created'])
    
    """actual code"""
    today = datetime.now()
    current_month = today.month
    current_year = today.year
    #only showing data for the current month and year
    df = df[(df['Created'].dt.month == current_month) & (df['Created'].dt.year == current_year)]
    df['Service Address'] = df['Service Address'].str.lower()
    df['Service Address'] = df['Service Address'].str.split()
    df['House Number'] = df['Service Address'].str.get(0)
    
    """zip code info"""
    df['Zip Code'] = df['Service Address'].str.get(-1).astype(str)
    zip_code_pattern = r'^\d{5}(?:-\d{4})?$'
    df['Zip Code'] = df.apply(lambda row: row['Zip Code'] if pd.Series(row['Zip Code']).str.contains(zip_code_pattern).any() else 'No Zip Code', axis=1)


    """street/city info"""    
    df['Street'] = df.apply(extract_street_name, axis=1)
    df['City'] = df.apply(extract_city_name, axis=1)
    
    print(df)
    df.to_csv('test.csv', index=False)
    return df
    
    
    
    

def extract_street_name(row):
    """Extracts the street name while treating punctuation as part of the word"""
    
    street_name_endings = ['st', 'street', 'rd', 'road', 'ave', 'avenue', 'pl', 'place', 'cir', 'circle', 'hwy', 'highway', 'drive', 'dr',
                           'blvd', 'lane', 'ln', 'pkwy', 'loop', 'lp']
    street_name = []
    service_address = row['Service Address']
    found_street = False  # Flag to stop after finding the street name
    
    if isinstance(service_address, list):
        for word in service_address[1:]:
            if found_street:
                break
            
            if any(word.endswith(ending) for ending in street_name_endings):
                # Remove punctuation from the start and end of the word
                cleaned_word = re.sub(r'^[^\w\s]+|[^\w\s]+$', '', word)
                street_name.append(cleaned_word)
                found_street = True  # Set the flag to stop processing
            
            else:
                street_name.append(word)
    
    return ' '.join(street_name)




def extract_city_name(row):
    """Extracts the city name while ignoring punctuation"""
    
    street_name_endings = ['st', 'street', 'rd', 'road', 'ave', 'avenue', 'pl', 'place', 'cir', 'circle', 'hwy', 'highway', 'drive', 'dr',
                           'blvd', 'lane', 'ln', 'pkwy', 'loop', 'lp']
    city = ""
    service_address = row['Service Address']
    
    if isinstance(service_address, list):
        for i, word in enumerate(service_address):
            if any(word.endswith(ending) for ending in street_name_endings):
                if i + 1 < len(service_address):
                    next_word = re.sub(r'[^\w\s]', '', service_address[i + 1])
                    city = next_word
                break
    
    return city





def sfd_support_file():
    """sfd file manipulation"""
    df = pd.read_excel(sfdFilepath)
    sheet_names = pd.ExcelFile(sfdFilepath).sheet_names
    last_sheet_name = sheet_names[-1]
    last_sheet_df = pd.read_excel(sfdFilepath, sheet_name=last_sheet_name)
    last_row_index = last_sheet_df.last_valid_index()
    if last_row_index is None:
        start_row_index = 0
    else:
        start_row_index = last_row_index + 1
    
    

def main():
    sharepoint_file()
    # sfd_support_file()
    
if __name__ == '__main__':
    main()
    
    
    