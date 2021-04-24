import React from 'react';
import {Link} from 'react-router-dom'
import { makeStyles } from '@material-ui/core/styles';
import Drawer from '@material-ui/core/Drawer';
import List from '@material-ui/core/List';
import Divider from '@material-ui/core/Divider';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';

const useStyles = makeStyles({
  list: {
    width: 250,
  },
  fullList: {
    width: 'auto',
  },
});

const MenuContent = (props) => {
	const classes = useStyles();
	const {toggleDrawer} = props;
	return (
	    <div
	      className={classes.list}
	      role="presentation"
	    >
			<List>
			  	<ListItem component={Link} to='/resources' key='resources' onClick={toggleDrawer}>
					<ListItemText primary="Resources" />
			    </ListItem>
				<ListItem component={Link} to='/bookings' key='bookings' onClick={toggleDrawer}>
					<ListItemText primary="Bookings" />
				</ListItem>
				<ListItem component={Link} to='/new-booking' key='new-booking' onClick={toggleDrawer}>
					<ListItemText primary="Book Something" />
				</ListItem>
			</List>
			<Divider />
			<List>
				<ListItem onClick={()=> window.location = '/logout'} key="logout">
					<ListItemText primary="Logout" />
				</ListItem>
			</List>
	    </div>
	);
}


const LeftSideMenu = (props) => {
	const {open, toggleDrawer} = props;
	return (
		<Drawer open={open}>
  			<MenuContent toggleDrawer={toggleDrawer}/>
		</Drawer>
	);
};

export default LeftSideMenu;