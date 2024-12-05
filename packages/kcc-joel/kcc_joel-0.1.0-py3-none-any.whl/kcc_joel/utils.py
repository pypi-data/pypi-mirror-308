# Funciones extra
def calcular_rsi(data, periodo=14, columna_objetivo = 'close'):
    # Calcular las diferencias de cierre
    cambios = data[columna_objetivo].diff()

    # Separar ganancias y pérdidas
    ganancias = cambios.where(cambios > 0, 0)
    perdidas = -cambios.where(cambios < 0, 0)

    # Calcular promedios de ganancias y pérdidas
    avg_ganancia = ganancias.rolling(window=periodo).mean()
    avg_perdidas = perdidas.rolling(window=periodo).mean()

    # Calcular RS
    rs = avg_ganancia / avg_perdidas

    # Calcular RSI
    rsi = 100 - (100 / (1 + rs))

    return rsi

# Numero de ticks temporales seleccionados para la media de la Banda de Bollinger
def calculo_bandas_bollinger(df, bollinger_delta):
    df['win_mean'] = df['close'].rolling(window=bollinger_delta).mean()
    df['win_std'] = df['close'].rolling(window=bollinger_delta).std()

    return df['win_mean'] + (2 * df['win_std']), df['win_mean'] - (2 * df['win_std'])