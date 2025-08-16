import React, { useState } from 'react';
import axios from '../../lib/axios';
import Navbar from '../../components/Navbar';
import { useNavigate } from 'react-router-dom';

export default function Register() {
  const [form, setForm] = useState({
    email: '',
    password: '',
    password2: '',
    first_name: '',
    last_name: '',
    phone_number: '',
    is_driver: false,
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const navigate = useNavigate();

  const handleChange = (field, value) => {
    setForm({ ...form, [field]: value });
  };

  async function handleSubmit(e) {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (form.password !== form.password2) {
      setError('Passwords do not match');
      return;
    }

    setLoading(true);
    try {
      await axios.post('/accounts/register/', form);
      setSuccess('Registered successfully. Redirecting to login...');
      setTimeout(() => navigate('/login'), 2000);
    } catch (err) {
      setError(err.response?.data?.detail || JSON.stringify(err.response?.data) || err.message || 'Registration failed');
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <Navbar />
      <div className="container py-5">
        <div className="row justify-content-center">
          <div className="col-md-8">
            <div className="card p-4 shadow-sm">
              <h3 className="card-title mb-3">Create an account</h3>

              {error && <div className="alert alert-danger">{error}</div>}
              {success && <div className="alert alert-success">{success}</div>}

              <form onSubmit={handleSubmit}>
                <div className="row">
                  <div className="col-md-6 mb-3">
                    <label htmlFor="first_name" className="form-label">First name</label>
                    <input
                      id="first_name"
                      className="form-control"
                      value={form.first_name}
                      onChange={e => handleChange('first_name', e.target.value)}
                      required
                      autoComplete="given-name"
                    />
                  </div>
                  <div className="col-md-6 mb-3">
                    <label htmlFor="last_name" className="form-label">Last name</label>
                    <input
                      id="last_name"
                      className="form-control"
                      value={form.last_name}
                      onChange={e => handleChange('last_name', e.target.value)}
                      autoComplete="family-name"
                    />
                  </div>
                </div>

                <div className="mb-3">
                  <label htmlFor="phone_number" className="form-label">Phone</label>
                  <input
                    id="phone_number"
                    className="form-control"
                    value={form.phone_number}
                    onChange={e => handleChange('phone_number', e.target.value)}
                    autoComplete="tel"
                  />
                </div>

                <div className="mb-3">
                  <label htmlFor="email" className="form-label">Email</label>
                  <input
                    id="email"
                    type="email"
                    className="form-control"
                    value={form.email}
                    onChange={e => handleChange('email', e.target.value)}
                    required
                    autoComplete="email"
                  />
                </div>

                <div className="row">
                  <div className="col-md-6 mb-3">
                    <label htmlFor="password" className="form-label">Password</label>
                    <input
                      id="password"
                      type="password"
                      className="form-control"
                      value={form.password}
                      onChange={e => handleChange('password', e.target.value)}
                      required
                      autoComplete="new-password"
                    />
                  </div>
                  <div className="col-md-6 mb-3">
                    <label htmlFor="password2" className="form-label">Confirm Password</label>
                    <input
                      id="password2"
                      type="password"
                      className="form-control"
                      value={form.password2}
                      onChange={e => handleChange('password2', e.target.value)}
                      required
                      autoComplete="new-password"
                    />
                  </div>
                </div>

                <div className="form-check mb-3">
                  <input
                    className="form-check-input"
                    type="checkbox"
                    id="isDriver"
                    checked={form.is_driver}
                    onChange={e => handleChange('is_driver', e.target.checked)}
                  />
                  <label className="form-check-label" htmlFor="isDriver">
                    Register as driver
                  </label>
                </div>

                <button type="submit" className="btn btn-primary w-100" disabled={loading}>
                  {loading ? 'Registering...' : 'Register'}
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </>
  ); 
}
