import React, {useEffect, useState} from 'react';
import Dropdown from "../../common/dropdown";
import {getLocations, getSpecialistType} from '../../common/util';
import {get} from "lodash";

const AppointmentFilter = ({onFilterChange, filters}) => {
    const [startDate, setStartDate] = useState(get(filters, 'startDate'));
    const [endDate, setEndDate] = useState(get(filters, 'endDate'));
    const [clinicLocation, setClinicLocation] = useState(get(filters, 'clinicLocation'));
    const [selectedSpecialist, setSelectedSpecialist] = useState(get(filters, 'selectedSpecialist'));

    useEffect(() => {
        console.log('use filter');
        setStartDate(get(filters, 'startDate'));
        setEndDate(get(filters, 'endDate'));
        setClinicLocation(get(filters, 'clinicLocation'));
        setSelectedSpecialist(get(filters, 'selectedSpecialist'));
    }, [filters]);

    const handleFilterChange = () => {
        onFilterChange && onFilterChange({
            startDate,
            endDate,
            clinicLocation,
            selectedSpecialist
        });
    };

    const clearFilters = () => {
        setStartDate('');
        setEndDate('');
        setClinicLocation('');
        setSelectedSpecialist('');
        onFilterChange && onFilterChange({});
    };

    return (
        <div className='appointments__filter-Container'>
            <div className='appointments__filter-Container-group'>
                <div className='appointments__filter-Container-item'>
                    <label>Start Date:</label>
                    <input
                        type="date"
                        value={startDate}
                        onChange={(e) => setStartDate(e.target.value)}
                    />

                </div>
                <div className='appointments__filter-Container-item'>
                    <label>End Date:</label>
                    <input
                        type="date"
                        value={endDate}
                        onChange={(e) => setEndDate(e.target.value)}
                    />
                </div>
            </div>
            <div className='appointments__filter-Container-group'>
                <div className='appointments__filter-Container-item'>
                    <label>Clinic Location:</label>
                    <Dropdown
                        selected={clinicLocation}
                        changeSelectedItem={setClinicLocation}
                        elements={getLocations()}
                    />
                </div>
                <div className='appointments__filter-Container-item'>
                    <label>Specialist:</label>
                    <Dropdown
                        selected={selectedSpecialist}
                        changeSelectedItem={setSelectedSpecialist}
                        elements={getSpecialistType()}
                    />
                </div>
            </div>
            <div className='appointments__filter-Container-button-group'>
                <div></div>
                <button className={'appointments__filter-Container-button'} onClick={handleFilterChange}>Filter Appointments</button>
                <button className={'appointments__filter-Container-button'} onClick={clearFilters}>Clear Appointments</button>
            </div>
        </div>
    );
};

export default AppointmentFilter;
