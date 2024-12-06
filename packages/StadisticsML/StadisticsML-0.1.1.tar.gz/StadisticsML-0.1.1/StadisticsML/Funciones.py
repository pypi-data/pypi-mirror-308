import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from keras.layers import Dense, Input
from sklearn.model_selection import train_test_split
from tensorflow.keras.optimizers import Adam, SGD, RMSprop
from sklearn.model_selection import ParameterGrid, KFold
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error
from sklearn.covariance import MinCovDet
from math import comb
from scipy import stats
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error
from keras.wrappers.scikit_learn import KerasRegressor  # Asegúrate de importar esto


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

# Función de creación del modelo de red neuronal
def create_model(neurons, hidden_layers, optimizer, n_features=3):
    model = Sequential()
    
    # Usamos Input como la primera capa para especificar la forma de entrada
    model.add(Input(shape=(n_features,)))  # Capa de entrada
    
    # Agregar capas ocultas
    for _ in range(hidden_layers):
        model.add(Dense(neurons, activation='relu'))
    
    # Capa de salida
    model.add(Dense(1, activation='linear'))
    
    # Seleccionar optimizador
    if optimizer == 'adam':
        opt = 'adam'
    else:
        opt = 'sgd'
    
    model.compile(loss='mean_squared_error',
                  optimizer=opt,
                  metrics=['mae', 'mse'])
    return model

# Función de optimización de modelo con GridSearchCV
def optimize_model(X, y, model_type='NN', param_grid=None, cv_folds=3):
    if model_type == 'NN':
        model = KerasRegressor(model=create_model, verbose=0)
    elif model_type == 'SVR':
        model = SVR()
    else:
        raise ValueError("Modelo no soportado. Utiliza 'NN' o 'SVR'.")

    # Configuración de validación cruzada
    kfold = KFold(n_splits=cv_folds)

    # Convertir y a un vector unidimensional (para evitar el warning)
    y = y.ravel()

    # Ejecución de GridSearchCV con los hiperparámetros
    grid = GridSearchCV(estimator=model, param_grid=param_grid, cv=kfold, verbose=1)
    grid_result = grid.fit(X, y)

    # Resultados del modelo
    best_model = grid_result.best_estimator_
    best_score = grid_result.best_score_
    print(f"Mejor modelo: {best_model} con score: {best_score}")

    return best_model, best_score