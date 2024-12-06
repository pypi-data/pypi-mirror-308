#mpmg/mpmg.py

import numpy as np
import itertools
from typing import Tuple, List, Dict


class MPMGEnv:
    '''
    Minimum Price Markov Game modular environment. A theoretical model 
    that reasonably approximates real-world first-price markets following the minimum price rule, 
    such as public auctions. See: https://arxiv.org/abs/2407.03521 for more details.

    Parameters:
    ----------

    num_agents (int): Number of agents. Must be a positive integer, default value is 2.
    sigma_beta (float): Heterogeneity level, standard deviation of the power parameters' distribution. Must be in [0,1], default value is 0.
    alpha (float): Collusive bid multiplier. Must be > 1.  
    '''


    def __init__(
        self, 
        num_agents: int = 2, 
        sigma_beta: float = 0.0, 
        alpha: float = 1.3
    ):

        # Validate num_agents
        if not isinstance(num_agents, int) or num_agents <= 0:
            raise ValueError(f'num_agents must be a positive integer, not {num_agents}.')
        self.num_agents = num_agents

        # Validate sigma_beta
        if not isinstance(sigma_beta, (float, int)) or not (0 <= sigma_beta <= 1):
            raise ValueError(f'sigma_beta must be a float in the range [0, 1], not {sigma_beta}.')
        self.sigma_beta = sigma_beta

        # Validate alpha
        if not isinstance(alpha, (float, int)) or alpha <= 1:
            raise ValueError(f'alpha must be a float greater than 1, not {alpha}.')
        self.alpha = alpha

        # Internal state action variables
        self.action_size = 2
        self.joint_action_size = self.action_size ** self.num_agents
        self.beta_size = self.num_agents
        self.state_size = self.num_agents + self.joint_action_size + self.beta_size
        self.state_space = {
            'action_frequencies': None,
            'joint_action_frequencies': None,
            'beta_parameters': None
        }

    @staticmethod
    def _get_joint_action_code(actions: List[int]) -> int:
        action_code = 0
        for action in actions:
            action_code = (action_code << 1) | action
        return action_code
    
    def _get_power_parameters(self) -> None:
        '''
        Generates market shares as power parameters based on market heterogeneity.
        '''
        # Homogeneous agents
        if self.sigma_beta == 0:
            self.beta_parameters = np.ones(self.num_agents) / self.num_agents
        # Heterogeneous agents
        else:
            beta = np.abs(np.random.normal(1 / self.num_agents, self.sigma_beta, self.num_agents))
            self.beta_parameters = beta / np.sum(beta)

    def _update_action_frequencies(self, actions: List[int]) -> None:
        for agent_id, action in enumerate(actions): 
            if action == 1:
                self.action_counts[agent_id] += 1
        self.action_frequencies = self.action_counts / self.iteration

    def _update_joint_action_frequencies(self, actions: List[int]) -> None:
        index = self._get_joint_action_code(actions)
        self.joint_action_counts[index] += 1
        self.joint_action_frequencies = self.joint_action_counts / self.iteration

    def _update_beta(self) -> None:
        '''
        Placeholder method for future beta parameter updates.
        '''
        pass

    def _get_immediate_rewards(self, actions: List[int]) -> np.ndarray:
        '''
        Follows Minimum Price Game (MPG) payoff structure.
        '''
        mask_defect = np.array([action == 0 for action in actions])  # Defection mask
        if mask_defect.sum() == 0:  # All cooperate
            rewards = ((1 - self.beta_parameters) * self.beta_parameters) * self.alpha
        else:
            beta_omega = mask_defect.dot(self.beta_parameters)
            rewards = ((1 - self.beta_parameters) * (self.beta_parameters / beta_omega)) * mask_defect
        return rewards

    def _get_state(self) -> Dict[str, np.ndarray]:
        '''
        Observation space can be incremented here.
        '''
        self.state_space['action_frequencies'] = self.action_frequencies
        self.state_space['joint_action_frequencies'] = self.joint_action_frequencies
        self.state_space['beta_parameters'] = self.beta_parameters
        # To extend the state space
        # self.state_space['additional_variable'] = self.additional_variable
        return np.concatenate([v.flatten() for v in self.state_space.values()])

    def reset(self) -> Dict[str, np.ndarray]:
        '''
        Reset env with unbiased frequencies. Returns initial state.
        '''
        self._get_power_parameters()
        self.iteration = 1  # not 0 because it's a counter
        self.action_counts = np.zeros(self.num_agents)
        self.joint_action_counts = np.zeros(self.joint_action_size)

        # Initialize state with unbiased frequencies (plays each joint action exactly once)
        joint_actions = list(itertools.product(range(self.action_size), repeat=self.num_agents))
        for actions in joint_actions:
            _, _, _ = self.step(list(actions))
        self._get_state()

        return self.state_space
    
    def step(self, actions: List[int]) -> Tuple[np.ndarray, dict, bool]:
        '''
        Executes a single step in the environment.
        '''
        
        # Check that actions is a list of integers
        if not isinstance(actions, list) or not all(isinstance(action, int) for action in actions):
            raise TypeError("actions must be a list of integers.")
    
        # Update internal state variables
        self._update_action_frequencies(actions)
        self._update_joint_action_frequencies(actions)
        # If self.beta_parameters is dynamic
        # self.beta_parameters = self._update_beta()

        # Get immediate rewards
        immediate_rewards = self._get_immediate_rewards(actions)

        # Next state
        next_state = self._get_state()

        # Update counters
        self.iteration += 1

        return immediate_rewards, next_state, True  # 'True' indicates the 'done' flag
