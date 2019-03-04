import numpy as np
import math

NUM_FEATURES = 2  # Todo fix


class ActorCritic:

    def __init__(self, lr, lamb):
        self.lr = np.repeat(lr, 5)  # For each of the arrays in the following order
        self.lamb = np.repeat(lamb, 5)

        # throttle_mu, throttle_sigma, dir_mu, dir_sigma
        self.pol_weights = [np.zeros(sz) for sz in [NUM_FEATURES] * 4]
        self.pol_traces = [np.zeros(sz) for sz in [NUM_FEATURES] * 4]

        self.rbar = 0
        self.val_weights = np.zeros(NUM_FEATURES)
        self.val_trace = np.zeros(NUM_FEATURES)

    def sample_action(self, features):
        """
        Sample the throttle and direction according to our normal distributions
        :param features: Unified feature vector for all approximations
        :return: (throttle, direction)
        """
        t_mu = np.dot(self.pol_weights[0], features)
        t_sigma = math.exp(np.dot(self.pol_weights[1], features))
        throttle = np.random.normal(t_mu, t_sigma, 1)
        d_mu = np.dot(self.pol_weights[2], features)
        d_sigma = math.exp(np.dot(self.pol_weights[3], features))
        direction = np.random.normal(d_mu, d_sigma, 1)
        return throttle, direction

    def estimate_value(self, state):
        return np.dot(self.val_weights, state)

    def update(self, old_state, new_state, reward):
        delta = reward - self.rbar + self.estimate_value(new_state) - self.estimate_value(old_state)  # Loss
        # self.rbar += self.lr[4] * delta
        # self.tm_trace *=


class TD:
    """
    An implementation of emphatic TD(lambda) as provided by Sutton's True Online Emphatic TD(lambda)
    """

    def __init__(self, n, alpha, lamb, gamma=1.0, I=1):
        """

        :param n: Dimensionality of feature vector
        :param I: Initial interest value
        :param alpha: Learning rate
        :param lamb: Lambda value
        :param gamma: Gamma value
        """
        self.ep = np.zeros(n)
        self.gm = gamma
        self.lm = lamb
        self.theta = np.zeros(n)
        self.prevtheta = np.zeros(n)
        self.alpha = alpha
        self.H = 0.0
        self.M = alpha * I  # Emphasis
        self.prevI = I
        self.prevgm = 0
        self.prevlm = 0

    def learn(self, phi, phiPrime, R, rho=1, I=1, prediction=None):
        """
        Learns for a single step

        :param phi: Observation at time t
        :param phiPrime: Observation at time t + 1
        :param R: Single-step reward
        :param rho: Ratio of target / behavior probabilities
        :param I: Interest, i.e. importance of accurately predicting at time t
        :param prediction: Predicted value of phi
        :return:
        """

        # Todo decide how to handle lambda, gamma update or lack thereof

        if prediction is None:
            delta = R + self.gm * self.predict(phiPrime) - self.predict(phi)  # Loss
        else:
            delta = R + self.gm * self.predict(phiPrime) - prediction  # Loss
        self.ep = rho * (self.prevgm * self.prevlm * self.ep + self.M * (1 - rho * self.prevgm * self.prevlm *
                                                                         np.dot(self.ep, phi)) * phi)
        Delta = delta * self.ep + np.dot(self.theta - self.prevtheta, phi) * (self.ep - rho * self.M * phi)
        self.prevtheta = self.theta.copy()
        self.theta += Delta
        self.H = rho * self.gm * (self.H + self.prevI)
        self.M = self.alpha * (I + (1 - self.lm) * self.H)
        self.prevgm = self.gm
        self.prevlm = self.lm
        self.prevI = I

    def predict(self, phi):
        return np.dot(self.theta, phi)

if __name__ == '__main__':
    ac = ActorCritic(1e-2, 0.8)
    feat = np.ones(NUM_FEATURES)
    throttle, direction = ac.sample_action(feat)
    print(throttle)
    print(direction)
