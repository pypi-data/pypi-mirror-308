import unittest
import numpy as np
from kalmanfilterByRuhail.extended import ExtendedKalmanFilter

class TestExtendedKalmanFilter(unittest.TestCase):
    def setUp(self):
        F = np.eye(2)
        H = np.array([[1, 0]])
        Q = np.eye(2) * 0.01
        R = np.array([[1]])
        P = np.eye(2)
        x = np.array([[0.5], [1]])
        
        def f(x):
            return np.array([[x[0, 0] + x[1, 0]], [x[1, 0]]])

        def h(x):
            return np.array([[x[0, 0]**2]])

        def F_jacobian(x):
            return np.eye(2)

        def H_jacobian(x):
            return np.array([[2 * x[0, 0], 0]])
        
        self.ekf = ExtendedKalmanFilter(F, H, Q, R, P, x, f, h, F_jacobian, H_jacobian)

    def test_initialization(self):
        self.assertIsInstance(self.ekf, ExtendedKalmanFilter)

if __name__ == "__main__":
    unittest.main()
