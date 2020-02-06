import React from 'react';
import { createStyles, makeStyles, Theme } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import IconButton from '@material-ui/core/IconButton';
import MenuIcon from '@material-ui/icons/Menu';

/* Sourced from material-ui demo app bars 
https://codesandbox.io/s/tc74g
*/
const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    root: {
      flexGrow: 1,
    },
    menuButton: {
      marginRight: theme.spacing(2),
    },
  }),
);

const ApplicationBar = (props) => {
	const classes = useStyles();
	const {onClick} = props;
	return (
		<AppBar position="static">
		  <Toolbar>
		    <IconButton edge="end" className={classes.menuButton} color="inherit" aria-label="menu" onClick={onClick}>
		      <MenuIcon />
		    </IconButton>
		    <Typography variant="h6" className={classes.title}>
		      {"Reservations"}
		    </Typography>
		  </Toolbar>
		</AppBar>
	);	
};

export default ApplicationBar;