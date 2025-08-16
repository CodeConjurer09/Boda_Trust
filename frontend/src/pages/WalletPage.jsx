import React, { useEffect, useState } from 'react'
import axios from '../lib/axios'
import Navbar from '../components/Navbar'

export default function WalletPage(){
  const [wallet, setWallet] = useState(null)

  useEffect(()=>{
    axios.get('/payments/wallet/')
      .then(res=> setWallet(res.data))
      .catch(err=> console.error(err))
  }, [])

  if(!wallet) return (
    <>
      <Navbar />
      <div className="container py-5">Loading...</div>
    </>
  )

  return (
    <>
      <Navbar />
      <div className="container py-5">
        <div className="row">
          <div className="col-md-6">
            <div className="card p-3">
              <h5>Wallet</h5>
              <p>Balance (USD): <strong>{wallet.balance_usd}</strong></p>
              <p>Referral Balance (KSH): <strong>{wallet.referral_balance_ksh}</strong></p>
              <p>Deposit Balance (KSH): <strong>{wallet.deposit_balance_ksh}</strong></p>
              <div className="d-grid gap-2">
                <a className="btn btn-outline-primary" href="/topup">Top up (M-Pesa)</a>
                <a className="btn btn-outline-secondary" href="/withdraw">Request Withdrawal</a>
              </div>
            </div>
          </div>
          <div className="col-md-6">
            <div className="card p-3">
              <h5>Recent Transactions</h5>
              {/* You can fetch transactions from /payments/transactions/ */}
            </div>
          </div>
        </div>
      </div>
    </>
  )
}
