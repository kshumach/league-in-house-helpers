import React, { ReactElement, useMemo } from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import useMediaQuery from '@material-ui/core/useMediaQuery';
import { createMuiTheme, ThemeProvider } from '@material-ui/core/styles';
import CssBaseline from '@material-ui/core/CssBaseline';
import RegisterPage from '../RegisterPage';
import HomePage from '../HomePage';
import { UserContextProvider } from '../../context/user';
import ErrorBoundary from '../../components/ErrorBoundary';
import RedirectIfLoggedIn from '../../components/guards/RedirectIfLoggedIn';
import LoginPage from '../LoginPage';

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
            <Route path="/">
              <UserContextProvider handleErrors>
                <HomePage />
              </UserContextProvider>
            </Route>
          </Switch>
        </BrowserRouter>
      </ErrorBoundary>
    </ThemeProvider>
  );
}
