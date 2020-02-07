/**
 * Created by bugounet on 06/02/2020.
 */
import React, {useState} from 'react';
import {TextField, Menu, List, ListItem, ListItemText} from '@material-ui/core';
import requestMiddleware from '../requestMiddleware';

const AutoCompletingResourceSelector = (props) => {
    // constants
    const {value: inputValue, onChange, label, name} = props;

    // state
    const [value, setValue] = useState(inputValue);
    const [editing, setEditing] = useState(false);
    const [resources, setResources] = useState([]);
    const [anchorEl, setAnchorEl] = React.useState(null);

    // Hooks & actions
    const activateInput = event => {
        setAnchorEl(event.currentTarget.parentElement);
        setEditing(true);
    };

    const exitInput = () => {
        setAnchorEl(null);
        setEditing(false);
    };

    const setNotFound = () => {
        setResources([{label:'Not found', id: null}]);
    };

    const chooseResource = (resource) => {
        setValue(resource.label);
        onChange({target:{
            value:resource.id,
            name: name
        }});
        exitInput();
    };

    const updateSearch = (event) => {
        const value = event.target.value;
        // skip with less than 3 results
        if (value.length < 3) return;
        // else search by location & type simultaneously
        Promise.all([
            requestMiddleware.findResourceByType(value),
            requestMiddleware.findResourceByLocation(value)
        ]).then(([typeResults, locationResults]) => {
            const allResults = typeResults.results.concat(
                locationResults.results
            );
            if (allResults.length)
                setResources(allResults);
            else
                setNotFound();
        }).catch(() => {
            setNotFound();
        })
    };

    //template helpers
    const resultsList = resources.map((resource) => (
        <ListItem key={resource.id}>
            <ListItemText onClick={() => chooseResource(resource)}>
                {resource.label}
                {(!!resource.id) && `(${resource.type}, ${resource.location})`}
            </ListItemText>
        </ListItem>
    ));

    //render
    return (
        <div>
            {(!editing) ? (
            <TextField
              label={label}
              name={name}
              value={value}
              onClick={activateInput}
              InputProps={{
                  readOnly: true,
              }}
            />
        ) : (
            <React.Fragment>
                <Menu
                    id="simple-menu"
                    anchorEl={anchorEl}
                    keepMounted
                    open={Boolean(anchorEl)}
                    onClose={exitInput}
                >
                    <TextField
                        label={label}
                        onChange={updateSearch}
                        name="search"/>
                    <List>
                        {resultsList}
                    </List>
                </Menu>
            </React.Fragment>
        )}
        </div>
    );
};
//This component must be documented...

export default AutoCompletingResourceSelector;