# Portfolio Theory Web App

This project provides a Python script to modern portfolio theory analysis based on Harry Markowitz's principles. It's especially useful for visualising the risk return relationship within the market. Additionally, the project includes a Streamlit web app for visualizing the results. The final result is deployed as [Portfolio Theory Web App](https://portfoliocalcapp-ukfuypapshw6i8mek946qb.streamlit.app/)

## Features

- Simulation of portfolio returns and volitility for given stocks and provides optimall portfolio.
- Visualize simulated portfolios risk return relationship.
- Deployed as a Streamlit web app.

### Prerequisites

- Python (3.9 or higher)
- Required Python packages (install via `pip install -r requirements.txt`):
  - random
  - pandas
  - numpy
  - datetime
  - pandas_datareader
  - scipy optimize
  - yfinance
  - streamlit
  - plotly express

### Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/Bjohns800/portfolio_calc_app.git
   ```

2. Navigate to the project directory:

   ```bash
   cd portfolio_calc_app
   ```

3. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

### Usage

#### Portfolio Sumilation Script

Run the portfolio sinulation script:

```bash
python portfolio_calc.py
```

#### Web App

The project includes a Streamlit web app. To run the web app, use the following command:

```bash
streamlit run portfolio_sim_app.py
```

This will launch the app locally, and you can access it via your web browser.

### Deployed Web App

The web app is deployed and accessible online at:

[Portfolio Theory Web App](https://portfoliocalcapp-ukfuypapshw6i8mek946qb.streamlit.app/)

## Contributing

If you'd like to contribute to this project, please follow these steps:

1. Fork the repository on GitHub.
2. Create a new branch with your changes: `git checkout -b feature/your-feature-name`.
3. Commit your changes and push to your branch.
4. Create a pull request to the original repository's `main` branch.

## Acknowledgments

- Inspiration for the web app was from Jkaterina's monte carlo option pricong and can be found [here](https://github.com/JKaterina/monte-carlo-python/tree/main)
- Modern portfolio theory is based on Harry Markowitz's principles.
- Special thanks to the open-source Python community for the libraries and tools used in this project.

Feel free to customize the README with additional details, project-specific instructions, and acknowledgements as needed.
