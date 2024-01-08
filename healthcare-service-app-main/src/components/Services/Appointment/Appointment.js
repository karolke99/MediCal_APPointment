import { Box, Container } from '@mui/material';
import React, {useMemo, useState} from 'react';
import useAuth from '../../../Hooks/useAuth';
import AppointmentFilter from "./AppoitmentFilter";
import AppointmentList from "./AppoitmentList";
import useAppointmentFetcher from "../../../Hooks/useAppoitmnetFetcher";
import isEmpty from 'lodash/isEmpty';
import moment from 'moment';
import {isEqual} from "lodash";
import "./appointments.scss";

const filterAppointments = (appointments, filters) => {
    const {
        startDate,
        endDate,
        specialist,
        clinicLocation
    } = filters;

    return appointments.filter(appointment => {

        if (!isEmpty(startDate)) {
            if (moment(startDate).isAfter(moment(appointment.date))) {
                return false;
            }
        }

        if (!isEmpty(endDate)) {
            if (moment(endDate).isBefore(moment(appointment.date))) {
                return false;
            }
        }

        if (!isEmpty(specialist)) {
            if (!isEqual(specialist, appointment.specialist)) {
                return false;
            }
        }

        if (!isEmpty(clinicLocation)) {
            if (!isEqual(clinicLocation, appointment.clinicLocation)) {
                return false;
            }
        }

        return true;
    });
}


const Appointment = () => {
    // const { user } = useAuth();
    const { appointments } = useAppointmentFetcher();
    const [filters, setFilters] = useState({})

    const filteredAppointments = useMemo(() => {
        return filterAppointments(appointments, filters);
    }, [appointments, filters]);

    return (
        <Box id='appointment'
             className='appointments'
            sx={{
                display: 'flex',
                flexDirection: 'column',
                minHeight: '100vh',
            }}>
            <Container maxWidth="xl">
                <h6>Select your time and data for Appointment</h6>
                <AppointmentFilter
                    onFilterChange={setFilters}
                    filters={filters}
                />
                <AppointmentList
                    appointments={filteredAppointments}
                />
            </Container>
        </Box>
    );
};

export default Appointment;