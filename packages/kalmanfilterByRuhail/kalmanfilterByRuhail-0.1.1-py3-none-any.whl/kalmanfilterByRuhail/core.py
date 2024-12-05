import numpy as np

class KalmanFilter:
    def __init__(self, F, H, Q, R, P, x):
        """
        Initialize the Kalman Filter.
        F: State transition matrix
        H: Measurement matrix
        Q: Process noise covariance
        R: Measurement noise covariance
        P: Estimate error covariance
        x: Initial state estimate
        """
        self.F = F
        self.H = H
        self.Q = Q
        self.R = R
        self.P = P
        self.x = x

    def predict(self):
        """Predict the next state and error covariance."""
        self.x = np.dot(self.F, self.x)
        self.P = np.dot(np.dot(self.F, self.P), self.F.T) + self.Q

    def update(self, z):
        """
        Update the state based on a measurement.
        z: Measurement vector
        """
        y = z - np.dot(self.H, self.x)  # Measurement residual
        S = np.dot(self.H, np.dot(self.P, self.H.T)) + self.R  # Residual covariance
        K = np.dot(np.dot(self.P, self.H.T), np.linalg.inv(S))  # Kalman gain
        
        self.x = self.x + np.dot(K, y)  # Updated state estimate
        I = np.eye(self.P.shape[0])  # Identity matrix
        self.P = np.dot(I - np.dot(K, self.H), self.P)  # Updated error covariance

    def get_state(self):
        """Return the current state estimate."""
        return self.x
