import random
import pandas as pd
import numpy as np
import datetime as dt
from pandas_datareader import data as pdr
from scipy.optimize import minimize
import yfinance as yf
yf.pdr_override()

  
# Import data
def getData(stocks, start, end):
    stockData = pdr.get_data_yahoo(stocks, start=start, end=end)
    stockData = stockData['Close']
    returns = stockData.pct_change()
    meanReturns = returns.mean()
    covMatrix = returns.cov()
    return meanReturns.to_numpy(), covMatrix.to_numpy()

def portfolio_expected_Return(weights, expectedreturn):
    weighted_sum = sum(expectedreturn * weight for expectedreturn,
                       weight in zip(expectedreturn, weights))
    return weighted_sum

def portfolio_std(weights, cov_matrix):
    port_std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    return port_std


def generate_random_weights(numstocks):
    random_points = [random.random() for _ in range(numstocks - 1)]
    # Add 0 and 1 to the list and sort it
    random_points.extend([0, 1])
    random_points.sort()
    # Calculate the differences between successive elements
    weights = np.array([random_points[i+1] - random_points[i]
                       for i in range(numstocks)])
    return weights

# Constraints - sum of weights is 1, and return is the target return
def constraint_sum_of_weights(weights):
    return np.sum(weights) - 1

def constraint_expected_return(weights, meanReturns, target_return):
    return weights.T @ meanReturns - target_return


def portfoliocalc(companies,riskfreerate, attempts,riskscalar):
    # Define a dictionary that maps company names to their ticker symbols
    company_to_ticker = {
        'Microsoft': 'MSFT',
        'Apple': 'AAPL',
        "Google": "GOOGL",
        "Amazon": "AMZN",
        "Visa": "V",
        "Nike": "NKE",
        "Deere & Company": "DE",
        "Tesla": "TSLA",
        "Southwest Airlines Co.": "LUV"
        }
    # Convert company names to ticker symbols
    ticker_symbols = [company_to_ticker[company] for company in companies]
    
    #initilise time variables
    endDate = dt.datetime.now()
    startdate = endDate - dt.timedelta(days=365*5)
    tradingdays = 252

    meanReturns, covMatrix = getData(ticker_symbols, startdate, endDate)
    
    #generate a list of possible portfolios ising random weights and add results to a dataframe 
    availableportfoliosdf = pd.DataFrame(columns=['x', 'y'])
    for i in range(attempts):
        weights = generate_random_weights(len(ticker_symbols))
        x = (portfolio_std(weights, covMatrix) * np.sqrt(tradingdays))
        y = (portfolio_expected_Return(weights, meanReturns)*tradingdays)
        availableportfoliosdf.loc[len(availableportfoliosdf)] = [x, y]



    frontierdf = pd.DataFrame(columns=['Standard Deviations', 'Returns'])
    # Bounds for the weights 
    bounds = tuple((0, 1) for _ in range(len(meanReturns)))
    # Define a range of target returns
    target_returns = np.linspace(availableportfoliosdf['y'].min()/tradingdays, availableportfoliosdf['y'].max()/tradingdays, num=50)
    for target_return in target_returns:
        constraints = [{'type': 'eq', 'fun': constraint_sum_of_weights},
                       {'type': 'eq', 'fun': lambda w: constraint_expected_return(w, meanReturns, target_return)}]
        # Initial guess for the weights
        initial_weights = np.array([1 / len(meanReturns)] * len(meanReturns))
        # Portfolio optimization
        result = minimize(portfolio_std, initial_weights, args=(covMatrix,), method='SLSQP', bounds=bounds, constraints=constraints)
        if result.success:
            frontierdf.loc[len(frontierdf)] = [result.fun*np.sqrt(tradingdays), target_return*tradingdays]


    # find the point on the efficent frontier ccurve that generates the highest sharpe ratio by finding the max gradient with the risk free rate       
    maxgradient = 0
    tangent = [0]*2
    for i in range(50):
        # calculate slope
        gradient = (frontierdf.loc[i,'Returns'] - riskfreerate) / frontierdf.loc[i,'Standard Deviations']
        # if slope is largest store it
        if gradient > maxgradient:
            maxgradient = gradient
            tangent[0] = frontierdf.loc[i,'Standard Deviations']
            tangent[1] = frontierdf.loc[i,'Returns']
                           
            
    # use the tanx and tany values and optimise to find optimum split of portfolio
    result = minimize(portfolio_std, initial_weights, args=(covMatrix,), method='SLSQP', bounds=bounds, constraints=constraints)
    if result.success:
        optimized_weights = result.x
        #optimized_risk = result.fun  # This is the minimized risk for the desired return
    #result = minimize(portfolio_std, initial_weights, args=(covMatrix,), method='SLSQP', bounds=bounds, constraints=constraints)
    
    
    #optimal risky portfolio
    optimalportfolio = [0]*2
    optimalportfolio[0] = tangent[0] * riskscalar
    optimalportfolio[1] = tangent[1] * riskscalar + riskfreerate * (1-riskscalar)
    
    
    
    #scale for risk tolerence
    optimized_weights = [round(num * 100 *riskscalar, 2) for num in optimized_weights]
    optimized_weights.append(round(100-sum(optimized_weights)))
    companies.append("Bonds")
    portfoliotabledf = pd.DataFrame({'Companies': companies,
                                     'Share of Portfolio': optimized_weights })
    portfoliotabledf = portfoliotabledf[portfoliotabledf['Share of Portfolio'] != 0]
    return availableportfoliosdf , frontierdf , tangent , optimalportfolio , portfoliotabledf


