# Valatility Crypto Top Ticking Dashboard ₿

![Dashboard Image](https://github.com/valazeinali/Valatility-Crypto-Gang/blob/main/assets/Valatility.png)

# https://valatility.com

Welcome to the Valatility Crypto Top Ticking Dashboard project. This repository is the central hub for collaboration among members of the Valatility #crypto channel. Our objective is to develop a comprehensive dashboard for cryptocurrency tick data, utilizing various algorithms and strategies to provide insightful analytics and forecasts.

## Project Objective

The primary goal of this project is to aggregate real-time and historical cryptocurrency data to create a dynamic and interactive dashboard. This dashboard aims to serve as a powerful tool for traders and enthusiasts, providing them with the ability to analyze market trends, compare different cryptocurrencies, and apply various trading strategies effectively.

## Features

- **Real-Time Data Visualization**: Interactive charts and graphs displaying live cryptocurrency data.
- **Historical Data Analysis**: Tools to analyze historical price movements and trends.
- **Algorithmic Trading Strategies**: Implementation of various trading algorithms to forecast future movements.
- **Customizable Indicators**: Users can select and customize technical indicators according to their trading preferences.
- **Portfolio Tracking**: Functionality to track and manage your cryptocurrency portfolio within the dashboard.

## Getting Started

### Prerequisites

Before you begin, ensure you have met the following requirements:

- **Python 3.8 or higher**: Make sure Python is installed on your system. You can check your Python version by running `python --version` or `python3 --version` in your terminal
- **Pip** (Python package installer)

### Installation & Contribution

We welcome contributions from everyone. If you're interested in helping, please:

1. Clone the repository to your local machine:

```commandline
git clone https://github.com/valazeinali/Valatility-Crypto-Gang.git
```

2. Navigate to the project directory:

```commandline
cd Valatility-Crypto-Gang
```

3. Install a virtual environment. Choose one of the following methods (example uses venv):

```commandline
python -m venv venv
# Activate the virtual environment
# On Windows
.\venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

4. Intall package dependencies:

```commandline
pip install -r requirements.txt
```

## Setting Up Pre-commit Git Hooks and Pre-push Hooks

### Pre-commit Installation

This project utilizes pre-commit to manage Git hooks, enhancing code quality and consistency.
Follow the steps below to set up these hooks on your local machine:

1. Install `pre-commit`.
   - This project requires Python. pre-commit can be installed via pip. The installation should be handled automatically
     from step 4 of the Contribution section; however, if needed, it can be installed manually with the following command:

```commandline
pip install pre-commit
```

2. Install the Git Hook scripts:
   - To activate the pre-commit hooks in your local repository to automatically run on every commit, run the following command:

```commandline
pre-commit install
```

3. (Optionally), run `pre-commit` against all the files to ensure everything is formatted properly:
   - To ensure your entire codebase is formatted and passes the hooks, execute:

```commandline
pre-commit run --all-files
```

### Setting Up Pre-push Hooks

1. Install Pre-push Hooks
   - Some workflows benefit from additional checks before pushing to remote repositories. To install pre-push hooks, run the provided script

```commandline
bash install_hooks.sh
```

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

- Project Link: [https://github.com/valazeinali/Valatility-Crypto-Gang](https://github.com/valazeinali/Valatility-Crypto-Gang)
