import matplotlib.pyplot as plt

def plot_results(true_states, estimates):
    """Plot true states vs. Kalman Filter estimates."""
    plt.plot(true_states, label='True State')
    plt.plot(estimates, label='Kalman Estimate')
    plt.legend()
    plt.xlabel('Time Steps')
    plt.ylabel('State Value')
    plt.title('Kalman Filter Performance')
    plt.show()
