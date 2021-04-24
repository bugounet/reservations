/**
 * Created by bugounet on 03/02/2020.
 */
import React, {useState, useEffect} from 'react';
import {useLocation} from "react-router-dom";
import Table from '@material-ui/core/Table';
import TablePagination from '@material-ui/core/TablePagination';
import TableBody from '@material-ui/core/TableBody';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableCell from '@material-ui/core/TableCell';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import LoadingPage from '../components/LoadingPage';
import BookingListItem from '../components/BookingListItem';
import requestMiddleware from "../requestMiddleware";

const transformInIdToResourceMap = (resources_list) => {
    return resources_list.map(
        resource => ({[resource.id]: resource})
    ).reduce(
        (item, aggregate) => ({...aggregate, ...item})
    );
};

const AllBookingsPage = () => {
    const query = new URLSearchParams(useLocation().search);
    const [bookings, setBookings] = useState([]);
    const [page, setPage] = useState(0);
    const [count, setCount] = useState(0);
    const [resourcesMapping, setResourcesMapping] = useState({});
    const [loading, setLoading] = useState(true);

    const pageSize = 10;
    const onPageChange = (event, newPage) => {
        setLoading(true);
        loadData(newPage);

    };
    const loadData = (page) => {
        Promise.all([
            requestMiddleware.getAllResources(),
            requestMiddleware.getBookings(page)
        ]).then(([resources, bookingsResponse])=> {
            setResourcesMapping(transformInIdToResourceMap(resources.results));
            setBookings(bookingsResponse.results);
            setCount(bookingsResponse.count);
            setPage(page);
            setLoading(false);
        });
    };

    // eslint-disable-next-line react-hooks/exhaustive-deps
    useEffect(() => loadData(query.get('page') || 0), []);
    if (loading) return <LoadingPage />;

    const bookingsList = bookings.map(
        booking => <BookingListItem booking={booking} resource={resourcesMapping[booking.resource]} linkTo="/booking/:id" key={booking.id} />
    );

    return (
        <div className="page">
            <TableContainer component={Paper}>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>Title</TableCell>
                            <TableCell align="right">Resource</TableCell>
                            <TableCell align="right">From</TableCell>
                            <TableCell align="right">To</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {bookingsList}
                        <TableRow>
                            <TablePagination
                                rowsPerPageOptions={[pageSize]}
                                count={count}
                                rowsPerPage={pageSize}
                                page={page}
                                onChangePage={onPageChange}
                            />
                        </TableRow>
                    </TableBody>
                </Table>
            </TableContainer>
        </div>
    );
};

export default AllBookingsPage