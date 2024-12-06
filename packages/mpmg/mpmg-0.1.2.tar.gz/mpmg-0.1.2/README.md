# Minimum Price Markov Game (MPMG) Environment

## Overview

`mpmg` is a modular environment designed for studying the Minimum Price Markov Game (MPMG), a concept in game theory and algorithmic game theory. It provides an easy-to-use framework for conducting experiments with multiple agents using collusion and cooperation dynamics. This environment is useful for researchers and developers interested in game theory, reinforcement learning, and multi-agent systems.

## Features
- **Customizable Multi-Agent Environment**: Supports different numbers of agents and heterogeneous vs. homogeneous settings.

## Project Structure

```
mpmg/
├── mpmg/                  # Main package directory
│   ├── __init__.py        # Package initialization
│   └── mpmg_env.py        # Environment implementation
├── .gitignore             # Ignored files for git
├── README.md              # Project description and usage guide
├── requirements.txt       # Project dependencies
├── setup.py               # Installation script
└── LICENSE                # License information
```

## Installation

To install the package locally, run the following command from the root directory:

```sh
pip install mpmg
```

This installs the package in "editable" mode, meaning any changes made in the source code will immediately reflect in the installed package.

## Requirements
- Python 3.6+

## Usage

To use the `mpmg` package, import the `MPMGEnv` class and create an instance of the environment:

```python
from mpmg import MPMGEnv

# Create an instance of the environment
env = MPMGEnv(n_agents=2, sigma_beta=0.0, alpha=1.3)

# Reset the environment
state = env.reset()

# Take a step in the environment
actions = [1, 0]  # Example actions for each agent
rewards, next_state, done = env.step(actions)
```


The `MPMGEnv` class provides methods for resetting the environment, taking steps, and observing the state, rewards, and dynamics of multi-agent interactions.

## Parameter Definition
```
num_agents (int): Number of agents. Must be a positive integer, default value is 2.

sigma_beta (float): Heterogeneity level, standard deviation of the power parameters' distribution. Must be in [0,1], default value is 0.

alpha (float): Collusive bid multiplier. Must be > 1.
```

## Scenarios
`MPMGEnv` is a social dilemma based on the Prisoner's Dilemma. 

- **Full Defection**: All agents choose to defect (action 0), Nash Equilibrium.
- **Full Cooperation**: All agents cooperate (action 1), Pareto Optimal.
- **Asymmetric play**: actions taken can be separated into two sets, other suboptimal outcome.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request for improvements, bug fixes, or new features.

## Author

Igor Sadoune - igor.sadoune@polymtl.ca

