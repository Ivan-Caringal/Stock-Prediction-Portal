import React from 'react'
import Button from './Button'
import Header from './Header'
import Footer from './Footer'
import PrivateRoute from '../Privateroute'
import PublicRoute from '../PublicRoute'
const Main = () => {
  return (
    <>
      
    <div className='container pt-3 '>
      <div className='p-5 text-center bg-light-dark rounded'>
        <h1 className='text-light'>Welcome to the Stock Prediction Portal</h1>
        <p className="lead text-light">This stock prediction application utilizes machine learning techniques, specifically employing Keras, and LSTM model, integrated within the Django framework. It forecasts future stock prices by analyzing 100-day and 200-day moving averages, essential indicators widely used by stock analysts to inform trading and investment decisions.</p>
        <PublicRoute><Button text='Explore now' class='btn-outline-info' url="/dashboard"/></PublicRoute>
      </div>
    </div>
    
   </>
  );
};


export default Main