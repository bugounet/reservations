/**
 * Created by bugounet on 06/02/2020.
 */
class requestMiddleware {
    constructor(auth, username) {
        this.auth = auth;
        this.userName = username;
    };

    castServerResponseToRelevantFormat(booking) {
        if(booking.resource) {
            booking.resource = Number(
                booking.resource.match(/resource\/(\d+)/)[1]
            );
        }
        booking.start_datetime = new Date(booking.start_datetime);
        booking.end_datetime = new Date(booking.end_datetime);
        return booking;
    };

    getBookings(page) {
        return fetch(
            `http://localhost:8000/api/booking/?offset=${page*10}`,
            {
                headers: {
                    Authorization: this.auth
                }
            }
        ).then((response) => response.json()).then((responseData) => {
            return {
                ...responseData,
                results: responseData.results.map(
                    this.castServerResponseToRelevantFormat
                )
            };
        });
    };

    updateBooking(bookingId, data) {
        return fetch(
            `http://localhost:8000/api/booking/${bookingId}/`,
            {
                headers: {
                    Authorization: this.auth,
                    'Content-Type': 'application/json',
                },
                method: 'PUT',
                body: JSON.stringify(data)
            }
        ).then((response) => response.json()).then(
            data => this.castServerResponseToRelevantFormat(data)
        );
    };

    createBooking(data) {
        data.owner_name = this.userName;
        data.resource = `/api/resource/${data.resource}/`;
        return fetch(
            'http://localhost:8000/api/booking/',
            {
                headers: {
                    Authorization: this.auth,
                    'Content-Type': 'application/json',
                },
                method: 'POST',
                body: JSON.stringify(data)
            }
        ).then((response) => response.json()).then(
            data => this.castServerResponseToRelevantFormat(data)
        );
    };

    getBookingFromId(bookingId) {
        return fetch(
            `http://localhost:8000/api/booking/${bookingId}/`,
            {
                headers: {
                    Authorization: this.auth
                }
            }
        ).then((response) => response.json()).then(
            data => this.castServerResponseToRelevantFormat(data)
        );
    };

    getAllResources() {
        return this.getResources(0, 0);
    };

    getResources(page, limit=10) {
        return fetch(
            `http://localhost:8000/api/resource/?offset=${page*10}&limit=${limit}`,
            {
                headers: {
                    Authorization: this.auth
                }
            }
        ).then((response) => response.json());
    };

    getBookingsForResource(resourceId) {
        return fetch(
            // Not the best performance, but I'm not comfortable with
            // react-big-calendar. else I'd request with a date interval.
            // Here I grab all Bookings no matter what.
            `http://localhost:8000/api/resource/${resourceId}/bookings/?offset=0&limit=0`,
            {
                headers: {
                    Authorization: this.auth
                }
            }
        ).then((response) => response.json()).then((responseData) => {
            return {
                ...responseData,
                results: responseData.results.map(
                    this.castServerResponseToRelevantFormat
                )
            };
        });
    }
};

export default new requestMiddleware('Basic YWRtaW46TXlBZG1pbjEyMyE=', 'admin')