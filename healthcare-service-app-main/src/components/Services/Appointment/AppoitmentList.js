import React from 'react';
import './appointments.scss';

const AppointmentList = ({ appointments }) => {
    return (
        <div className="appointment-list">
            <h2>Appointment List</h2>
            <ul>
                {appointments.map((appointment, index) => (
                    <li key={index} className="appointment-item">
                        <div className="appointment-details">
                            <h3>{appointment.title}</h3>
                            <p>{appointment.date}</p>
                            <p>{appointment.location}</p>
                        </div>
                        <div className="appointment-actions">
                            <button>View</button>
                        </div>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default AppointmentList;
