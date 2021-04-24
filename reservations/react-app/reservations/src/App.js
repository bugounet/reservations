import React, {useState, useEffect} from 'react';
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import { w3cwebsocket as W3CWebSocket } from "websocket";
import ApplicationBar from './components/ApplicationBar';
import LeftSideMenu from './components/LeftSideMenu';
import MainPage from './pages/main';
import {
    AllBookingsPage,
    AllResourcesPage,
    BookingPage,
    ResourcePage,
} from './pages';
import { ThemeProvider } from '@material-ui/core/styles';
import theme from './theme';
import './App.css';

const client = new W3CWebSocket('ws://localhost:8001');

const SocketListener = () => {
    useEffect(() => {
        client.onopen = () => {
          console.log('WebSocket Client Connected');
        };
        client.onmessage = (message) => {
          console.log(message);
        };
    }, []);

}
function App() {
    const [menuState, setMenuState] = useState(false);
    const toggleSideMenu = () => {
        setMenuState(oldState => !oldState);
    };

    return (
        <AppConextProvider>
            <SocketListener />
            <ThemeProvider theme={theme}>
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
            </ThemeProvider>
        </AppConextProvider>
    );
}

export default App;
