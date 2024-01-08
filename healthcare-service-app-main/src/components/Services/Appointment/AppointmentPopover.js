import React, {useState} from 'react';
import './appointments.scss';
import isEmpty from "lodash/isEmpty";

const PopoverAppointment = ({ appointment, setSelectedAppointment, onBook }) => {

    const [formData, setFormData] = useState({
        name: '',
        lastname: '',
        birthday: '',
        insuranceNumber: '',
        paymentMethod: '',
    });

    if (isEmpty(appointment)) {
        return <div/>;
    }

    const handleTogglePopover = () => {
        setSelectedAppointment && setSelectedAppointment(null);
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData((prevData) => ({ ...prevData, [name]: value }));
    };

    return (
        <div className="popover-appointment">
            <button className="popover-trigger" onClick={handleTogglePopover}>
                View Appointment
            </button>
            <div className="popover-content">
                <button className="close-button" onClick={handleTogglePopover}>
                    X
                </button>
                <h3>{appointment.specialist}</h3>
                <p>Date: {appointment.date}</p>
                <p>Location: {appointment.clinicLocation}</p>

                <form>
                    <label>
                        Name:
                        <input type="text" name="name" value={formData.name} onChange={handleChange} />
                    </label>
                    <label>
                        Lastname:
                        <input type="text" name="lastname" value={formData.lastname} onChange={handleChange} />
                    </label>
                    <label>
                        Birthday:
                        <input type="text" name="birthday" value={formData.birthday} onChange={handleChange} />
                    </label>
                    <label>
                        Insurance Number:
                        <input type="text" name="insuranceNumber" value={formData.insuranceNumber} onChange={handleChange} />
                    </label>
                    <label>
                        Payment Method:
                        <input type="text" name="paymentMethod" value={formData.paymentMethod} onChange={handleChange} />
                    </label>
                </form>

                <button className="book-button" onClick={() => onBook(formData)}>Book Now</button>
            </div>
        </div>
    );
};

export default PopoverAppointment;
