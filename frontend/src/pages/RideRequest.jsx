import React, { useState } from 'react'
import axios from '../lib/axios'
import Navbar from '../components/Navbar'

export default function RideRequest(){
  const [origin, setOrigin] = useState('')
  const [destination, setDestination] = useState('')
  const [fare, setFare] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleSubmit(e){
    e.preventDefault()
    setLoading(true)
    try{
      // In production, you'd send geo-coordinates. Here we assume coordinates are provided.
      await axios.post('/rides/request/', {
        origin: origin, // should be {type: 'Point', coordinates: [lng, lat]} according to GeoDjango format or custom serializer
        destination: destination,
        fare: fare
      })
      alert('Ride requested')
    }catch(err){
      alert('Error: '+JSON.stringify(err.response?.data || err.message))
    }finally{ setLoading(false) }
  }

  return (
    <>
      <Navbar />
      <div className="container py-5">
        <div className="row justify-content-center">
          <div className="col-md-8">
            <div className="card p-4">
              <h4>Request a Ride</h4>
              <form onSubmit={handleSubmit}>
                <div className="mb-3">
                  <label className="form-label">Origin (lat,lng)</label>
                  <input className="form-control" value={origin} onChange={e=>setOrigin(e.target.value)} placeholder="-1.2921,36.8219" required />
                </div>
                <div className="mb-3">
                  <label className="form-label">Destination (lat,lng)</label>
                  <input className="form-control" value={destination} onChange={e=>setDestination(e.target.value)} placeholder="-1.3032,36.7073" required />
                </div>
                <div className="mb-3">
                  <label className="form-label">Estimated Fare (USD)</label>
                  <input type="number" step="0.01" className="form-control" value={fare} onChange={e=>setFare(e.target.value)} required />
                </div>
                <button className="btn btn-primary" disabled={loading}>{loading ? 'Requesting...' : 'Request Ride'}</button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}
