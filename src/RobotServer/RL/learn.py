import numpy as np
import math

class ActorCritic:

    def __init__(self, lr, lamb, num_features):
        self.lr = lr  # For each of the arrays in the following order
        self.lamb = lamb

        # throttle_mu, throttle_sigma, dir_mu, dir_sigma
        self.pol_weights = [np.zeros(sz) for sz in [num_features] * 4]
        self.pol_traces = [np.zeros(sz) for sz in [num_features] * 4]

        self.val_weights = np.zeros(num_features)
        self.val_trace = np.zeros(num_features)
        self.rbar = 0  # Average reward

    def sample_action(self, features):
        """
        Sample the throttle and direction according to our normal distributions

        :param features: Unified feature vector for all approximations
        :return: (throttle, direction)
        """
        t_mu, t_sigma, d_mu, d_sigma = self._get_gaussian(features)
        throttle = np.random.normal(t_mu, t_sigma, 1)
        direction = np.random.normal(d_mu, d_sigma, 1)
        return throttle, direction

    def _get_gaussian(self, features):
        t_mu = np.dot(self.pol_weights[0], features)
        t_sigma = math.exp(np.dot(self.pol_weights[1], features))
        d_mu = np.dot(self.pol_weights[2], features)
        d_sigma = math.exp(np.dot(self.pol_weights[3], features))
        return t_mu, t_sigma, d_mu, d_sigma

    def estimate_value(self, state):
        return np.dot(self.val_weights, state)

    def update(self, old_state, new_state, throttle, direction, reward):
        """
        Update step after observing result of an action

        :param old_state: Previous feature vector
        :param new_state: Resulting feature vector
        :param throttle: Throttle action value
        :param direction: Direction action value
        :param reward: One-step reward
        """
        delta = reward - self.rbar + self.estimate_value(new_state) - self.estimate_value(old_state)  # Loss
        self.rbar += self.lr[5] * delta
        # Update value fn
        self.val_trace *= self.lamb[4]
        self.val_trace += old_state  # derivative of linear val fn
        self.val_weights += self.lr[4] * delta * self.val_trace
        # Update policy weights
        gauss = self._get_gaussian(old_state)

        for index in range(len(self.pol_weights)):
            self.pol_traces[index] *= self.lamb[index]

        self.pol_traces[0] += self._mean_grad(gauss[0], gauss[1], throttle, old_state)
        self.pol_traces[1] += self._std_grad(gauss[0], gauss[1], throttle, old_state)
        self.pol_traces[2] += self._mean_grad(gauss[2], gauss[3], direction, old_state)
        self.pol_traces[3] += self._std_grad(gauss[2], gauss[3], direction, old_state)

        for index in range(len(self.pol_weights)):
            self.pol_weights[index] += self.lr[index] * delta * self.pol_traces[index]

    @staticmethod
    def _mean_grad(mu, sigma, action, feature):
        return 1 / (sigma ** 2) * (action - mu) * feature

    @staticmethod
    def _std_grad(mu, sigma, action, feature):
        coeff = ((action - mu)**2 / (sigma**2)) - 1
        return coeff * feature


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
    ac = ActorCritic(np.repeat(1e-2, 6), np.repeat(0.8, 6), 2)
    st1 = np.array([0.8, 0.8])
    st2 = np.array([0.9, 0.9])
    throttle, direction = ac.sample_action(st1)
    print(ac.pol_weights[0])
    ac.update(st1, st2, throttle, direction, 1)
    print(throttle)
    print(direction)
    print(ac.pol_weights[1])
