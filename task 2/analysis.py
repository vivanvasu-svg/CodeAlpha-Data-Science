import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")

def main():
    print("Starting unemployment analysis...")
    
    # Path setups
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "archive(1)")
    charts_dir = os.path.join(base_dir, "charts")
    os.makedirs(charts_dir, exist_ok=True)
    
    file1 = os.path.join(data_dir, "Unemployment in India.csv")
    file2 = os.path.join(data_dir, "Unemployment_Rate_upto_11_2020.csv")
    
    # Process Dataset 1 (urban/rural split)
    print(f"Reading: {file1}")
    df1 = pd.read_csv(file1)
    df1.columns = df1.columns.str.strip()
    df1 = df1.dropna(how='all')
    df1 = df1.dropna(subset=['Region', 'Date', 'Estimated Unemployment Rate (%)'])
    
    # Strip string fields
    for col in ['Region', 'Frequency', 'Area']:
        if col in df1.columns:
            df1[col] = df1[col].astype(str).str.strip()
            
    df1['Date'] = pd.to_datetime(df1['Date'].astype(str).str.strip(), format='%d-%m-%Y', errors='coerce')
    df1 = df1.dropna(subset=['Date'])
    
    df1['Year'] = df1['Date'].dt.year
    df1['Month_Num'] = df1['Date'].dt.month
    df1['Month_Name'] = df1['Date'].dt.strftime('%b')
    df1['Year_Month'] = df1['Date'].dt.to_period('M')
    
    df1 = df1.rename(columns={
        'Region': 'State',
        'Estimated Unemployment Rate (%)': 'Unemployment_Rate',
        'Estimated Employed': 'Employed',
        'Estimated Labour Participation Rate (%)': 'Labour_Participation_Rate'
    })
    
    df1['Unemployment_Rate'] = pd.to_numeric(df1['Unemployment_Rate'], errors='coerce')
    df1['Employed'] = pd.to_numeric(df1['Employed'], errors='coerce')
    df1['Labour_Participation_Rate'] = pd.to_numeric(df1['Labour_Participation_Rate'], errors='coerce')
    
    # Process Dataset 2 (consolidated state details)
    print(f"Reading: {file2}")
    df2 = pd.read_csv(file2)
    df2.columns = df2.columns.str.strip()
    
    df2 = df2.rename(columns={
        'Region': 'State',
        'Region.1': 'Zone',
        'Estimated Unemployment Rate (%)': 'Unemployment_Rate',
        'Estimated Employed': 'Employed',
        'Estimated Labour Participation Rate (%)': 'Labour_Participation_Rate',
        'longitude': 'Longitude',
        'latitude': 'Latitude'
    })
    
    df2 = df2.dropna(how='all')
    df2 = df2.dropna(subset=['State', 'Date', 'Unemployment_Rate'])
    
    for col in ['State', 'Frequency', 'Zone']:
        if col in df2.columns:
            df2[col] = df2[col].astype(str).str.strip()
            
    df2['Date'] = pd.to_datetime(df2['Date'].astype(str).str.strip(), format='%d-%m-%Y', errors='coerce')
    df2 = df2.dropna(subset=['Date'])
    
    df2['Year'] = df2['Date'].dt.year
    df2['Month_Num'] = df2['Date'].dt.month
    df2['Month_Name'] = df2['Date'].dt.strftime('%b')
    df2['Year_Month'] = df2['Date'].dt.to_period('M')
    
    df2['Unemployment_Rate'] = pd.to_numeric(df2['Unemployment_Rate'], errors='coerce')
    df2['Employed'] = pd.to_numeric(df2['Employed'], errors='coerce')
    df2['Labour_Participation_Rate'] = pd.to_numeric(df2['Labour_Participation_Rate'], errors='coerce')
    
    print("\n--- Dataset 1 Summary ---")
    print(df1[['Unemployment_Rate', 'Employed', 'Labour_Participation_Rate']].describe())
    print("\n--- Dataset 2 Summary ---")
    print(df2[['Unemployment_Rate', 'Employed', 'Labour_Participation_Rate']].describe())
    
    # Plotting Trends
    print("\nGenerating charts...")
    
    # Chart 1: Unemployment Rate Trend
    plt.figure(figsize=(10, 5))
    trend1 = df1.groupby('Date')['Unemployment_Rate'].mean().reset_index()
    trend2 = df2.groupby('Date')['Unemployment_Rate'].mean().reset_index()
    
    sns.lineplot(data=trend1, x='Date', y='Unemployment_Rate', label='Dataset 1 (Rural/Urban Combined)', marker='o', color='#3498db')
    sns.lineplot(data=trend2, x='Date', y='Unemployment_Rate', label='Dataset 2 (State consolidated)', marker='s', color='#e74c3c')
    
    # Highlight lockdown
    plt.axvspan(pd.to_datetime('2020-03-24'), pd.to_datetime('2020-06-30'), color='grey', alpha=0.2, label='Lockdown')
    plt.title("Monthly Unemployment Rate Trend in India (2019-2020)")
    plt.xlabel("Date")
    plt.ylabel("Unemployment Rate (%)")
    plt.legend(frameon=True)
    plt.tight_layout()
    plt.savefig(os.path.join(charts_dir, "overall_unemployment_trend.png"))
    plt.close()
    
    # Chart 2: Urban vs Rural
    plt.figure(figsize=(10, 5))
    area_trend = df1.groupby(['Date', 'Area'])['Unemployment_Rate'].mean().reset_index()
    sns.lineplot(data=area_trend, x='Date', y='Unemployment_Rate', hue='Area', markers=True, style='Area', palette=['#e67e22', '#2c3e50'])
    plt.axvspan(pd.to_datetime('2020-03-24'), pd.to_datetime('2020-06-30'), color='grey', alpha=0.2, label='Lockdown')
    plt.title("Urban vs Rural Unemployment Trends")
    plt.xlabel("Date")
    plt.ylabel("Unemployment Rate (%)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(charts_dir, "urban_vs_rural_comparison.png"))
    plt.close()
    
    # Chart 3: Lockdown Peak State-wise Impact
    lockdown_data = df2[(df2['Date'] >= '2020-04-01') & (df2['Date'] <= '2020-06-30')]
    states_peak = lockdown_data.groupby('State')['Unemployment_Rate'].mean().sort_values(ascending=False).reset_index()
    
    plt.figure(figsize=(10, 8))
    sns.barplot(data=states_peak, y='State', x='Unemployment_Rate', palette="flare_r", hue='State', legend=False)
    plt.axvline(x=lockdown_data['Unemployment_Rate'].mean(), color='#2c3e50', linestyle='--', label=f"Average ({lockdown_data['Unemployment_Rate'].mean():.1f}%)")
    plt.title("State-wise Unemployment during Lockdown Peak (April-June 2020)")
    plt.xlabel("Unemployment Rate (%)")
    plt.ylabel("State")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(charts_dir, "statewise_unemployment_covid.png"))
    plt.close()
    
    # Chart 4: Zone Trends
    plt.figure(figsize=(10, 5))
    zone_trend = df2.groupby(['Date', 'Zone'])['Unemployment_Rate'].mean().reset_index()
    sns.lineplot(data=zone_trend, x='Date', y='Unemployment_Rate', hue='Zone', marker='o', palette="Set1")
    plt.axvspan(pd.to_datetime('2020-03-24'), pd.to_datetime('2020-06-30'), color='grey', alpha=0.15, label='Lockdown')
    plt.title("Zone-wise Unemployment Trends (2020)")
    plt.xlabel("Date")
    plt.ylabel("Unemployment Rate (%)")
    plt.tight_layout()
    plt.savefig(os.path.join(charts_dir, "zone_unemployment_trend.png"))
    plt.close()
    
    # Chart 5: Correlation
    plt.figure(figsize=(8, 5))
    sns.regplot(data=df2, x='Labour_Participation_Rate', y='Unemployment_Rate', 
                scatter_kws={'alpha':0.6, 'color':'#1abc9c'}, 
                line_kws={'color':'#e74c3c', 'label':'Fit Line'})
    r_val = df2['Labour_Participation_Rate'].corr(df2['Unemployment_Rate'])
    plt.text(48, 65, f'Correlation (r) = {r_val:.2f}', bbox=dict(facecolor='white', alpha=0.8))
    plt.title("Labour Participation vs Unemployment Rate")
    plt.xlabel("Labour Participation Rate (%)")
    plt.ylabel("Unemployment Rate (%)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(charts_dir, "unemployment_vs_participation.png"))
    plt.close()
    
    # Impact Calculations
    print("\n--- COVID-19 Impact Calculations ---")
    pre_lockdown = df2[df2['Date'] < '2020-04-01']['Unemployment_Rate'].mean()
    lockdown_peak = df2[(df2['Date'] >= '2020-04-01') & (df2['Date'] <= '2020-06-30')]['Unemployment_Rate'].mean()
    recovery = df2[df2['Date'] > '2020-06-30']['Unemployment_Rate'].mean()
    
    print(f"Pre-lockdown Avg: {pre_lockdown:.2f}%")
    print(f"Lockdown Peak Avg: {lockdown_peak:.2f}%")
    print(f"Recovery Phase Avg: {recovery:.2f}%")
    print(f"Relative Increase: {((lockdown_peak - pre_lockdown) / pre_lockdown) * 100:.1f}%")
    
    rural_pre = df1[(df1['Date'] < '2020-04-01') & (df1['Area'] == 'Rural')]['Unemployment_Rate'].mean()
    rural_peak = df1[(df1['Date'] >= '2020-04-01') & (df1['Date'] <= '2020-06-30') & (df1['Area'] == 'Rural')]['Unemployment_Rate'].mean()
    urban_pre = df1[(df1['Date'] < '2020-04-01') & (df1['Area'] == 'Urban')]['Unemployment_Rate'].mean()
    urban_peak = df1[(df1['Date'] >= '2020-04-01') & (df1['Date'] <= '2020-06-30') & (df1['Area'] == 'Urban')]['Unemployment_Rate'].mean()
    
    print(f"Rural - Pre-COVID: {rural_pre:.2f}%, Peak: {rural_peak:.2f}%")
    print(f"Urban - Pre-COVID: {urban_pre:.2f}%, Peak: {urban_peak:.2f}%")
    
    print("\n--- 2019 Monthly Average (Baseline) ---")
    m_2019 = df1[df1['Year'] == 2019].groupby('Month_Num')['Unemployment_Rate'].mean()
    m_names = df1[df1['Year'] == 2019].groupby('Month_Num')['Month_Name'].first()
    for m_num, m_name in m_names.items():
        print(f"  {m_name}: {m_2019.get(m_num, 0.0):.2f}%")
        
    print("\nAnalysis completed.")

if __name__ == '__main__':
    main()
