import numpy as np


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
