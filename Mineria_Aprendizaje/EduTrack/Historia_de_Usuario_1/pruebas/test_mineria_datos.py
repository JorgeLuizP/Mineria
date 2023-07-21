import unittest
import sys
import os
import pandas as pd
import numpy as np

# Agregar la ruta del directorio "codigo_fuente" al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'codigo_fuente')))

from mineria_datos import obtener_datos


class TestMineriaDatos(unittest.TestCase):
    def test_obtener_datos(self):
        # Caso de prueba 1: Verificar si se obtienen los datos correctamente
        X, y, _ = obtener_datos()
        self.assertIsNotNone(X)
        self.assertIsNotNone(y)
        self.assertIsInstance(X, pd.DataFrame)
        self.assertIsInstance(y, pd.Series)
        self.assertGreater(len(X), 0)
        self.assertGreater(len(y), 0)

    def test_obtener_datos_columnas_correctas(self):
        # Caso de prueba 2: Verificar si los datos obtenidos tienen las columnas correctas
        columnas_esperadas = ['id', 'name', 'age', 'grade', 'average_grade']
        _, _, columnas_obtenidas = obtener_datos()
        self.assertEqual(columnas_obtenidas, columnas_esperadas)

    def test_obtener_datos_tipos_correctos(self):
        # Caso de prueba 3: Verificar si los tipos de datos son correctos
        X, y, _ = obtener_datos()
        X_numeric = X.select_dtypes(include=[np.number])
        self.assertTrue(all(np.issubdtype(dtype, np.number) for dtype in X_numeric.dtypes))

    def test_obtener_datos_valores_no_nulos(self):
        # Caso de prueba 4: Verificar si no hay valores nulos en los datos
        X, y, _ = obtener_datos()
        self.assertFalse(X.isnull().values.any())
        self.assertFalse(y.isnull().values.any())


if __name__ == '__main__':
    unittest.main()
