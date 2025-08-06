import {useEffect, useState} from 'react'
import axios from 'axios'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faSpinner } from '@fortawesome/free-solid-svg-icons'
import axiosInstance from '../../axiosinstance'

const Dashboard = () => {
     const [ticker, setTicker] = useState('')
     const [user, setUser] = useState(null)
     const [error, setError] = useState()
     const [plot, setPlot] = useState()
     const [ma100, setMa100] = useState()
     const [ma200, setMa200] = useState()
     const [prediction, setPrediction] = useState()
     const [mse, setMSE] = useState()
     const [rmse, setRMSE] = useState()
     const [r2, setR2] = useState()
     const [Sevenday_predict, setSevenday_predict] = useState()
    useEffect(() => {
      const fetcProtectedData = async () => {
        try {
             const response = await axiosInstance.get('/protected-view/');
             setUser(response.data.user)
            
        } catch (error) {
            console.error('Error fetching protected data:',error);
        }
      }
    
      fetcProtectedData();
    }, [])
const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axiosInstance.post('/predict/', { ticker: ticker });
      console.log(response.data);
      const backendRoot = import.meta.env.VITE_BACKEND_ROOT
      const plotUrl = `${backendRoot}${response.data.plot_img}`
      const ma100Url = `${backendRoot}${response.data.plot_100_dma}`
      const ma200Url = `${backendRoot}${response.data.plot_200_dma}`
      const predictionUrl = `${backendRoot}${response.data.plot_prediction}`
      const FutureUrl = `${backendRoot}${response.data.plot_future}`
      
      setPlot(plotUrl)
      setMa100(ma100Url)
      setMa200(ma200Url)
      setPrediction(predictionUrl)
      setSevenday_predict(FutureUrl)
      setMSE(response.data.mse)
      setRMSE(response.data.rmse)
      setR2(response.data.r2)
      if(response.data.error){
                setError(response.data.error)
                setPlot()
                setMa100()
                setMa200()
                setPrediction()
                setMSE()
                setRMSE()
                setR2()
      }else{
                setError(null)
      }
     
    } catch (error) {
      console.error('There was an error making the API request', error)
    }
}

    


  return (
    <>
    <div className='text-light container '>
      {user ? (
        <>
        <div className='row'>
          <div className='col-md-6 mx-auto'>
            <div className='d-flex justify-content-center align-items-center mb-3'>
              <h1>Welcome, <strong>{user.username}</strong>!</h1></div>
          </div>
        </div>
        
        
        </>
        
        
      ) : (
        <p>Loading user info...</p>
      )}

      <div className='row'>
        <div className='col-md-6 mx-auto'>
          <form onSubmit={handleSubmit} className='d-flex align-items-center w-100 gap-2'>
            <input type="text" className='form-control' placeholder='Enter Stock Ticker'
             onChange={(e) => setTicker(e.target.value)} required
            ></input>
            
            <button className='btn btn-primary' type='submit'>Search</button>
            
          </form>
          <small>{error && <div className='text-danger'>{error}</div>}</small>
        </div>
        {/* Print prediction plots */}
        <div className="prediction mt-5">
          <div className="p-3">
            {plot && (
              <img src={plot} style={{ maxWidth: '100%' }} />
              )}
          </div>
        </div>
        <div className="prediction mt-5">
          <div className="p-3">
            {plot && (
              <img src={ma100} style={{ maxWidth: '100%' }} />
              )}
          </div>
        </div>
        <div className="prediction mt-5">
          <div className="p-3">
            {plot && (
              <img src={ma200} style={{ maxWidth: '100%' }} />
              )}
          </div>
        </div>
        <div className="prediction mt-5">
          <div className="p-3">
            {plot && (
              <img src={prediction} style={{ maxWidth: '100%' }} />
              )}
          </div>
        </div>

        <div className="prediction mt-5">
          <div className="p-3">
            {plot && (
              <img src={Sevenday_predict} style={{ maxWidth: '100%' }} />
              )}
          </div>
        </div>

        <div className="text-light p-3">
                    <h4>Model Evalulation</h4>
                    <p>Mean Squared Error (MSE): {mse}</p>
                    <p>Root Mean Squared Error (RMSE): {rmse}</p>
                    <p>R-Squared: {r2}</p>
                </div>

      </div>
    </div>
    
    </>
    
  )
}

export default Dashboard