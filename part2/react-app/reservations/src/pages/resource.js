/**
 * Created by bugounet on 03/02/2020.
 */
import React, {useState, useEffect} from 'react';
import {useParams} from 'react-router-dom';
import {Calendar, momentLocalizer} from 'react-big-calendar';
import moment from 'moment';
import LoadingPage from '../components/LoadingPage';
import ErrorPage from '../components/ErrorPage';
import requestMiddleware from '../requestMiddleware';
import 'react-big-calendar/lib/css/react-big-calendar.css';

const localizer = momentLocalizer(moment);

const ResourcePage = () => {
    const { id: queryId } = useParams();
    const resourceId = Number(queryId);
    const [loading, setLoading] = useState(true);
    const [bookings, setBookings] = useState([]);
    const [error, setError] = useState("");

    const loadBookings = () => {
        setLoading(true);
        requestMiddleware.getBookingsForResource(resourceId).then((bookingsResponse) => {
            console.log(bookingsResponse.results);
            setBookings(bookingsResponse.results);
            setLoading(false);
        }).catch((error) => {
            console.error(error);
            setError(""+error);
            setLoading(false)
        });
    };

    // on page load: fetch resource's related bookings. When resourceId
    // changed, update this list.
    useEffect(() => loadBookings(), [resourceId]);

    if(loading) return <LoadingPage />;
    if(!!error) return <ErrorPage error={error} />;

    return (
        <div className="page">
            <Calendar
                localizer={localizer}
                events={bookings}
                startAccessor="start_datetime"
                endAccessor="end_datetime"
                titleAccessor="title"
            />
        </div>
    )
};

export default ResourcePage;
