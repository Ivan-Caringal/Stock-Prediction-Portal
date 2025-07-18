import React from 'react'

const test1 = () => {
  return (
    
   <>
      <div className="container d-flex justify-content-center align-items-center " style={{ minHeight: '80vh' }}>
        <div className="p-5 text-center  rounded bg-light-dark">
          <h1 className="text-light">Welcome to the Stock Prediction Portal</h1>
          <p className="lead text-light">
            This stock prediction application utilizes machine learning techniques, specifically employing Keras, and LSTM model, integrated within the Django framework. It forecasts future stock prices by analyzing 100-day and 200-day moving averages, essential indicators widely used by stock analysts to inform trading and investment decisions.
          </p>
          <a className="btn btn-outline-info" href="#">Login</a>
        </div>
      </div>
    </>
  )
}

export default test1