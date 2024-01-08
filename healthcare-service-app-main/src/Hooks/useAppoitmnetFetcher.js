import { useState, useEffect } from 'react';
// import axios from 'axios';

const useAppointmentFetcher = () => {
    const [loading, setLoading] = useState(true);
    const [appointments, setAppointments] = useState([]);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = [
                    {
                        "id": 1,
                        "specialist": "Dr. Smith",
                        "clinicLocation": "Medical Center A",
                        "date": "2022-07-15T10:00:00Z"
                    },
                    {
                        "id": 2,
                        "specialist": "Dr. Johnson",
                        "clinicLocation": "Medical Center B",
                        "date": "2022-07-16T14:30:00Z"
                    },
                    {
                        "id": 3,
                        "specialist": "Dr. Brown",
                        "clinicLocation": "Medical Center A",
                        "date": "2022-07-17T09:15:00Z"
                    },
                    {
                        "id": 4,
                        "specialist": "Dr. Davis",
                        "clinicLocation": "Medical Center C",
                        "date": "2022-07-18T11:45:00Z"
                    },
                    {
                        "id": 5,
                        "specialist": "Dr. Wilson",
                        "clinicLocation": "Medical Center B",
                        "date": "2022-07-19T13:20:00Z"
                    }
                ];

                // await axios.get('https://fakeApi/appointments');
                // const fetchedAppointments = response.data;

                setAppointments(response);
            } catch (error) {
                setError(error);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    return { loading, appointments, error };
};

export default useAppointmentFetcher;
