import requests
import pandas as pd
 
# url_template = r'https://api.eia.gov/v2/electricity/rto/region-data/data/?frequency=hourly&data[0]=value&start=2023-11-15T00&end=2024-04-15T00&sort[0][column]=period&sort[0][direction]=desc&offset={offset}&length=5000&api_key=jIOjeRRDAMYkT5aGDZgzqWZedy0uOsvcbWQeYyyW'
 
# get data from the api url
url_template = r'https://api.eia.gov/v2/electricity/rto/daily-region-sub-ba-data/data/?frequency=daily&data[0]=value&facets[subba][]=NCEN&facets[parent][]=ERCO&facets[timezone][]=Central&sort[0][column]=period&sort[0][direction]=asc&offset=0&length=50000&api_key=OnfTQ00ROLCCmUPP1n5IrvWJcom60KghdbxUKS7x'
def fetch_data(offset):
    url = url_template.format(offset=offset)
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: Unable to fetch data (Status code: {response.status_code})")
        return None
 
def fetch_all_data():
    all_data = []
    offset = 0
    while True:
        data = fetch_data(offset)
        if data is None:
            break
        all_data.extend(data['response']['data'])
        offset += 5000
        if len(data['response']['data']) < 5000:  # Adjust this value based on the total number of records
            break
    return all_data
 
def main():
    all_data = fetch_all_data()
 
    # Create DataFrame from all the retrieved data
    df = pd.DataFrame(all_data)
 
    # Write DataFrame to an Excel file
    output_excel_path = 'electricity_data.xlsx'
    df.to_excel(output_excel_path, index=False)
    print(f"DataFrame successfully written to {output_excel_path}")
 
if __name__ == "__main__":
    main()