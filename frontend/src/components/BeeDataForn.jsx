import React, { useState } from 'react';
import axios from 'axios';

const BeeDataForm = ({ onSuccess }) => {
  const [formData, setFormData] = useState({
    hive_id: '',
    temperature: '',
    humidity: '',
    location: '',
    notes: ''
  });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    try {
      await axios.post('http://localhost:8000/api/bee-data', {
        ...formData,
        temperature: parseFloat(formData.temperature),
        humidity: parseFloat(formData.humidity)
      });

      setMessage('Data added successfully!');
      setFormData({
        hive_id: '',
        temperature: '',
        humidity: '',
        location: '',
        notes: ''
      });
      
      if (onSuccess) onSuccess();
    } catch (error) {
      setMessage('Error adding data: ' + (error.response?.data?.detail || error.message));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <div className="card-header">
        <h3>Add New Bee Data</h3>
      </div>
      <div className="card-body">
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label htmlFor="hive_id" className="form-label">Hive ID *</label>
            <input
              type="text"
              className="form-control"
              id="hive_id"
              name="hive_id"
              value={formData.hive_id}
              onChange={handleChange}
              required
            />
          </div>

          <div className="mb-3">
            <label htmlFor="temperature" className="form-label">Temperature (°C) *</label>
            <input
              type="number"
              step="0.1"
              className="form-control"
              id="temperature"
              name="temperature"
              value={formData.temperature}
              onChange={handleChange}
              required
            />
          </div>

          <div className="mb-3">
            <label htmlFor="humidity" className="form-label">Humidity (%) *</label>
            <input
              type="number"
              step="0.1"
              className="form-control"
              id="humidity"
              name="humidity"
              value={formData.humidity}
              onChange={handleChange}
              required
            />
          </div>

          <div className="mb-3">
            <label htmlFor="location" className="form-label">Location</label>
            <input
              type="text"
              className="form-control"
              id="location"
              name="location"
              value={formData.location}
              onChange={handleChange}
            />
          </div>

          <div className="mb-3">
            <label htmlFor="notes" className="form-label">Notes</label>
            <textarea
              className="form-control"
              id="notes"
              name="notes"
              rows="3"
              value={formData.notes}
              onChange={handleChange}
            />
          </div>

          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? 'Adding...' : 'Add Data'}
          </button>
        </form>

        {message && (
          <div className={`alert ${message.includes('Error') ? 'alert-danger' : 'alert-success'} mt-3`}>
            {message}
          </div>
        )}
      </div>
    </div>
  );
};

export default BeeDataForm;