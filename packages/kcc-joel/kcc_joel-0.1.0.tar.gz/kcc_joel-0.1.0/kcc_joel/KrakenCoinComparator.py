import krakenex
import pandas as pd
import ipywidgets as widgets
from IPython.display import display
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import plotly.express as px
import plotly.graph_objects as go
from kcc_joel.utils import calcular_rsi, calculo_bandas_bollinger

class KrakenCoinComparator:
    def __init__(self):
        self._is_coin_selected=False
        self._kraken = krakenex.API()
        self.data = pd.DataFrame(self._kraken.query_public('AssetPairs')['result']).T
        self.data[['from', 'to']] = self.data['wsname'].str.split('/', expand=True)
        self.possible_from_coins = self.data['from'].unique()
        self.possible_to_coins = self.data['to'].unique()
        self._prepared_data = None
        self._is_data_prepared = False
    
    def is_coin_selected(self):
        return self._is_coin_selected
    
    def get_coins_selected(self):
        if self._is_coin_selected:
            return "Las Monedas seleccionadas son " + self.from_coin + ' y ' + self.to_coin
        else:
            return "Aun no se ha seleccionado una moneda, se debe llamar al método `select_coin`"
    
    def select_coin(self):
        # Crear un dropdown con más configuración visual
        selector = widgets.Dropdown(
            options=self.possible_from_coins,
            description='Elige las dos monedas que quieres comparar:',
            value=self.possible_from_coins[0],  # Valor predeterminado
            disabled=False,      # Habilitar el dropdown
            style={'description_width': 'initial'},  # Ancho de la descripción
            layout=widgets.Layout(width='500px'),  # Ancho del dropdown
        )
        # Crear un dropdown con más configuración visual
        selector2 = widgets.Dropdown(
            options=self.possible_from_coins,
            value='EUR',  # Valor predeterminado
            disabled=False,      # Habilitar el dropdown
            style={'description_width': 'initial'},  # Ancho de la descripción
            layout=widgets.Layout(width='500px'),  # Ancho del dropdown
        )
        self.from_coin = selector.value
        self.to_coin = selector2.value
        self.coin_selected = self.from_coin+self.to_coin

        # Función para manejar el cambio de selección
        def on_select(change):
            self.from_coin = change['new']
            self.coin_selected = self.from_coin+self.to_coin
            self._is_data_prepared = False
            print(f'La moneda {self.from_coin} ha sido seleccionada')

        def on_select2(change):
            self.to_coin = change['new']
            self.coin_selected = self.from_coin+self.to_coin
            self._is_data_prepared = False
            print(f'La moneda {self.to_coin} ha sido seleccionada')

        selector.observe(on_select, names='value')
        selector2.observe(on_select2, names='value')

        # Mostrar el selector
        display(selector)
        display(selector2)
        self._is_coin_selected = True
        self._is_data_prepared = False
    
    def select_coin_from_possible(self):
        possible_data = pd.DataFrame(self._kraken.query_public('AssetPairs')['result']).T['altname']
        # Crear un dropdown con más configuración visual
        selector = widgets.Dropdown(
            options=possible_data,
            description='Elige el par que quieres comparar:',
            value=possible_data.iloc[0],  # Valor predeterminado
            disabled=False,      # Habilitar el dropdown
            style={'description_width': 'initial'},  # Ancho de la descripción
            layout=widgets.Layout(width='500px'),  # Ancho del dropdown
        )
        self.coin_selected = selector.value
        # Función para manejar el cambio de selección
        def on_select(change):
            self.coin_selected = change['new']
            print('La moneda ha sido seleccionada')
            self._is_data_prepared = False

        selector.observe(on_select, names='value')

        # Mostrar el selector
        display(selector)
        
        self._is_coin_selected = True
        self._is_data_prepared = False

    def _calcular_metricas(self, interval, bollinger_delta):
        def aplicar_estrategia_compra(df, columna_objetivo = 'close'):
            if ('Banda_Inferior' in df.columns) & ('count' in df.columns) & ('RSI' in df.columns) & (columna_objetivo in df.columns):
                return ((df[columna_objetivo]<df['Banda_Inferior']) 
                        & (df['count']>1) 
                        & (df['RSI']<30))
            else:
                raise(Exception(f'Falta una columna de las siguientes para calcular la estrategia de compra: Banda_Superior, count, RSI o {columna_objetivo}. Cambia la estrategia de compra o define dichas columnas'))

        def aplicar_estrategia_venta(df, columna_objetivo = 'close'):
            if ('Banda_Superior' in df.columns) & ('count' in df.columns) & ('RSI' in df.columns) & (columna_objetivo in df.columns):
                return ((df[columna_objetivo]>df['Banda_Superior']) 
                        & (df['count']>1) 
                        & (df['RSI']>70))
            else:
                raise(Exception(f'Falta una columna de las siguientes para calcular la estrategia de venta: Banda_Superior, count, RSI o {columna_objetivo}. Cambia la estrategia de venta o define dichas columnas'))

        try:
            print("Haciendo una peticion de la moneda :", self.coin_selected)
            coin_evolution = self._kraken.query_public('OHLC', {'pair': self.coin_selected, 'interval':interval})['result']
            coin_evolution_df = pd.DataFrame(coin_evolution[self.coin_selected], columns=['timestamp', 'open', 'high', 'low', 'close', 'vwap', 'volume', 'count'])
        except:
            self._is_coin_selected = False
            self._is_data_prepared = False
            raise(Exception('Esa combinacion de monedas no está contemplada en Kraken. Prueba otra :D'))

        coin_evolution_df['close'] = coin_evolution_df['close'].astype(float)
        # Convertir el timestamp a formato de fecha
        coin_evolution_df['timestamp'] = pd.to_datetime(coin_evolution_df['timestamp'], unit='s')
        # Configurar el índice del DataFrame como el timestamp
        coin_evolution_df.set_index('timestamp', inplace=True)

        coin_evolution_df['Banda_Superior'], coin_evolution_df['Banda_Inferior'] = calculo_bandas_bollinger(coin_evolution_df, bollinger_delta=bollinger_delta)

        # Calcular el RSI y agregarlo al DataFrame
        coin_evolution_df['RSI'] = calcular_rsi(coin_evolution_df)

        coin_evolution_df['Compra'] = aplicar_estrategia_compra(coin_evolution_df)
        coin_evolution_df['Venta'] = aplicar_estrategia_venta(coin_evolution_df)
        
        coin_evolution_df.dropna(inplace=True)
        self._prepared_data = coin_evolution_df
        self._is_data_prepared = True

    def plot_coin_evolution(self, interval = 30, bollinger_delta = 20):        
        if (not self._is_data_prepared) or (self._prepared_data is None):
            try:
                self._calcular_metricas(interval, bollinger_delta)
            except Exception as e:
                raise e

        # Graficar los precios de cierre (close)
        plt.figure(figsize=(12,6))

        plt.plot(self._prepared_data.index, self._prepared_data['close'], label='Precio de cierre', color='b')

        plt.plot(self._prepared_data.index, self._prepared_data['Banda_Superior'], label='Banda_Superior', color='green', linewidth=0.5)
        plt.plot(self._prepared_data.index, self._prepared_data['Banda_Inferior'], label='Banda_Inferior', color='red', linewidth=0.5)

        # Rellenar el área entre las bandas
        plt.fill_between(self._prepared_data.index, self._prepared_data['Banda_Inferior'], self._prepared_data['Banda_Superior'], color='lightgray')

        plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(20))  # 5 ticks en el eje Y, ajusta según lo que necesites
        # Graficar la banda superior e inferior

        # Obtener los índices donde la columna booleanos es True
        sign_compra = self._prepared_data.index[self._prepared_data['Compra']]
        plt.scatter(sign_compra, self._prepared_data['close'][sign_compra], color='red', s=100, marker='X', label='Señal de Compra')

        # Obtener los índices donde la columna booleanos es True
        sign_venta = self._prepared_data.index[self._prepared_data['Venta']]
        plt.scatter(sign_venta, self._prepared_data['close'][sign_venta], color='green', s=100, marker='o', label='Señal de Venta')

        # Añadir etiquetas y título
        plt.title(f'Histórico de Precios de {self.coin_selected}')
        plt.tick_params(axis='x', rotation=60)
        plt.xlabel('Fecha')
        plt.ylabel('Precio de Cierre')
        plt.legend()
        plt.grid(True)
        plt.show()

def plot_interactive_coin_evolution(self, interval = 30, bollinger_delta = 20):
    if (not self._is_data_prepared) or (self._prepared_data is None):
        try:
            self._calcular_metricas(interval, bollinger_delta)
        except Exception as e:
            raise e

    # Crear la gráfica
    fig = px.line(self._prepared_data, x=self._prepared_data.index, y='close', title='Histórico de Precios')

    # Mostrar la gráfica
    fig.show()