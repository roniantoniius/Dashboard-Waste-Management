import dash
import sqlite3
import pandas as pd
from dash import dcc
from dash import html
from pyforest import *
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output


BS = "https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/litera/bootstrap.min.css"

app    = dash.Dash(__name__, external_stylesheets=[BS])
server = app.server

# database
conn_sqlite = sqlite3.connect('datawarehouse.db')
df          = pd.read_sql("SELECT * FROM municipal_waste_management", conn_sqlite)
conn_sqlite.close()

# KPIs
total_waste_collected         = df['la_collected_waste'].sum() + df['household_waste_arisings'].sum()
recycling_rate                = (df['household_waste_dry_recycling_composting'].sum() / df['la_collected_waste'].sum()) * 100
average_energy_recovery_rate  = df['la_energy_recovery_rate'].mean()
average_landfill_rate         = df['household_waste_landfill_rate'].mean()
average_waste_per_household   = df['household_waste_arisings_per_household'].mean()


# Visualiasi Baris Pertama
df_donut_a3         = df[["la_dry_recycling", "la_composting", "la_landfilled"]].sum().reset_index()
df_donut_a3.columns = ["kategori", "jumlah"]

df_stack_a4  = df[["year", "la_landfilled", "biodegradable_la_waste_to_landfill"]].groupby("year").sum().reset_index()

fig_donut_a3 = px.pie(df_donut_a3,
                      values='jumlah',
                      names='kategori', 
                      title='Proporsi Sampah Kota yang Didaur Ulang, Dikompos, dan Ditimbun per Tahun',
                      hover_name='kategori')

fig_stack_a4 = px.bar(df_stack_a4,
                      x='year',
                      y=['la_landfilled', 'biodegradable_la_waste_to_landfill'], 
                      title='Sampah Kota yang Ditimbun dan yang Terurai ke TPA 2006 - 2023',
                      labels={'year': 'Tahun', 'value': 'Jumlah Sampah (ton)'})


# Visualiasi Baris Kedua
energy_recovery_df_a5     = df[['year', 'la_energy_recovery_mixed', 'la_energy_recovery_specific']]

energy_recovery_melted_a5 = energy_recovery_df_a5.melt(id_vars='year',
                                                       var_name='energy_recovery_type',
                                                       value_name='energy_recovery_amount')

fig_line_energy_a5    = px.line(energy_recovery_melted_a5,
                                x='year',
                                y='energy_recovery_amount',
                                color='energy_recovery_type', 
                                title='Pemulihan Energi dari Sampah Kota dan TPA 2006 - 2023',
                                labels={'year': 'Tahun', 'energy_recovery_amount': 'Jumlah Energy Recovery'})

fig_scatter_energy_a6 = px.scatter(df,
                                   x='la_energy_recovery_rate',
                                   y='la_preparing_for_reuse', 
                                   title='Tingkat Pemulihan Energi vs Limbah/Sampah yang Dipulihkan',
                                   labels={'la_energy_recovery_rate': 'Tingkat Energy Recovery (%)', 'la_preparing_for_reuse': 'Sampah yang Dipulihkan (ton)'})

# Visualiasi Baris Ketiga
area_rates_a1     = df.groupby('area_name')['la_energy_recovery_rate'].mean().reset_index()
population_a2     = df['population']
num_households_a2 = df['num_households']

fig_bar_area_rates_a1 = px.bar(area_rates_a1.sort_values('la_energy_recovery_rate',
                                                         ascending=False).head(10),
                                                         x='area_name',
                                                         y='la_energy_recovery_rate')

fig_bar_area_rates_a1.update_layout(
    title='Top 10 Wilayah berdasarkan Tingkat Pemulihan Energi',
    xaxis_title='Wilayah',
    yaxis_title='Tingkat Pemulihan Energi (%)',
)

z = np.polyfit(population_a2, num_households_a2, 1)
p = np.poly1d(z)

fig_scatter_population_num_households_a2 = px.scatter(x=population_a2, y=num_households_a2)

fig_scatter_population_num_households_a2.add_trace(go.Scatter(x=population_a2,
                                                              y=p(population_a2),
                                                              mode='lines',
                                                              name='Trendline'))

fig_scatter_population_num_households_a2.update_layout(
    title='Hubungan antara Populasi dan Jumlah Rumah Tangga',
    xaxis_title='Populasi',
    yaxis_title='Jumlah Rumah Tangga',
)

# Membuat visualisasi baris Keempat
la_dry_recycling_composting_rate_a1 = df['la_dry_recycling_composting_rate']
waste_mgmt_group_a1                 = df['waste_mgmt_group']

la_energy_recovery_rate_a2          = df['la_energy_recovery_rate']
waste_mgmt_group_a2                 = df['waste_mgmt_group']

fig_bar_la_dry_recycling_composting_rate_a1 = px.bar(x=waste_mgmt_group_a1,
                                                     y=la_dry_recycling_composting_rate_a1,
                                                     color_discrete_sequence=px.colors.sequential.Viridis)

fig_bar_la_dry_recycling_composting_rate_a1.update_layout(
    title='Perbandingan Tingkat Daur Ulang Sampah Kota Berdasarkan Komunitas Pengelola Sampah',
    xaxis_title='Komunitas Pengelola Sampah',
    yaxis_title='Tingkat Daur Ulang Sampah Kota',
)

fig_violin_la_energy_recovery_rate_a2 = px.violin(x=waste_mgmt_group_a2,
                                                  y=la_energy_recovery_rate_a2,
                                                  box=True,
                                                  hover_name=waste_mgmt_group_a2,
                                                  hover_data=[la_energy_recovery_rate_a2])

fig_violin_la_energy_recovery_rate_a2.update_layout(
    title='Distribusi Tingkat Pemulihan Energi berdasarkan Komunitas Pengelola Sampah',
    xaxis_title='Komunitas Pengelola Sampah',
    yaxis_title='Tingkat Pemulihan Energi',
)


# Membuat visualisasi baris Kelima
quarter_code_a1             = df['quarter_code']
la_collected_waste_a1       = df['la_collected_waste']
area_name_a2                = df['area_name']
household_waste_arisings_a2 = df['household_waste_arisings']

top_10_areas_a2 = df.groupby('area_name')['household_waste_arisings'].sum().nlargest(3).reset_index()

fig_bar_total_waste_collection_a1 = px.bar(x=quarter_code_a1, y=la_collected_waste_a1, color_discrete_sequence=px.colors.sequential.Viridis)
fig_bar_total_waste_collection_a1.update_layout(
    title='Total Pengumpulan Sampah per Kuartal/Triwulan',
    xaxis_title='Kode Kuartal/Triwulan',
    yaxis_title='Total Sampah Dikumpulkan',
)

fig_bar_area_wise_waste_generation_a2 = px.bar(x=top_10_areas_a2['area_name'], y=top_10_areas_a2['household_waste_arisings'], color_discrete_sequence=px.colors.sequential.Viridis)
fig_bar_area_wise_waste_generation_a2.update_layout(
    title='Top 10 Timbulan Sampah Berdasarkan Wilayah',
    xaxis_title='Nama Wilayah',
    yaxis_title='Total Sampah yang Dihasilkan',
)

# Membuat visualisasi baris Keenam
quarter_code_a1                     = df['quarter_code']
la_dry_recycling_composting_rate_a1 = df['la_dry_recycling_composting_rate']
waste_mgmt_group_a3                 = df['waste_mgmt_group']
la_energy_recovery_rate_a3          = df['la_energy_recovery_rate']
mean_energy_recovery_rate_a3        = df.groupby('waste_mgmt_group')['la_energy_recovery_rate'].mean().reset_index()
df['waste_per_capita_a1']           = df['household_waste_arisings_per_capita']
df['waste_per_household_a2']        = df['household_waste_arisings_per_household']
top_10_area                         = df['area_name'].value_counts().head(10).index

fig_bar_waste_per_capita_a1 = px.bar(df[df['area_name'].isin(top_10_area)],
                                     x='area_name', 
                                     y='waste_per_capita_a1',
                                     title='Timbulan Sampah per Kapita',
                                     labels={'area_name': 'Wilayah', 'waste_per_capita_a1': 'Sampah per Kapita'},
                                     template='plotly_white')

fig_bar_waste_per_capita_a1.update_layout(xaxis_title='Wilayah', yaxis_title='Sampah per Kapita')
fig_bar_waste_per_capita_a1.update_xaxes(tickangle=90)

fig_bar_waste_per_household_a2 = px.bar(df[df['area_name'].isin(top_10_area)],
                                        x='area_name', 
                                        y='waste_per_household_a2',
                                        title='Timbulan Sampah per Rumah Tangga',
                                        labels={'area_name': 'Wilayah', 'waste_per_household_a2': 'Sampah per Rumah Tangga'},
                                        template='plotly_white')

fig_bar_waste_per_household_a2.update_layout(xaxis_title='Wilayah', yaxis_title='Sampah per Rumah Tangga')
fig_bar_waste_per_household_a2.update_xaxes(tickangle=90)

app.title = 'Waste Management Statistics'

app.layout = html.Div(
    html.Div([
        html.Div(
            [
                html.H1(
                    'Waste Management Statistics',
                    style={
                        'fontSize': 40,
                        'textAlign': 'center',
                        'padding': '20px',
                        'padding-top': '40px',
                        'padding-bottom': '40px',
                        'color': '#02340f',
                        'margin-left': 'auto',
                        'margin-right': 'auto'
                    },
                    className='eight columns'),

            ], className="row"
        ),
        dbc.Row([
            dbc.Col(html.Div(
                dbc.Alert("Total Sampah yang Dikumpulkan: {0:,.0f} tons".format(total_waste_collected),
                          color='#00FF92', style={'fontWeight': 'bold', 'borderRadius': '10px', 'color': '#0B1D26', 'fontSize': '16px'})), width=2),

            dbc.Col(html.Div(
                dbc.Alert("Tingkat Daur Ulang: {0:.2f}%".format(recycling_rate),
                          color='#00FF92', style={'fontWeight': 'bold', 'borderRadius': '10px', 'color': '#0B1D26', 'fontSize': '18px'})), width=2),

            dbc.Col(html.Div(
                dbc.Alert("Rata2 Tingkat Pemulihan Energi: {0:.2f}%".format(average_energy_recovery_rate),
                          color='#00FF92', style={'fontWeight': 'bold', 'borderRadius': '10px', 'color': '#0B1D26', 'fontSize': '15px'})), width=2),

            dbc.Col(html.Div(
                dbc.Alert("Avg Landfill Rate: {0:.2f}%".format(average_landfill_rate),
                          color='#00FF92', style={'fontWeight': 'bold', 'borderRadius': '10px', 'color': '#0B1D26', 'fontSize': '18px'})), width=2),

            dbc.Col(html.Div(
                dbc.Alert("Rata2 Sampah per Rumah Tangga: {0:.2f} kg".format(average_waste_per_household),
                          color='#00FF92', style={'fontWeight': 'bold', 'borderRadius': '10px', 'color': '#0B1D26', 'fontSize': '15px'})), width=2),

        ], align="center", justify="center"),


        html.Div([
            html.H4('Proporsi Sampah Kota dan Sampah yang Ditimbun', style={'textAlign': 'center'}),
            dbc.Row([
                dbc.Col(dcc.Graph(id='donut-proporsi-a3', figure=fig_donut_a3), width=6),
                dbc.Col(dcc.Graph(id='stack-sampah-a4', figure=fig_stack_a4), width=6),
            ], className="row", style={'border-radius': '15px', 'backgroundColor': '#f8f9fa', 
                                      'box-shadow' : '4px 4px 2.5px #dddddd',
                                      'padding':'20px', 'margin-left':'auto','margin-right':'auto', 'margin-top':'25px'} ),
        ], style={'padding': '20px'}),

        html.Div([
            html.H4('Energy Recovery dari Sampah Kota dan Hubungannya dengan Sampah yang Dipulihkan', style={'textAlign': 'center'}),
            dbc.Row([
                dbc.Col(dcc.Graph(id='line-energy-recovery-a5', figure=fig_line_energy_a5), width=6),
                dbc.Col(dcc.Graph(id='scatter-energy-recovery-a6', figure=fig_scatter_energy_a6), width=6),
            ], className="row", style={'border-radius': '15px', 'backgroundColor': '#f8f9fa', 
                                      'box-shadow' : '4px 4px 2.5px #dddddd',
                                      'padding':'20px', 'margin-left':'auto','margin-right':'auto', 'margin-top':'25px'} ),
        ], style={'padding': '20px'}),

        html.Div([
            html.H4('Tingkat Pemulihan Energi Area dan Dinamika Populasi', style={'textAlign': 'center'}),
            dbc.Row([
                dbc.Col(dcc.Graph(id='bar-area-rates-a1', figure=fig_bar_area_rates_a1), width=6),
                dbc.Col(dcc.Graph(id='scatter-population-num-households-a2', figure=fig_scatter_population_num_households_a2), width=6),
            ], className="row", style={'border-radius': '15px', 'backgroundColor': '#f8f9fa', 
                                    'box-shadow' : '4px 4px 2.5px #dddddd',
                                    'padding':'20px', 'margin-left':'auto','margin-right':'auto', 'margin-top':'25px'} ),

        ], style={'padding': '20px'}),

        html.Div([
            html.H4('Perbandingan Komunitas Pengelolaan Sampah', style={'textAlign': 'center'}),
            dbc.Row([
                dbc.Col(dcc.Graph(id='bar-la-dry-recycling-composting-rate-a1', figure=fig_bar_la_dry_recycling_composting_rate_a1), width=6),
                dbc.Col(dcc.Graph(id='violin-la-energy-recovery-rate-a2', figure=fig_violin_la_energy_recovery_rate_a2), width=6),
            ], className="row", style={'border-radius': '15px', 'backgroundColor': '#f8f9fa', 
                                    'box-shadow' : '4px 4px 2.5px #dddddd',
                                    'padding':'20px', 'margin-left':'auto','margin-right':'auto', 'margin-top':'25px'} ),

        ], style={'padding': '20px'}),

        html.Div([
            html.H4('Tren Pengumpulan dan Produksi Sampah', style={'textAlign': 'center'}),
            dbc.Row([
                dbc.Col(dcc.Graph(id='bar-total-waste-collection-a1', figure=fig_bar_total_waste_collection_a1), width=6),
                dbc.Col(dcc.Graph(id='bar-area-wise-waste-generation-a2', figure=fig_bar_area_wise_waste_generation_a2), width=6),
            ], className="row", style={'border-radius': '15px', 'backgroundColor': '#f8f9fa', 
                                    'box-shadow' : '4px 4px 2.5px #dddddd',
                                    'padding':'20px', 'margin-left':'auto','margin-right':'auto', 'margin-top':'25px'} ),

        ], style={'padding': '20px'}),

        html.Div([
            html.H4('Tingkat Daur Ulang dan Tingkat Pemulihan Energi', style={'textAlign': 'center'}),
            dbc.Row([
                dbc.Col(dcc.Graph(id='bar-recycling-rate-a1', figure={
                    'data': [
                        {'x': quarter_code_a1, 'y': la_dry_recycling_composting_rate_a1, 'type': 'bar'}
                    ],
                    'layout': {
                        'title': 'Recycling Rate by Quarter',
                        'xaxis': {'title': 'Quarter Code'},
                        'yaxis': {'title': 'Recycling Rate'}
                    }
                }), width=6),
                dbc.Col(dcc.Graph(id='bar-energy-recovery-rate-a3', figure={
                    'data': [
                        {'x': mean_energy_recovery_rate_a3['waste_mgmt_group'], 'y': mean_energy_recovery_rate_a3['la_energy_recovery_rate'], 'type': 'bar'}
                    ],
                    'layout': {
                        'title': 'Tingkat Pemulihan Energi berdasarkan Komunitas Pengelola Sampah',
                        'xaxis': {'title': 'Komunitas Pengelola Sampah'},
                        'yaxis': {'title': 'Tingkat Pemulihan Energi'}
                    }
                }), width=6),
            ], className="row", style={'border-radius': '10px', 'backgroundColor': '#f8f9fa', 
                                    'box-shadow' : '4px 4px 2.5px #dddddd',
                                    'padding':'20px', 'margin-left':'auto','margin-right':'auto', 'margin-top':'25px'} ),
        ], style={'padding': '20px'}),

        html.Div([
            html.H4('Metrik Timbulan/Kumpulan Sampah berdasarkan Wilayah', style={'textAlign': 'center'}),
            dbc.Row([
                dbc.Col(dcc.Graph(id='bar-waste-per-capita-a1', figure=fig_bar_waste_per_capita_a1), width=6),
                dbc.Col(dcc.Graph(id='bar-waste-per-household-a2', figure=fig_bar_waste_per_household_a2), width=6),
            ], className="row", style={'border-radius': '15px', 
                                        'backgroundColor': '#f8f9fa', 
                                        'box-shadow': '4px 4px 2.5px #dddddd',
                                        'padding': '20px', 'margin-left': 'auto', 'margin-right': 'auto', 'margin-top': '25px'}),
        ], style={'padding': '20px'})

    ])
)

if __name__ == '__main__':
    app.run_server(debug=True)