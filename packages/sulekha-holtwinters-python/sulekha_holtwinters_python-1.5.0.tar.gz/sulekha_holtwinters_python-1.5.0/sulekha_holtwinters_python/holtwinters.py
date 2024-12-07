class holtwinters:
    def __init__(self):
        np = __import__('numpy')
        pd = __import__('pandas')
        minimize = __import__('scipy.optimize', fromlist=['minimize']).minimize
        warnings = __import__('warnings')

        warnings.filterwarnings('ignore')
        pd.options.display.float_format = "{:,.2f}".format
        float_format = "{:.2f}".format
        np.set_printoptions(formatter={'float_kind':float_format})
    
    def extract_actuals(self, pandasDF):
        '''
        Extract observed values from pandas 
        dataframe for further processing.
        Parameters:
        pandasDF - Input a pandas dataframe with only two columns - Date/Time and Observed values
        Example:
        extract_actuals(testDF)
        '''
        oldColumns = pandasDF.columns
        pandasDF = pandasDF.rename(columns={oldColumns[0]: "DateTime", oldColumns[1]: "ObservedVals"})
        observed = pandasDF["ObservedVals"].values
        return observed

    def initiate_trend_factor(self, pandasDF, L):
        '''
        Calculate initial trend factor using a 
        weighted average for better accuracy.
        
        Parameters:
        pandasDF - Input a pandas dataframe with only two columns - Date/Time and Observed values
        
        L - Seasonal length of dataset
        
        Example:
        hw.initiate_trend_factor(testDF,24)
        '''
        observed = self.extract_actuals(pandasDF)
        b_numerator = sum([(observed[L + i] - observed[i]) / L for i in range(L)]) / L
        return b_numerator

     
    def initiate_seasonal_indices(self, pandasDF, L, model_type):
        '''
        Calculate initial seasonal indices for both 
        additive and multiplicative models.

        Parameters:
        pandasDF - Input a pandas dataframe with only two columns - Date/Time and Observed values

        L - Seasonal length of dataset

        Example:
        SeasonalIndices2,Avgs2,Subset2 = hw.initiate_seasonal_indices(testDF,24,'multiplicative')
        '''
        np = __import__('numpy')
        observed = self.extract_actuals(pandasDF)

        period = len(observed) // L

        Subset = []
        Avgs = []

        for i in range(period):
            Subset.append(observed[i*L:(i+1)*L])

        Avgs = [np.mean(subset) for subset in Subset]

        Indices = [[] for _ in range(L)]  

        for i in range(period):
            for j in range(L):
                if model_type == 'multiplicative':
                    Indices[j].append(Subset[i][j] / Avgs[i])
                else:
                    Indices[j].append(Subset[i][j] - Avgs[i])

        SeasonalIndices = []
        for j in range(L):
            SeasonalIndices.append(np.mean(Indices[j]))

        return SeasonalIndices



    def holtwinters(self, pandasDF, alpha, beta, gamma, L, n_predictions, model_type='multiplicative'):
        '''
        Generic Holt-Winters forecasting method 
        for additive and multiplicative models.
        
        Parameters:
        pandasDF - Input a pandas dataframe with only two columns - Date/Time and Observed values

        alpha - parameter required to calculate Level

        beta - parameter required to calculate Trend

        gamma - parameter required to calculate Seasonality
        
        L - Seasonal length of dataset

        n_predictions - No. of future periods to predict
        
        Example:
        Observed2, Predictions2, Level2, Trend2, Seasonality2 = 
        hw.holtwinters(testDF,0.865,0.01,0.865,24,48,'multiplicative')
        '''
        observed = self.extract_actuals(pandasDF)
        SeasonalIndices = self.initiate_seasonal_indices(pandasDF, L, model_type)
        trendfactor = self.initiate_trend_factor(pandasDF, L)
        Level = [observed[0]]
        Trend = [trendfactor]
        Predictions = []
        p = len(observed)
        k = p + n_predictions
        SeasonalityIndex = SeasonalIndices[:]

        for i in range(k):
            if i == 0:
                Predictions.append(observed[0])
            elif i < p:
                if model_type == 'multiplicative':
                    Level.append(alpha * (observed[i] / SeasonalityIndex[i % L]) + (1 - alpha) * (Level[i - 1] + Trend[i - 1]))
                    Trend.append(beta * (Level[i] - Level[i - 1]) + (1 - beta) * Trend[i - 1])
                    SeasonalityIndex[i % L] = gamma * (observed[i] / Level[i]) + (1 - gamma) * SeasonalityIndex[i % L]
                    Predictions.append((Level[i] + Trend[i]) * SeasonalityIndex[i % L])
                elif model_type == 'additive':
                    Level.append(alpha * (observed[i] - SeasonalityIndex[i % L]) + (1 - alpha) * (Level[i - 1] + Trend[i - 1]))
                    Trend.append(beta * (Level[i] - Level[i - 1]) + (1 - beta) * Trend[i - 1])
                    SeasonalityIndex[i % L] = gamma * (observed[i] - Level[i]) + (1 - gamma) * SeasonalityIndex[i % L]
                    Predictions.append(Level[i] + Trend[i] + SeasonalityIndex[i % L])
            else:  
                m = i - p + 1
                if model_type == 'multiplicative':
                    Predictions.append((Level[p - 1] + m * Trend[p - 1]) * SeasonalityIndex[i % L])
                elif model_type == 'additive':
                    Predictions.append((Level[p - 1] + m * Trend[p - 1]) + SeasonalityIndex[i % L])

        return observed, Predictions, Level, Trend, SeasonalityIndex

    def Error(self, Observed, Predictions):
        '''Calculate sum of errors.
        Parameters:
        Observed - Observed values [input type: series]
        Predictions - Forecasted values [input type: series]
        
        Example:
        hw.Error(Observed, Predictions)
        '''
        return sum([Observed[i] - Predictions[i] for i in range(len(Observed))])

    def ABSError(self, Observed, Predictions):
        '''Calculate sum of absolute errors.
        Parameters:
        Observed - Observed values [input type: series]
        Predictions - Forecasted values [input type: series]
        
        Example:
        hw.ABSError(Observed, Predictions)
        '''
        return sum([abs(Observed[i] - Predictions[i]) for i in range(len(Observed))])

    def RMSE(self, Observed, Predictions):
        '''Calculate Root Mean Square Error.
        Parameters:
        Observed - Observed values [input type: series]
        Predictions - Forecasted values [input type: series]
        
        Example:
        hw.RMSE(Observed2, Predictions2)
        '''
        np = __import__('numpy')
        return np.sqrt(np.mean([(Observed[i] - Predictions[i]) ** 2 for i in range(len(Observed))]))

    def MAPE(self, Observed, Predictions):
        '''Calculate Mean Absolute Percentage Error.
        Parameters:
        Observed - Observed values [input type: series]
        Predictions - Forecasted values [input type: series]
        
        Example:
        hw.MAPE(Observed, Predictions)
        '''
        np = __import__('numpy')
        return np.mean([abs((Observed[i] - Predictions[i]) / Observed[i]) for i in range(len(Observed))]) * 100

    def Accuracy(self, Observed, Predictions):
        '''Calculate Forecasting Accuracy as 100 - MAPE.
        Parameters:
        Observed - Observed values [input type: series]
        Predictions - Forecasted values [input type: series]
        Example:
        hw.Accuracy(Observed, Predictions)
        
        '''
        return 100 - self.MAPE(Observed, Predictions)
    
    def BestFit(self, pandasDF, possible_season_lengths, n_predictions, model_type='multiplicative'):
        '''
        Optimize alpha, beta, and gamma for best forecasting accuracy.
        Uses scipy's minimize function for parameter tuning.
        
        Parameters:
        pandasDF - Input a pandas dataframe with only two columns - Date/Time and Observed values

        possible_season_lengths: a list of possible values for the season length (L)
        n_predictions: number of time steps to predict into the future
        model_type: 'multiplicative' or 'additive'
    
        Example: hw.BestFit(testDF, possible_season_lengths = [12, 24, 36], n_predictions = 36, model_type='multiplicative')
        '''
        minimize = __import__('scipy.optimize', fromlist=['minimize']).minimize
        np = __import__('numpy')
        def objective(params, L):
            alpha, beta, gamma = params
            Observed, Predictions, _, _, seasonality = self.holtwinters(
                pandasDF, alpha, beta, gamma, L, n_predictions, model_type
            )
        
            return self.RMSE(Observed, Predictions)
    
        best_mse = float('inf')
        best_alpha, best_beta, best_gamma, best_seasonality, best_L = None, None, None, None, None

        initial_guess = [0.0, 0.0, 0.0]
        bounds = [(0, 1), (0, 1), (0, 1)]
    
        for L in possible_season_lengths:
            result = minimize(objective, initial_guess, args=(L,), bounds=bounds, method='L-BFGS-B')
            alpha, beta, gamma = result.x
            mse = result.fun
       
            if mse < best_mse:
                best_mse = mse
                best_alpha = alpha
                best_beta = beta
                best_gamma = gamma
                best_L = L
                _, _, _, _, _ = self.holtwinters(
                    pandasDF, alpha, beta, gamma, L, n_predictions, model_type
                )

        accuracy = 100 - best_mse

        return accuracy, best_alpha, best_beta, best_gamma, best_L


    def CreateGraphs(self, model):
        '''Function to plot Observed, Predictions, Level, Trend, 
        Seasonality values using Plotly.
        
        Parameters:
        model - holtwinters() model
        Example:
        model1 = hw.holtwinters(testDF,0.865,0.01,0.865,24,48,'additive')
        hw.CreateGraphs(model1)

        model2 = hw.holtwinters(testDF,0.865,0.01,0.865,24,48,'multiplicative')
        hw.CreateGraphs(model2)      
        '''
        from plotly.offline import init_notebook_mode, iplot
        import plotly.graph_objs as go
        from plotly import subplots
        init_notebook_mode(connected=True)
        
        Observed, Predictions, Level, Trend, Seasonality = model
        observed = go.Scatter(y=Observed, mode='lines', name='Observed')
        predictions = go.Scatter(y=Predictions, mode='lines', name='Predictions')
        level = go.Scatter(y=Level, mode='lines', name='Level')
        trend = go.Scatter(y=Trend, mode='lines', name='Trend')
        seasonality = go.Scatter(y=Seasonality, mode='lines', name='Seasonality')

        fig = subplots.make_subplots(rows=5, cols=1, subplot_titles=["Observed", "Predictions", "Level", "Trend", "Seasonality"])
        fig.append_trace(observed, 1, 1)
        fig.append_trace(predictions, 2, 1)
        fig.append_trace(level, 3, 1)
        fig.append_trace(trend, 4, 1)
        fig.append_trace(seasonality, 5, 1)

        fig.update_layout(height=800, width=900, title='Holt-Winters Forecast', showlegend=True)
        iplot(fig)

