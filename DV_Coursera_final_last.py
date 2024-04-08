import pandas as pd
import matplotlib as mpl
import folium
import aiohttp
import asyncio
import os

url_us_states = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/us-states.json'

async def download(url, filename):
    if not os.path.exists(filename):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    with open(filename, 'wb') as file:
                        while True:
                            chunk = await resp.content.read(1024)
                            if not chunk:
                                break
                            file.write(chunk)
    else:
        print("Using existing file.")

async def main():
    await download(url_us_states, 'us-states.json')
    df_us = pd.read_json('us-states.json')  # Corrected line to read JSON file
    df_recession = pd.read_csv(r'E:\NpowerLab\DataSets\historical_automobile_sales.csv')

    print(df_us.head())
    print(df_us.columns)


    '''
     Create a map on the hightest sales region/offices of the company during recession period
    '''
    recession_data = df_recession[df_recession['Recession'] == 1]  # Corrected variable name

    # Calculate the total sales by city
    sales_by_city = recession_data.groupby('City')['Automobile_Sales'].sum().reset_index()

    # Create a base map centered on the United States
    map1 = folium.Map(location=[37.0902, -95.7129], zoom_start=4)

    # Load the GeoJSON file containing state boundaries
    geo_json_data = 'us-states.json'

    # Create a choropleth layer using Folium
    choropleth = folium.Choropleth(
        geo_data=geo_json_data,  # GeoJSON file with state boundaries
        data=sales_by_city,
        columns=['City', 'Automobile_Sales'],
        key_on='feature.properties.name',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Automobile Sales during Recession'
    ).add_to(map1)

    # Add tooltips to the choropleth layer
    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(['name'], labels=True)
    )

    # Display the map
    map1.save('map1.html')

if __name__ == '__main__':
    asyncio.run(main())
