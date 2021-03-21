import React, { ReactElement, useRef, useState } from 'react';
import { Button, Grid, makeStyles, Menu, MenuItem, Theme } from '@material-ui/core';
import { useHistory } from 'react-router-dom';
import SettingsIcon from '@material-ui/icons/Settings';
import { Nullable } from '../utils/types';
import makeApiRequest, { RequestMethods } from '../utils/apiClient';
import { deleteStoredTokenPair } from '../utils/general';

const useStyles = makeStyles(({ spacing }: Theme) => ({
  container: {
    maxHeight: spacing(6),
    minHeight: spacing(6),
    height: '100%',
    padding: spacing(0.5, 0.5),
    marginBottom: spacing(2),
    alignContent: 'center',
  },
  settings: {
    display: 'flex',
    justifyContent: 'flex-end',
  },
  menuItem: {
    width: '100%',
  },
}));

export default function NavBar({ children }: { children: ReactElement }): ReactElement {
  const [anchorEl, setAnchorRef] = useState<Nullable<HTMLButtonElement>>(null);
  const buttonRef = useRef(null);

  const history = useHistory();
  const classes = useStyles();

  const onSettingsOpen = () => {
    /*
     * Due to using a button with an icon, if the user clicks on the svg the menu actually opens relative to the svg.
     * To fix this, we set the value of the anchorEl to a direct ref of the button. This way the menu always opens
     * relative to the button and not any of the icons/text.
     */
    setAnchorRef(buttonRef.current);
  };

  const onSettingsClose = () => {
    setAnchorRef(null);
  };

  const onLogoutClick = async () => {
    deleteStoredTokenPair();

    await makeApiRequest(
      RequestMethods.DELETE,
      'users/logout',
      { token: localStorage.getItem('refresh_token') },
      {},
      { withAuthHeader: true },
    );

    history.push('/login');
  };

  return (
    <React.Fragment>
      <Grid container className={classes.container} component="nav" justify="flex-end">
        <Grid item className={classes.settings} xs={1}>
          <Button
            ref={buttonRef}
            aria-haspopup
            aria-controls="settings-menu"
            color="default"
            startIcon={<SettingsIcon />}
            variant="contained"
            onClick={onSettingsOpen}
          >
            Settings
          </Button>
          <Menu
            keepMounted
            anchorEl={buttonRef.current}
            anchorOrigin={{ vertical: 'bottom', horizontal: 'left' }}
            getContentAnchorEl={null} // Needed in order to be able to use anchorOrigin
            id="settings-menu"
            open={!!anchorEl}
            onClose={onSettingsClose}
          >
            <MenuItem onClick={onLogoutClick}>Logout</MenuItem>
          </Menu>
        </Grid>
      </Grid>
      {children}
    </React.Fragment>
  );
}
