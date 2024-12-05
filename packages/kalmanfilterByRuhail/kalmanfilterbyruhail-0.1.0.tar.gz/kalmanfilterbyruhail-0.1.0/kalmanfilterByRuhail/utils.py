def initialize_kalman(dim, process_noise, measurement_noise):
    """
    Helper to initialize a Kalman Filter with identity matrices.
    dim: State dimension
    process_noise: Variance of process noise
    measurement_noise: Variance of measurement noise
    """
    F = np.eye(dim)
    H = np.eye(dim)
    Q = np.eye(dim) * process_noise
    R = np.eye(dim) * measurement_noise
    P = np.eye(dim)
    x = np.zeros((dim, 1))
    return KalmanFilter(F, H, Q, R, P, x)
