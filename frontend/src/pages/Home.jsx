import React from 'react';
import { Link } from 'react-router-dom';
import Navbar from '../components/Navbar';

export default function Home() {
  return (
    <>
      <Navbar />

      <header className="py-5 bg-primary text-white">
        <div className="container">
          <h1>BodaTrust — Safer Rides, Faster Connections</h1>
          <p className="lead">
            Book rides, request emergency help, chat with drivers, and manage your wallet.
          </p>
        </div>
      </header>

      <main className="container my-5">
        <div className="row">
          <div className="col-md-6">
            <h3>How it works</h3>
            <ol>
              <li>Register as a passenger or driver</li>
              <li>Top up your wallet via M-Pesa (STK Push)</li>
              <li>Request a ride and wait for drivers to accept</li>
              <li>Complete the ride — driver gets paid</li>
            </ol>
          </div>
          <div className="col-md-6">
            <h3>Get Started</h3>
            <p>
              <Link className="btn btn-outline-primary" to="/register">
                Create an account
              </Link>
            </p>
          </div>
        </div>
      </main>
    </>
  );
}
