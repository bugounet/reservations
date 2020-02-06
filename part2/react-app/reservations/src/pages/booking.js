import React, {useState, useEffect} from 'react';
import {useParams, Redirect} from 'react-router-dom';
import moment from 'moment'
import {Paper, TextField, Button, Container, NativeSelect, makeStyles} from '@material-ui/core';
import LoadingPage from '../components/LoadingPage';
import ErrorPage from '../components/ErrorPage';
import requestMiddleware from "../requestMiddleware";

const useStyles = makeStyles(theme => ({
  container: {
    display: 'flex',
    flexDirection: 'column',
      paddingTop: 20,
      paddingBottom: 20,
  },
  textField: {
    width: 300,
    marginBottom: 10,
    display: 'block',
  },
}));

const BOOKING_KEYS = ['start_datetime', 'end_datetime', 'title', 'resource']

const BookingPage = (props) => {
    const classes = useStyles();
    const { id: queryId } = useParams();
    const bookingId = (queryId !== undefined) ? Number(queryId) : null;

    const [booking, setBooking] = useState(null);
    const [resources, setResources] = useState([]);
    const [error, setError] = useState("");
    const [redirect, setRedirect] = useState("");
    const [formMessages, setFormMessages] = useState("");
    const [loading, setLoading] = useState(true);
    const [modified, setModified] = useState(false);
    const [complete, setComplete] = useState(false);

    // load data on page first display
    useEffect(() => {
        // does not support IDs starting at 0. hopefully PgSQL or sqlite3 don't
        // start at 0.
        Promise.all([
            requestMiddleware.getResources(),
            ...((bookingId) ?
                [requestMiddleware.getBookingFromId(bookingId)] :
                [Promise.resolve({
                    title: '',
                    start_datetime: new Date(),
                    end_datetime: new Date(),
                    resource: null,
                })]
            )
        ]).then(([resourcesResponse, booking]) => {
            setResources(resourcesResponse.results);
            setBooking({
                ...booking,
                start_datetime: new Date(booking.start_datetime),
                end_datetime: new Date(booking.end_datetime),
            });
            setLoading(false);
        }).catch((error) => {
            setError("Something went wrong while getting this booking.");
            setLoading(false);
        });
    }, [bookingId]);

    // Edge cases: loading, error, redirect etc.
    if (loading) return <LoadingPage/>;
    if (!!error) return <ErrorPage error={error} />;
    if (!!redirect) return <Redirect to={redirect} />;

    // hooks
    const saveAction= () => {
        setLoading(true);
        if(bookingId !== null) {
            requestMiddleware.updateBooking(bookingId, booking).then(()=> {
                setModified(false);
                setLoading(false);
            }).catch(() => {
                setError("Couldn't modify this booking. Try again.");
                setLoading(false);
            });
        } else {
            requestMiddleware.createBooking(booking).then(() => {
                setRedirect('/bookings');
                setLoading(false);
            }).catch((error) => {
                setFormMessages(""+error);
                setLoading(false);
            });
        }
    };

    const onChange = (event) => {
        const {target } = event;
        booking[target.name] = target.value;

        const emptyFields = BOOKING_KEYS.map(
            key => !!(booking[key])
        ).filter(filled => !filled);

        setBooking({...booking});
        setModified(true);
        setComplete(emptyFields.length === 0);
    };

    // rendering helpers
    const allowSaveAction = (!!bookingId && modified) || (!bookingId && complete);
    const defaultStartDate = moment(
        (bookingId !== null) ? booking.start_datetime : new Date()
    ).format('YYYY-MM-DDTHH:mm');
    const defaultEndDate = moment(
        (bookingId !== null) ? booking.end_datetime : new Date()
    ).format('YYYY-MM-DDTHH:mm');
    const isEditable = !bookingId || moment(booking.end_datetime) > new Date();

    return (
        <div className="page">
            <Container>
                <Paper>
                    <Container>
                    <p>{(!!formMessages) && formMessages}</p>
                    <form className={classes.container}>
                        <TextField
                          required
                          id="filled-required"
                          label="Title"
                          name="title"
                          value={(!!booking) ? booking.title : ''}
                          className={classes.textField}
                          onChange={onChange}
                          InputProps={{
                              readOnly: !isEditable,
                          }}
                        />
                        <NativeSelect
                          value={booking.resource || ""}
                          onChange={onChange}
                          name="resource"
                          inputProps={{
                            name: 'resource',
                          }}
                        >
                          <option value="" />
                            {resources.map((resource)=> (
                                <option value={resource.id} key={resource.id}>{resource.label}</option>
                            ))}
                        </NativeSelect>
                        {
                            /* Could use sexy pickers but I want to ease my
                            dev so I would do it in an upcoming release */
                        }
                        <TextField
                            id="start_date"
                            label="Start date"
                            name="start_datetime"
                            type="datetime-local"
                            value={defaultStartDate}
                            className={classes.textField}
                            onChange={onChange}
                            InputLabelProps={{
                                shrink: true,
                                readOnly: !isEditable,
                            }}
                        />
                        <TextField
                            id="end_date"
                            label="End date"
                            name="end_datetime"
                            type="datetime-local"
                            value={defaultEndDate}
                            className={classes.textField}
                            onChange={onChange}
                            InputLabelProps={{
                                shrink: true,
                                readOnly: !isEditable
                            }}
                        />
                        {(isEditable) && (
                            <div>
                                <Button
                                    variant="contained"
                                    color={(allowSaveAction)? "primary" : "default"}
                                    onClick={saveAction}
                                    className={classes.submit}
                                    disabled={!allowSaveAction}
                                >
                                    { (bookingId !== null) ? 'Save' : 'Create' }
                                </Button>
                            </div>
                        )}
                    </form>
                    </Container>
                </Paper>
            </Container>
        </div>
    )
};

export default BookingPage;