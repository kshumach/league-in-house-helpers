import React, { ReactElement, useMemo } from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import useMediaQuery from '@material-ui/core/useMediaQuery';
import { createMuiTheme, ThemeProvider } from '@material-ui/core/styles';
import CssBaseline from '@material-ui/core/CssBaseline';
import { SnackbarProvider } from 'notistack';
import RegisterPage from '../RegisterPage';
import HomePage from '../HomePage';
import { UserContextProvider } from '../../context/user';
import ErrorBoundary from '../../components/ErrorBoundary';
import RedirectIfLoggedIn from '../../components/guards/RedirectIfLoggedIn';
import LoginPage from '../LoginPage';
import NavBar from '../../components/NavBar';
import ErrorHandler from '../../components/ErrorHandler';
import { NoRouteMatchError } from '../../utils/errors';
import SettingsPage from '../SettingsPage';
import RankingsPage from '../RankingsPage';

export default function App(): ReactElement {
  const prefersDarkMode = useMediaQuery('(prefers-color-scheme: dark)');

  const theme = useMemo(
    () =>
      createMuiTheme({
        palette: {
          type: prefersDarkMode ? 'dark' : 'light',
        },
      }),
    [prefersDarkMode]
  );

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <SnackbarProvider
        anchorOrigin={{
          vertical: 'top',
          horizontal: 'center',
        }}
        maxSnack={3}
        resumeHideDuration={0}
      >
        <ErrorBoundary>
          <BrowserRouter basename="">
            <Switch>
              <Route exact path="/register">
                <RedirectIfLoggedIn to="/">
                  <RegisterPage />
                </RedirectIfLoggedIn>
              </Route>
              <Route exact path="/login">
                <RedirectIfLoggedIn to="/">
                  <LoginPage />
                </RedirectIfLoggedIn>
              </Route>
              <UserContextProvider handleErrors>
                <NavBar>
                  <Route exact path="/">
                    <HomePage />
                  </Route>
                  <Route exact path="/settings">
                    <SettingsPage />
                  </Route>
                  <Route exact path="/rankings">
                    <RankingsPage />
                  </Route>
                </NavBar>
              </UserContextProvider>
              <Route path="*">
                <ErrorHandler error={new NoRouteMatchError()} />
              </Route>
            </Switch>
          </BrowserRouter>
        </ErrorBoundary>
      </SnackbarProvider>
    </ThemeProvider>
  );
}
