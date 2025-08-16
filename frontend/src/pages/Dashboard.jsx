import React from 'react'
import Navbar from '../components/Navbar'

export default function Dashboard(){
  return (
    <>
      <Navbar />
      <div className="container py-5">
        <div className="row">
          <div className="col-md-8">
            <h3>Dashboard</h3>
            <p>Quick actions: Request a ride, view your trips, or open chat.</p>
            <div className="d-grid gap-2 d-md-flex">
              <a className="btn btn-primary me-2" href="/ride/request">Request Ride</a>
              <a className="btn btn-outline-secondary" href="/wallet">Wallet</a>
            </div>
          </div>
          <div className="col-md-4">
            <div className="card p-3">
              <h6>Your Profile</h6>
              <p>Brief profile info here (populate from API)</p>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}