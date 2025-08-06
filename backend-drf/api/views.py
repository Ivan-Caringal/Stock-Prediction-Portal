from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import StockPredictionSerializer
from rest_framework import status
from rest_framework.response import Response
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os
from django.conf import settings
from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model
import os
from django.conf import settings
from .utils import save_plot
from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model
from sklearn.metrics import mean_squared_error, r2_score

# Create your views here.
class StockPredictionAPIView(APIView):
    def post(self, request):
        serializer = StockPredictionSerializer(data=request.data)
        if serializer.is_valid():
            ticker = serializer.validated_data['ticker']

            # Fetch the data from yfinance
            now = datetime.now()
            start = datetime(now.year-10, now.month, now.day)
            end = now
            df = yf.download(ticker, start, end)
            
            if df.empty:
                return Response({"error": "No data found for the given ticker.",
                                 'status': status.HTTP_404_NOT_FOUND})
            
            df = df.reset_index()
            # Generate Basic Plot
            plt.switch_backend('AGG')
            plt.figure(figsize=(12, 5))
            plt.plot(df.Close, label='Closing Price')
            plt.title(f'Closing price of {ticker}')
            plt.xlabel('Days')
            plt.ylabel('Price')
            plt.legend()
            # Save the plot to a file
            plot_img_path = f'{ticker}_plot.png'
            plot_img = save_plot(plot_img_path)

            # 100 Days moving average
            ma100 = df.Close.rolling(100).mean()
            plt.switch_backend('AGG')
            plt.figure(figsize=(12, 5))
            plt.plot(df.Close, label='Closing Price')
            plt.plot(ma100, 'r', label='100 DMA')
            plt.title(f'100 Days Moving Average of {ticker}')
            plt.xlabel('Days')
            plt.ylabel('Price')
            plt.legend()
            plot_img_path = f'{ticker}_100_dma.png'
            plot_100_dma = save_plot(plot_img_path)

            # 200 Days moving average
            ma200 = df.Close.rolling(200).mean()
            plt.switch_backend('AGG')
            plt.figure(figsize=(12, 5))
            plt.plot(df.Close, label='Closing Price')
            plt.plot(ma100, 'r', label='100 DMA')
            plt.plot(ma200, 'g', label='200 DMA')
            plt.title(f'200 Days Moving Average of {ticker}')
            plt.xlabel('Days')
            plt.ylabel('Price')
            plt.legend()
            plot_img_path = f'{ticker}_200_dma.png'
            plot_200_dma = save_plot(plot_img_path)


            # Splitting data into Training & Testing datasets
            data_training = pd.DataFrame(df.Close[0:int(len(df)*0.7)])
            data_testing = pd.DataFrame(df.Close[int(len(df)*0.7): int(len(df))])

            # Scaling down the data between 0 and 1
            scaler = MinMaxScaler(feature_range=(0,1))

            # Load ML Model
            model = load_model('../Resources/keras_model.keras')

            # Preparing Test Data
            past_100_days = data_training.tail(100)
            final_df = pd.concat([past_100_days, data_testing], ignore_index=True)
            input_data = scaler.fit_transform(final_df)

            x_test = []
            y_test = []
            for i in range(100, input_data.shape[0]):
                x_test.append(input_data[i-100: i])
                y_test.append(input_data[i, 0])
            x_test, y_test = np.array(x_test), np.array(y_test)

            # Making Predictions
            y_predicted = model.predict(x_test)

            # Revert the scaled prices to original price
            y_predicted = scaler.inverse_transform(y_predicted.reshape(-1, 1)).flatten()
            y_test = scaler.inverse_transform(y_test.reshape(-1, 1)).flatten()

            # Plot the final prediction
            plt.switch_backend('AGG')
            plt.figure(figsize=(12, 5))
            plt.plot(y_test, 'b', label='Original Price')
            plt.plot(y_predicted, 'r', label='Predicted Price')
            plt.title(f'Final Prediction for {ticker}')
            plt.xlabel('Days')
            plt.ylabel('Price')
            plt.legend()
            plot_img_path = f'{ticker}_final_prediction.png'
            plot_prediction = save_plot(plot_img_path)

            # Model Evaluation
            # Mean Squared Error (MSE)
            mse = mean_squared_error(y_test, y_predicted)

            # Root Mean Squared Error (RMSE)
            rmse = np.sqrt(mse)

            # R-Squared
            r2 = r2_score(y_test, y_predicted)


            # Making Predictions futures
            past_100_days_training=data_training.tail(100)
            past_100_days_testing=data_testing.tail(100)
            Mynewfinal_df = pd.concat([past_100_days_training, data_testing], ignore_index=True)
            scaled_last_100 = scaler.transform(past_100_days_testing)
            input_seq = scaled_last_100.reshape(1, 100, 1)

            future_predictions = []

            for _ in range(7):  # change this to how many days you want to predict
                prediction = model.predict(input_seq, verbose=0)
                predicted_value = prediction[0, 0]
                future_predictions.append(predicted_value)

                # update input_seq: remove first, add predicted at the end
                predicted_reshaped = np.array([[[predicted_value]]]) 
                input_seq = np.append(input_seq[:, 1:, :], predicted_reshaped, axis=1)

            My_predicted = scaler.inverse_transform(np.array(future_predictions).reshape(-1, 1)).flatten()
            df_predicted = pd.DataFrame(My_predicted, columns=['Predicted_Price'])

            plt.figure(figsize=(14, 6))
            plt.plot(df_predicted.index, df_predicted['Predicted_Price'], color='red', label='Future Predicted Prices')

            plt.title("Next 7 Day Stock Price Forecast")
            plt.xlabel("Date")
            plt.ylabel("Predicted Price")
            plt.legend()
            plt.grid(True)
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()
            plot_img_path = f'{ticker}_future_prediction.png'
            plot_future = save_plot(plot_img_path)



            return Response({
                "status": "success", 
                "plot_img": plot_img,
                'plot_100_dma': plot_100_dma,
                'plot_200_dma': plot_200_dma,
                'plot_prediction': plot_prediction,
                'mse': mse,
                'rmse': rmse,
                'r2': r2,
                'plot_future':plot_future
                })
        
            