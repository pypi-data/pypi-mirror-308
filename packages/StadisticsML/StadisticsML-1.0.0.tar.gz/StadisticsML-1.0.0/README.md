
# StadisticsML

**StadisticsML** is a Python library designed to facilitate the use of machine learning models, specifically neural networks and Support Vector Regression (SVR), with a focus on data prediction and analysis. This library allows users to create customizable models, adjust hyperparameters, and obtain predictions and performance evaluations.

## Features

- **Customizable Neural Network**: Allows the creation of neural networks with multiple layers and activations, specifying the number of epochs and optimization function.
- **SVR**: Implementation of Support Vector Regression, with easy adjustment of parameters like `C`, `gamma`, and `epsilon`.
- **Model Evaluation**: Generates performance metrics such as MSE and RMSE to assess the accuracy of trained models.
- **User-Friendly Interface**: Easy-to-use functions to train models and make predictions on new data.

## Installation

To install the library, use the following `pip` command:

```bash
pip install StadisticsML
```

## Requirements

- `numpy`
- `scipy`
- `scikit-learn`
- `tensorflow`
  
These packages will be installed automatically as dependencies when you install **StadisticsML**.

## Functions

### 1. **Customizable Neural Network** (`train_neural_network`)

This function allows the user to create and train a neural network for regression. The adjustable parameters include:

- **X**: Training input data.
- **y**: Labels or expected outcomes.
- **hidden_layers_config**: Configuration of the hidden layers with the number of neurons and activation functions.
- **output_neurons**: Number of neurons in the output layer.
- **output_activation**: Activation function for the output layer.
- **optimizer**: Optimizer to use (e.g., `adam`, `sgd`).
- **loss**: Loss function to use (e.g., `mean_squared_error`).
- **metrics**: Additional metrics for model evaluation (e.g., `mae`, `mse`).
- **epochs**: Number of training epochs.
- **test_size**: Percentage of data allocated for testing.
- **random_state**: Seed for randomization.

### Example:

```python
from StadisticsML import train_neural_network

# Example data
X = [[1], [2], [3], [4], [5]]
y = [1.1, 2.0, 2.9, 4.0, 5.1]

# Hidden layers configuration: [(neurons, activation function)]
hidden_layers_config = [(12, 'relu'), (8, 'relu')]

# Train the neural network
model, history, test_loss, predictions = train_neural_network(
    X=X, y=y, 
    hidden_layers_config=hidden_layers_config,
    epochs=100,
    test_size=0.2,
    random_state=42
)

print("Predictions:", predictions)
print("Test Loss:", test_loss)
```

### 2. **Support Vector Regression (SVR)** (`train_svr`)

This function trains a support vector regression model using customizable parameters.

- **X**: Training input data.
- **y**: Labels or expected outcomes.
- **C**: Penalty parameter.
- **gamma**: Kernel function coefficient.
- **epsilon**: Tolerance margin.
- **test_size**: Percentage of data allocated for testing.

### Example:

```python
from StadisticsML import train_svr

# Example data
X = [[1], [2], [3], [4], [5]]
y = [1.1, 2.0, 2.9, 4.0, 5.1]

# Train the SVR model
mse, rmse, predictions = train_svr(X=X, y=y, C=100, gamma=0.001, epsilon=0.001, test_size=0.2)

print("SVR Predictions:", predictions)
print("RMSE:", rmse)
```

### 3. **Cross-Validation for Model Optimization** (`cross_validate_model`)

This function allows the user to perform cross-validation for optimizing the hyperparameters of a neural network or SVR model.

- **model_type**: Choose between `'nn'` (neural network) or `'svr'` (Support Vector Regression).
- **X**: Input data for training.
- **y**: Expected outcomes.
- **hyperparameters**: A dictionary of hyperparameters to tune, such as `C`, `gamma`, `epochs`, etc.
- **cv_folds**: Number of cross-validation folds.
- **random_state**: Seed for reproducibility.

### Example:

```python
from StadisticsML import cross_validate_model

# Example data
X = [[1], [2], [3], [4], [5]]
y = [1.1, 2.0, 2.9, 4.0, 5.1]

# Hyperparameters to tune
hyperparameters = {'C': [0.1, 1, 10], 'gamma': [0.001, 0.01, 0.1]}

# Perform cross-validation for SVR
best_params, mean_score = cross_validate_model(
    model_type='svr', X=X, y=y, hyperparameters=hyperparameters, cv_folds=5, random_state=42
)

print("Best parameters:", best_params)
print("Mean score from cross-validation:", mean_score)
```

## Contribution

If you want to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/new-feature`).
3. Make your changes and commit them (`git commit -am 'Add new feature'`).
4. Push the branch (`git push origin feature/new-feature`).
5. Open a pull request.

**Expected Contribution:** Implementation of additional machine learning models.

## License

This project is licensed under the **MIT** License. For more details, please refer to the [LICENSE](LICENSE) file.

## Contact

- **Author**: Jorge Eduardo Londoño Arango
- **Email**: [joelondonoar@unal.edu.co](mailto:joelondonoar@unal.edu.co) - [jorge.nebulanoir@gmail.com](mailto:jorge.nebulanoir@gmail.com)
