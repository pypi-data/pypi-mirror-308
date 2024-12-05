import unittest
import numpy as np
from kalmanfilterByRuhail.core import KalmanFilter

class TestKalmanFilter(unittest.TestCase):
    def setUp(self):
        self.F = np.array([[1]])
        self.H = np.array([[1]])
        self.Q = np.array([[0.1]])
        self.R = np.array([[0.5]])
        self.P = np.array([[1]])
        self.x = np.array([[0]])
        self.kf = KalmanFilter(self.F, self.H, self.Q, self.R, self.P, self.x)

    def test_initialization(self):
        self.assertIsInstance(self.kf, KalmanFilter)

    def test_predict(self):
        self.kf.predict()
        self.assertEqual(self.kf.x.shape, (1, 1))

    def test_update(self):
        self.kf.update(np.array([[1]]))
        self.assertEqual(self.kf.x.shape, (1, 1))

if __name__ == "__main__":
    unittest.main()
