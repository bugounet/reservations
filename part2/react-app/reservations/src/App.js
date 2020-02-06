import React, {useState} from 'react';
import './App.css';
import ApplicationBar from './components/ApplicationBar';
import LeftSideMenu from './components/LeftSideMenu';
import MainPage from './pages/main';
import {
    AllBookingsPage,
    AllResourcesPage,
    BookingPage,
    ResourcePage,
} from './pages';
import {
  BrowserRouter as Router,
  Switch,
  Route
} from "react-router-dom";

function App() {
    const [menuState, setMenuState] = useState(false);
    const toggleSideMenu = () => {
        setMenuState(oldState => !oldState);
    };
    return (
        <Router>
            <ApplicationBar onClick={toggleSideMenu}/>
            <LeftSideMenu open={menuState} toggleDrawer={toggleSideMenu}/>
            <Switch>
                <Route path="/new-booking">
                    <BookingPage />
                </Route>
                <Route path="/booking/:id">
                    <BookingPage />
                </Route>
                <Route path="/bookings">
                    <AllBookingsPage />
                </Route>

                <Route path="/resource/:id">
                    <ResourcePage />
                </Route>
                <Route path="/resources">
                    <AllResourcesPage />
                </Route>

                <Route path="/">
                    <MainPage />
                </Route>
            </Switch>
        </Router>
    );
}

export default App;
