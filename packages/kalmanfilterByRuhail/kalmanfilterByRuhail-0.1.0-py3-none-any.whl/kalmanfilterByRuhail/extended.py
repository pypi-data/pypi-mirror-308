class ExtendedKalmanFilter(KalmanFilter):
    def __init__(self, F, H, Q, R, P, x, f, h, F_jacobian, H_jacobian):
        """
        Extended Kalman Filter with nonlinear dynamics.
        f: Nonlinear state transition function
        h: Nonlinear measurement function
        F_jacobian: Function to compute Jacobian of F
        H_jacobian: Function to compute Jacobian of H
        """
        super().__init__(F, H, Q, R, P, x)
        self.f = f
        self.h = h
        self.F_jacobian = F_jacobian
        self.H_jacobian = H_jacobian

    def predict(self):
        """Predict the next state using nonlinear dynamics."""
        self.x = self.f(self.x)
        self.F = self.F_jacobian(self.x)  # Update Jacobian
        self.P = np.dot(np.dot(self.F, self.P), self.F.T) + self.Q

    def update(self, z):
        """Update the state using nonlinear measurements."""
        H = self.H_jacobian(self.x)  # Update Jacobian
        y = z - self.h(self.x)  # Measurement residual
        S = np.dot(H, np.dot(self.P, H.T)) + self.R
        K = np.dot(np.dot(self.P, H.T), np.linalg.inv(S))
        
        self.x = self.x + np.dot(K, y)
        I = np.eye(self.P.shape[0])
        self.P = np.dot(I - np.dot(K, H), self.P)
