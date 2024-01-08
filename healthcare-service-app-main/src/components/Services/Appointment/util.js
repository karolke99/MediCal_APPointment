export async function bookAppointment(appointment, formData) {
    try {
        const response = await fetch('https://fakeApi/appointment', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({...appointment, ...formData}),
        });

        if (!response.ok) {
            throw new Error('Failed to create appointment');
        }

        const result = await response.json();
        console.log('Appointment created successfully:', result);
        return result;
    } catch (error) {
        console.error('Error creating appointment:', error.message);
        throw error;
    }
}
