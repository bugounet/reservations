import React from 'react';
import {Link} from 'react-router-dom'
import TableCell from '@material-ui/core/TableCell';
import TableRow from '@material-ui/core/TableRow';

const BookingListItem = (props) => {
    const {linkTo, booking, resource} = props;
    const path = linkTo.replace(':id', booking.id);
    const resourceName = (!!resource) ? resource.label : "";
    return (
        <TableRow>
            <TableCell>
                <Link to={path}>{booking.title}</Link>
            </TableCell>
            <TableCell align="right">
                {resourceName}
            </TableCell>
            <TableCell align="right">
                {booking.start_datetime.toLocaleString()}
            </TableCell>
            <TableCell align="right">
                {booking.end_datetime.toLocaleString()}
            </TableCell>
        </TableRow>
    );
};

export default BookingListItem;
