import React, { forwardRef, ReactElement, RefObject, useMemo, useRef, useState } from 'react';
import { Button, Grid, makeStyles, Menu, MenuItem, Theme } from '@material-ui/core';
import { Link, LinkProps, useHistory } from 'react-router-dom';
import AccountCircle from '@material-ui/icons/AccountCircle';
import HomeIcon from '@material-ui/icons/Home';
import PollIcon from '@material-ui/icons/Poll';
import { Nullable } from '../utils/types';
import makeApiRequest, { RequestMethods } from '../utils/apiClient';
import { deleteStoredTokenPair } from '../utils/general';
import { RANKINGS_PATH, HOME_PATH } from '../utils/paths';

const useStyles = makeStyles(({ spacing }: Theme) => ({
  container: {
    maxHeight: spacing(6),
    minHeight: spacing(6),
    height: '100%',
    padding: spacing(0.5, 0.5),
    marginBottom: spacing(8),
    alignContent: 'center',
  },
  settings: {
    display: 'flex',
    justifyContent: 'flex-end',
    marginLeft: 'auto',
  },
  home: {
    marginRight: 'auto',
  },
  sharedRight: {
    marginRight: spacing(0),
  },
  sharedLeft: {
    marginLeft: spacing(0),
  },
  navItems: {
    marginRight: 'auto',
    marginLeft: 'auto',
  },
}));

interface NavItemProps {
  to: string;
  icon: ReactElement;
  children: string;
}

function NavItem(props: NavItemProps) {
  const { to, icon, children } = props;

  const renderLink = useMemo(
    () =>
      // eslint-disable-next-line react/display-name
      forwardRef<unknown, Omit<LinkProps, 'to'>>((itemProps, ref) => (
        // eslint-disable-next-line react/jsx-props-no-spreading
        <Link ref={ref as RefObject<HTMLAnchorElement>} to={to} {...itemProps} />
      )),
    [to]
  );

  return (
    <Button color="default" component={renderLink} startIcon={icon}>
      {children}
    </Button>
  );
}

export default function NavBar({ children }: { children: ReactElement[] }): ReactElement {
  const [anchorEl, setAnchorRef] = useState<Nullable<HTMLButtonElement>>(null);
  const buttonRef = useRef(null);

  const history = useHistory();
  const classes = useStyles();

  const onAccountOpen = () => {
    /*
     * Due to using a button with an icon, if the user clicks on the svg the menu actually opens relative to the svg.
     * To fix this, we set the value of the anchorEl to a direct ref of the button. This way the menu always opens
     * relative to the button and not any of the icons/text.
     */
    setAnchorRef(buttonRef.current);
  };

  const onAccountClose = () => {
    setAnchorRef(null);
  };

  const onLogoutClick = async () => {
    deleteStoredTokenPair();

    await makeApiRequest(
      RequestMethods.DELETE,
      'users/logout',
      { token: localStorage.getItem('refresh_token') },
      {},
      { withAuthHeader: true }
    );

    return history.push('/login');
  };

  const onSettingsClick = () => history.push('/settings');

  return (
    <React.Fragment>
      <Grid container className={classes.container} component="nav" justify="flex-end">
        <Grid item className={classes.home} xs={1}>
          <NavItem icon={<HomeIcon />} to={HOME_PATH}>
            Home
          </NavItem>
        </Grid>
        <Grid item className={classes.navItems} xs={1}>
          <NavItem icon={<PollIcon />} to={RANKINGS_PATH}>
            Rankings
          </NavItem>
        </Grid>
        <Grid item className={classes.settings} xs={1}>
          <Button
            ref={buttonRef}
            aria-haspopup
            aria-controls="settings-menu"
            color="default"
            startIcon={<AccountCircle />}
            // variant="contained"
            onClick={onAccountOpen}
          >
            Account
          </Button>
          <Menu
            keepMounted
            anchorEl={buttonRef.current}
            anchorOrigin={{ vertical: 'bottom', horizontal: 'left' }}
            getContentAnchorEl={null} // Needed in order to be able to use anchorOrigin
            id="settings-menu"
            open={!!anchorEl}
            onClose={onAccountClose}
          >
            <MenuItem onClick={onSettingsClick}>Settings</MenuItem>
            <MenuItem onClick={onLogoutClick}>Logout</MenuItem>
          </Menu>
        </Grid>
      </Grid>
      {children}
    </React.Fragment>
  );
}
