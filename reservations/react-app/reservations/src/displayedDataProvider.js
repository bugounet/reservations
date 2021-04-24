/**
 * Created by bugounet on 19/07/2019.
 */
import React, { Component } from 'react';

export const DisplayedDataContext = React.createContext({});

const DisplayedDataContextProvider = (props) => {

    const [displayedBooking, setDisplayedBooking] = useState(null);
    const [displayedResource, setDisplayedResource] = useState(null);
    const [reloadView, setReloadingEvent] = useState(null);
    const {children} = props;
    const onSocketEvent = (data) => {
        const [modifiedBookingId, modifiedResourceId, ...other] = data.split("//");
        if (modifiedBookingId === displatedBooking || modifiedResourceId === displayedResource) {
            if (reloadView) reloadView();
        }
    }
    return (
        <DisplayedDataContext.Provider
            value={{
                displayedBooking,
                displayedResource,
                setDisplayedBooking,
                setDisplayedResource,
                onSocketEvent,
                setReloadingEvent,
            }}
        >
            {children}
        </DisplayedDataContext.Provider>
    );
};

export default DisplayedDataContextProvider;
