import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split
from tensorflow.keras.optimizers import Adam, SGD, RMSprop
from sklearn.model_selection import ParameterGrid, KFold
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error
from sklearn.covariance import MinCovDet
from math import comb
from scipy import stats


def detec_outliers(hw_matrix, percentil):
    """
    Detecta outliers en una matriz de datos utilizando la distancia de Mahalanobis.

    Args:
        hw_matrix (np.array): Matriz de datos (numpy array) donde se buscan outliers.
        percentil (float): Percentil para determinar el umbral de distancia de Mahalanobis. Por defecto es 95.

    Returns:
        np.array: Índices de los outliers en la matriz.
    """
    mcd = MinCovDet().fit(hw_matrix)
    dist = mcd.mahalanobis(hw_matrix)
    umbral = np.percentile(dist, percentil)
    outliers = np.where(dist > umbral)[0]
    return outliers

def cal_random_probability(m,n, u_):
    C = comb(m+n,m) # CORREGIDO
    u_ += 1

    # Calcula la suma en la fórmula de la probabilidad de aleatoriedad
    sum_f = 0
    for u in range(2, u_):
        if u % 2 == 0:
            k = u // 2
            f_u = 2 * comb(m-1, k-1) * comb(n-1, k-1)
        else:
            k = (u+1) // 2
            f_u = comb(m-1, k-1) * comb(n-1, k-2) + comb(m-1, k-2) * comb(n-1, k-1)
        sum_f += f_u

    # Calcula la probabilidad de aleatoriedad
    p = 1/C * sum_f

    return p

def durbin_watson(residuales):
    diff_residuales = np.diff(residuales)
    numerador = np.sum(diff_residuales ** 2)
    denominador = np.sum(residuales ** 2)
    d = numerador / denominador
    return d

def calculate_dL(residuos, k):
    n = len(residuos)
    alpha = 0.05
    critical_value = stats.f.ppf(1 - alpha/2, k, n - k - 1)
    return 2 - 2 * critical_value

def calculate_dU(residuos, k):
    n = len(residuos)
    alpha = 0.05
    critical_value = stats.f.ppf(alpha/2, k, n - k - 1)
    return 2 - 2 * critical_value


def train_neural_network(X, y, 
                         hidden_layers_config=[(12, 'relu')], 
                         output_neurons=1, 
                         output_activation='linear', 
                         optimizer='adam', 
                         loss='mean_squared_error', 
                         metrics=['mae', 'mse'], 
                         epochs=1000, 
                         test_size=0.2, 
                         random_state=42):
    """
    Entrena una red neuronal personalizada según los parámetros dados.

    Args:
        X (np.array): Datos de entrada (características).
        y (np.array): Datos de salida (objetivo).
        hidden_layers_config (list of tuples): Configuración de capas ocultas en formato (neuronas, activación).
        output_neurons (int): Número de neuronas en la capa de salida.
        output_activation (str): Función de activación para la capa de salida.
        optimizer (str or tf.keras.optimizers.Optimizer): Optimizador a utilizar.
        loss (str): Función de pérdida.
        metrics (list): Métricas de evaluación.
        epochs (int): Número de épocas para el entrenamiento.
        test_size (float): Tamaño del conjunto de prueba.
        random_state (int): Semilla para la división de datos.

    Returns:
        model: Modelo de red neuronal entrenado.
        history: Historia del entrenamiento del modelo.
        test_loss: Pérdida en el conjunto de prueba.
        predictions: Predicciones del modelo en el conjunto de prueba.
    """
    
    # Dividir los datos en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    # Crear el modelo secuencial
    model = Sequential()
    
    # Obtener la dimensión de entrada automáticamente desde los datos
    input_dim = X_train.shape[1] if len(X_train.shape) > 1 else 1

    # Añadir capas ocultas basadas en hidden_layers_config
    for neurons, activation in hidden_layers_config:
        model.add(Dense(neurons, input_dim=input_dim, activation=activation))
        input_dim = None  # Solo especificamos input_dim en la primera capa
    
    # Añadir la capa de salida
    model.add(Dense(output_neurons, activation=output_activation))

    # Configurar el optimizador
    if isinstance(optimizer, str):
        if optimizer == 'adam':
            optimizer = Adam()
        elif optimizer == 'sgd':
            optimizer = SGD()
        elif optimizer == 'rmsprop':
            optimizer = RMSprop()
        else:
            raise ValueError(f"Optimizador '{optimizer}' no es válido. Usa 'adam', 'sgd' o 'rmsprop'.")

    # Compilar el modelo
    model.compile(loss=loss, optimizer=optimizer, metrics=metrics)

    # Entrenar el modelo
    history = model.fit(X_train, y_train, epochs=epochs, validation_data=(X_test, y_test), verbose=0)

    # Evaluar el modelo en el conjunto de prueba
    test_loss = model.evaluate(X_test, y_test, verbose=0)

    # Generar predicciones en el conjunto de prueba
    predictions = model.predict(X_test)
    predictions = np.ravel(predictions)  # Aplanar a una sola dimensión

    return model, history, test_loss, predictions

def train_svr_model(X, y, test_size=0.2, random_state=42, kernel='rbf', C=100, gamma=0.001, epsilon=0.001):
    """
    Entrena un modelo SVR en los datos proporcionados y evalúa su desempeño.

    Parámetros:
    - X: matriz de características independientes
    - y: matriz de características dependientes
    - test_size: proporción de los datos para el conjunto de prueba (default=0.2)
    - random_state: semilla para la división de los datos (default=42)
    - kernel: tipo de kernel para SVR ('linear', 'poly', 'rbf', 'sigmoid')
    - C: parámetro de regularización
    - gamma: coeficiente de kernel ('scale', 'auto', o valor numérico)
    - epsilon: margen en el cual no se penaliza el error

    Retorna:
    - svm_model: modelo SVR entrenado
    - mse: error cuadrático medio en los datos de prueba
    - rmse: raíz del error cuadrático medio
    - y_pred: predicciones del modelo en los datos de prueba
    """

    # División de los datos en entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    # Creación del modelo SVR con los parámetros especificados
    svm_model = SVR(kernel=kernel, C=C, gamma=gamma, epsilon=epsilon)
    
    # Entrenamiento del modelo
    svm_model.fit(X_train, y_train)

    # Predicción en los datos de prueba
    y_pred = svm_model.predict(X_test)

    # Evaluación del modelo
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    
    print('RMSE:', rmse)

    return svm_model, mse, rmse, y_pred

def cross_validate_model(X, y, model_type, param_grid, n_splits=5):
    """
    Realiza validación cruzada en el modelo especificado y devuelve el mejor modelo, los mejores parámetros y el RMSE promedio.
    
    Args:
        X (np.array): Características de entrada.
        y (np.array): Etiquetas de salida.
        model_type (str): Tipo de modelo, 'neural_network' o 'svr'.
        param_grid (dict): Diccionario con los parámetros a probar en la validación cruzada.
        n_splits (int): Número de divisiones para la validación cruzada (default=5).
        
    Returns:
        best_model: Mejor modelo entrenado.
        best_params: Mejor combinación de parámetros.
        best_rmse: RMSE promedio del mejor modelo.
    """
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)
    best_rmse = float('inf')
    best_model = None
    best_params = None
    
    for params in param_grid:
        rmse_scores = []
        
        for train_index, test_index in kf.split(X):
            X_train, X_test = X[train_index], X[test_index]
            y_train, y_test = y[train_index], y[test_index]
            
            # Asegurarse de que y_train e y_test son vectores planos si es necesario
            y_train = y_train.ravel()
            y_test = y_test.ravel()
            
            if model_type == 'neural_network':
                # Llamar a train_neural_network con los parámetros actuales
                model, _, _, predictions = train_neural_network(
                    X_train, y_train,
                    hidden_layers_config=params.get('hidden_layers_config', [(12, 'relu')]),
                    output_neurons=params.get('output_neurons', 1),
                    output_activation=params.get('output_activation', 'linear'),
                    optimizer=params.get('optimizer', 'adam'),
                    loss=params.get('loss', 'mean_squared_error'),
                    metrics=params.get('metrics', ['mae', 'mse']),
                    epochs=params.get('epochs', 1000),
                    test_size=0.2,
                    random_state=42
                )
                
            elif model_type == 'svr':
                # Llamar a train_svr_model con los parámetros actuales
                model, _, rmse, predictions = train_svr_model(
                    X_train, y_train,
                    test_size=0.2,
                    random_state=42,
                    kernel=params.get('kernel', 'rbf'),
                    C=params.get('C', 100),
                    gamma=params.get('gamma', 0.001),
                    epsilon=params.get('epsilon', 0.001)
                )

            # Calcular el RMSE para las predicciones actuales
            rmse = np.sqrt(mean_squared_error(y_test, predictions))
            rmse_scores.append(rmse)
        
        # Calcular el promedio de RMSE para la combinación de parámetros actual
        avg_rmse = np.mean(rmse_scores)
        
        # Actualizar el mejor modelo si el RMSE promedio actual es menor
        if avg_rmse < best_rmse:
            best_rmse = avg_rmse
            best_model = model
            best_params = params

    return best_model, best_params, best_rmse