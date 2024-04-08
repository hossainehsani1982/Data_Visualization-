import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import folium
import io
import aiohttp
import asyncio
import os


url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv"


async def download_data():
    if not os.path.exists(r'E:\NpowerLab\DataSets\historical_automobile_sales.csv'):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    with open(r'E:\NpowerLab\DataSets\historical_automobile_sales.csv', 'wb') as file:
                        while True:
                            chunk = await resp.content.read(1024)
                            if not chunk:
                                break
                            file.write(chunk)
    else:
        print("Using existing file.")




async def main():
    await download_data()

    df = pd.read_csv(r'E:\NpowerLab\DataSets\historical_automobile_sales.csv')
    print(df.describe())
    print(df.columns)


    # Plotting
    df['Year'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Year'].dt.year


    #grouping the data by year
    df_line = df.groupby(df['Year'])['Automobile_Sales'].mean()


    plt.figure(figsize=(10, 6))
    df_line.plot(kind = 'line')    
    plt.title('Automobile Sales Fluctuation')
    plt.xlabel('Year')
    plt.ylabel('average automobile sales price')
    
    # Plotting
    df['Year'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Year'].dt.year

    #grouping the data by year
    df_line = df.groupby(df['Year'])['Automobile_Sales'].mean()

    plt.figure(figsize=(10, 6))
    df_line.plot(kind = 'line')    
    plt.title('Automobile Sales Fluctuation')
    plt.xticks(list(range(1980,2024)), rotation = 75)
    plt.xlabel('Year')
    plt.ylabel('average automobile sales price')
    plt.title('Automobile Sales during Recession')
    plt.text(1982, 650, '1981-82 Recession')
    plt.legend()
    plt.show()

    '''
    Plot different lines for categories of vehicle type and analyse the trend to answer the question Is there 
    a noticeable difference in sales trends between different vehicle types during recession periods?
    '''
    df_Mline = df.groupby(['Year','Vehicle_Type'], as_index=False)['Automobile_Sales'].sum()
    df_Mline.set_index('Year', inplace=True)
    df_Mline = df_Mline.groupby(['Vehicle_Type'])['Automobile_Sales']
    df_Mline.plot(kind='line')
    plt.xlabel('Year')
    plt.ylabel('average automobile sales price')
    plt.title('Sales Trend Vehicle-wise during Recession')
    plt.text(1982, 650, '1981-82 Recession')
    plt.legend()
    plt.show()
    
    '''
    compare the sales of different vehicle types during a recession and a non-recession period
    '''
    recession_data = df[df['Recession'] == 1]

    print(recession_data)

    dd=df.groupby(['Recession','Vehicle_Type'])['Automobile_Sales'].mean().reset_index()

    print(dd)

    # Calculate the total sales volume by vehicle type during recessions
    #sales_by_vehicle_type = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].sum().reset_index()

    # Create the grouped bar chart using seaborn

    plt.figure(figsize=(10, 6))
    sns.barplot(x='Recession', y='Automobile_Sales', hue='Vehicle_Type', data=dd)
    plt.xticks(ticks=[0, 1], labels=['Non-Recession', 'Recession'])
    plt.xlabel('Recession Period')
    plt.ylabel('Average Automobile Sales')
    plt.title('Vehicle-Wise Sales during Recession and Non-Recession Period')
    plt.legend(title='Vehicle Type', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

    '''
    TASK 1.4: Use sub plotting to compare the variations in GDP during recession and non-recession period by developing line plots for each period.
    '''
    rec_data = df[df['Recession'] == 1]
    non_rec_data = df[df['Recession'] == 0]
    
    #Figure
    fig = plt.figure(figsize=(12, 6))

    # Create different axes for subplotting
    ax0 = fig.add_subplot(1, 2, 1)  # add subplot 1 (1 row, 2 columns, first plot)
    ax1 = fig.add_subplot(1, 2, 2)  # add subplot 2 (1 row, 2 columns, second plot)

    sns.lineplot(x='Year', y='GDP', data=rec_data, label='Recession', ax=ax0)
    ax0.set_xlabel('Year')
    ax0.set_ylabel('GDP')
    ax0.set_title('GDP Variation during Recession Period')

    sns.lineplot(x='Year', y='GDP', data=non_rec_data, label='Non-Recession', ax=ax1)
    ax1.set_xlabel('Year')
    ax1.set_ylabel('GDP')
    ax1.set_title('GDP Variation during Non-Recession Period')

    plt.tight_layout()
    plt.show()

   #------------------------------------------------Alternatively--------------
   #Using subplot()
    plt.figure(figsize=(12, 6))

    # Subplot 1
    plt.subplot(1, 2, 1)
    sns.lineplot(x='Year', y='GDP', data=rec_data, label='Recession')
    plt.xlabel('Year')
    plt.ylabel('GDP')
    plt.title('GDP Variation during Recession Period')
    plt.legend()

    # Subplot 2
    plt.subplot(1, 2, 2)
    sns.lineplot(x='Year', y='GDP', data=non_rec_data, label='Non-Recession')
    plt.xlabel('Year')
    plt.ylabel('GDP')
    plt.title('GDP Variation during Non-Recession Period')
    plt.legend()

    plt.tight_layout()
    plt.show()

    '''
    1.5: Develop a Bubble plot for displaying the impact of seasonality on Automobile Sales.
    '''

    non_rec_data = df[df['Recession'] == 0]

    size = non_rec_data['Seasonality_Weight']  # for bubble effect

    sns.scatterplot(data=non_rec_data, x='Month', y='Automobile_Sales', size=size, hue='Seasonality_Weight', legend=False)

    plt.xlabel('Month')
    plt.ylabel('Automobile Sales')
    plt.title('Seasonality Impact on Automobile Sales')

    plt.show()

    '''
    1.6 Use the functionality of Matplotlib to develop a
    scatter plot to identify the correlation between average vehicle price relate to the sales volume during recessions.
    '''
    #Create dataframes for recession and non-recession period
    rec_data = df[df['Recession'] == 1]

    plt.scatter(rec_data['Consumer_Confidence'], rec_data['Automobile_Sales'])

    plt.xlabel('Consumer Confidence')
    plt.ylabel('Automobile Sales')
    plt.title('Correlation between Consumer Confidence and Automobile Sales during Recessions')

    plt.show()

    '''
    1.7: Create a pie chart to display the portion of advertising expenditure of 
    XYZAutomotives during recession and non-recession periods.¶    
    '''
 # Filter the data 
    rec_data = df[df['Recession'] == 1]

# Calculate the advertising expenditure by category during recessions
    sales_by_vehicle_type = rec_data.groupby('Vehicle_Type')['Automobile_Sales'].sum()


# Create a pie chart for the share of each advertising category in total expenditure during recessions
    plt.figure(figsize=(8, 8))

    labels = sales_by_vehicle_type.index
    sizes = sales_by_vehicle_type.values
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)

    plt.title('Portion of Advertising Expenditure during Recession Periods')

    plt.show()

    '''
    1.8: Develop a pie chart to display the total Advertisement expenditure for each vehicle type during recession period.
    '''
    Rdata = df[df['Recession'] == 1]

    ad_expenditure_by_vehicle_type = rec_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum()

    # Create a pie chart for the share of advertisement expenditure for each vehicle type during recessions
    plt.figure(figsize=(8, 8))

    labels = ad_expenditure_by_vehicle_type.index
    sizes = ad_expenditure_by_vehicle_type.values
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)

    plt.title('Total Advertisement Expenditure by Vehicle Type during Recession Periods')

    plt.show()

    '''
    1.9: Develop a lineplot to analyse the effect of the unemployment rate on vehicle type and sales during the Recession Period.
    '''
    df_rec = df[df['Recession']==1]
    sns.lineplot(data=df_rec, 
                 x='unemployment_rate', 
                 y='Automobile_Sales', 
                 hue='Vehicle_Type', 
                 markers='o', 
                 err_style=None)


    plt.ylim(0,850)
    plt.legend(loc=(0.05,.3))

if __name__ == "__main__":
    asyncio.run(main())