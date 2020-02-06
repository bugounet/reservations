/**
 * Created by bugounet on 05/02/2020.
 */
import React from 'react';
import {Link} from 'react-router-dom';
import { makeStyles, Theme, createStyles } from '@material-ui/core/styles';
import {Typography, Container, Button} from '@material-ui/core';

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    root: {
      display: 'flex',
      flexDirection: 'column',
    },
  }),
);

const ErrorPage = (props) => {
    const classes = useStyles();
    const {error} = props;
    return (
        <div className={classes.root+ " page"}>
            <Container>
                <Typography variant="h5">Uh oh!</Typography>
                <Typography variant="body1">{error}</Typography>
                <Button color="primary" variant="contained" component={Link} to="/">Go back home</Button>
            </Container>
        </div>
    )
};

export default ErrorPage;