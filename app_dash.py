import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc

# Cria a aplicação Dash
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Carrega o arquivo CSV
df = pd.read_csv('monsters.csv')

# Layout da aplicação
app.layout = dbc.Container([
    html.H1("Visualização de Monstros - Monster Hunter"),
    
    dbc.Row([
        dbc.Col(html.Div("Selecione o gráfico que deseja visualizar:")),
    ], className="mb-4"),

    dcc.RadioItems(
        id='graph-choice',
        options=[
            {'label': 'Resistências Elementares', 'value': 'elemental'},
            {'label': 'Comparação Corte vs Contusão', 'value': 'damage'}
        ],
        value='elemental',
        labelStyle={'display': 'inline-block'}
    ),
    
    dbc.Row([
        dbc.Col(dcc.Graph(id='graph-output'), width=12),
    ]),
])

# Função de callback para atualizar o gráfico com base na escolha do usuário
@app.callback(
    Output('graph-output', 'figure'),
    Input('graph-choice', 'value')
)
def update_graph(selected_graph):
    if selected_graph == 'elemental':
        # Gráfico de resistências elementares
        elemental_columns = ['fogo', 'agua', 'gelo', 'trovao', 'dragao']
        df_elemental = df.melt(id_vars=['name', 'part'], value_vars=elemental_columns, 
                               var_name='Elemento', value_name='Resistência')

        fig = px.bar(df_elemental, x='part', y='Resistência', color='Elemento',
                     title="Resistências Elementares por Parte do Monstro")
        fig.update_layout(xaxis_title='Parte do Monstro', yaxis_title='Resistência')
    elif selected_graph == 'damage':
        # Gráfico comparativo de corte vs contusão
        fig = px.scatter(df, x='corte', y='contusao', color='part',
                         title="Comparação entre Corte e Contusão por Parte do Monstro")
        fig.update_layout(xaxis_title='Dano por Corte', yaxis_title='Dano por Contusão')

    return fig

# Executa o servidor
if __name__ == '__main__':
    app.run_server(debug=True)

