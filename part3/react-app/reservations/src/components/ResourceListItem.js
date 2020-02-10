import React from 'react';
import {Link} from 'react-router-dom'
import TableCell from '@material-ui/core/TableCell';
import TableRow from '@material-ui/core/TableRow';

const ResourceListItem = (props) => {
    const {linkTo, resource} = props;
    const path = linkTo.replace(':id', resource.id);
    return (
        <TableRow>
            <TableCell>
                <Link to={path}>{resource.label}</Link>
            </TableCell>
        </TableRow>
    );
};

export default ResourceListItem;
