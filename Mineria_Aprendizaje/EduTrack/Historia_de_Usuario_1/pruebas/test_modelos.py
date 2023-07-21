import sys
import os
import unittest
from sklearn.tree import DecisionTreeClassifier

# Agregar la ruta del directorio "codigo_fuente" al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'codigo_fuente')))

from modelos import entrenar_modelo, predecir, evaluar_modelo

class TestModelos(unittest.TestCase):
    def test_entrenar_modelo(self):
        # Caso de prueba 1: Verificar si el modelo se entrena correctamente
        X = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        y = [0, 1, 0]

        modelo = entrenar_modelo(X, y)
        self.assertIsNotNone(modelo)

    def test_predecir(self):
        # Caso de prueba 2: Verificar si se realizan predicciones correctamente
        modelo = DecisionTreeClassifier()
        modelo.fit([[1, 2, 3], [4, 5, 6], [7, 8, 9]], [0, 1, 0])
        X = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        y_predicciones = predecir(modelo, X).tolist()  # Convertir el array en una lista
        self.assertEqual(y_predicciones, [0, 1, 0])

    def test_entrenar_modelo_no_datos_vacios(self):
        # Caso de prueba 3: Verificar si no se pueden entrenar modelos con datos vacíos
        X_empty = []
        y_empty = []
        with self.assertRaises(ValueError):
            entrenar_modelo(X_empty, y_empty)

    def test_evaluar_modelo_no_modelo_vacio(self):
        # Caso de prueba 4: Verificar si no se puede evaluar el rendimiento de un modelo vacío
        modelo = DecisionTreeClassifier()
        X = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        y = [0, 1, 0]
        with self.assertRaises(ValueError):
            evaluar_modelo(modelo, X, y)


if __name__ == '__main__':
    unittest.main()
