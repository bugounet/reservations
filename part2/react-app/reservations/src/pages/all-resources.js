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
import ErrorPage from '../components/ErrorPage';
import ResourceListItem from '../components/ResourceListItem';
import requestMiddleware from '../requestMiddleware';

const AllResourcesPage = () => {
    const pageSize = 10;
    const query = new URLSearchParams(useLocation().search);
    const [loading, setLoading] = useState(true);
    const [resources, setResources] = useState([]);
    const [count, setCount] = useState(0);
    const [page, setPage] = useState(0);
    const [error, setError] = useState("");

    const onPageChange = (event, newPage) => {
        setLoading(true);
        loadData(newPage);
    };

    const loadData = (page) => {
        requestMiddleware.getResources(page).then(resourcesResponse => {
            setResources(resourcesResponse.results);
            setCount(resourcesResponse.count);
            setPage(page);
            setLoading(false);
        }).catch(error => {
            setError(""+error);
            setLoading(false);
        })
    };

    useEffect(() => loadData(query.get('page') || 0), []);

    if (loading) return <LoadingPage />;
    if (!!error) return <ErrorPage error={error} />;

    const resourcesList = resources.map(
        resource => <ResourceListItem resource={resource} linkTo="/resource/:id" key={resource.id} />
    );

    return (
        <div className="page">
            <TableContainer component={Paper}>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>Label</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {resourcesList}
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
}
export default AllResourcesPage