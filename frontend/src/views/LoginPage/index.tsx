import React, { ChangeEvent, ReactElement, useState } from 'react';
import {
  Button,
  CircularProgress,
  Container,
  FormControl,
  FormHelperText,
  Grid,
  Link,
  makeStyles,
  TextField,
  Theme,
  Tooltip,
  Typography,
} from '@material-ui/core';
import { Link as RouterLink, useHistory } from 'react-router-dom';
import { AxiosError } from 'axios';
import makeApiRequest, { RequestMethods } from '../../utils/apiClient';
import { Left, Nullable } from '../../utils/types';
import { storeTokenPair } from '../../utils/general';

interface LoginSuccessPayload {
  access: string;
  refresh: string;
}

const useStyles = makeStyles(({ spacing }: Theme) => ({
  contentWrapper: {
    marginTop: spacing(8),
  },
  form: {
    width: '100%',
    marginTop: spacing(2),
  },
  formItem: {
    width: '100%',
    marginTop: spacing(2),
  },
  formControl: {
    width: '100%',
  },
  submit: {
    margin: spacing(2, 0),
  },
  formErrorText: {
    marginTop: spacing(2),
  },
  registerRedirect: {
    marginTop: spacing(1),
  },
}));

export default function LoginPage(): ReactElement {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [formError, setFormError] = useState<Nullable<string>>(null);
  const [error, setError] = useState<Nullable<Error>>(null);
  const [isLoading, setIsLoading] = useState(false);
  const history = useHistory();
  const classes = useStyles();

  if (error) throw error;

  const onUsernameChange = (event: ChangeEvent<HTMLInputElement>): void => {
    if (formError) {
      setFormError(null);
    }

    setUsername(event.target.value);
  };
  const onPasswordChange = (event: ChangeEvent<HTMLInputElement>): void => {
    if (formError) {
      setFormError(null);
    }

    setPassword(event.target.value);
  };

  const submitDisabled = !username || !password;

  const onSubmit = async (event: { preventDefault: () => void }): Promise<void> => {
    event.preventDefault();

    setIsLoading(true);

    const response = await makeApiRequest<LoginSuccessPayload>(
      RequestMethods.POST,
      'users/login',
      {
        username,
        password,
      },
      {},
      { withAuthHeader: false }
    );

    if (response instanceof Left) {
      const err = response.unsafeUnwrap();

      if ((err as AxiosError).isAxiosError) {
        setFormError('Invalid username and password combination.');
      } else {
        // Something else, job for the ErrorBoundary.
        setError(err);
      }
    } else {
      const tokenPair = response.unwrapOrThrow();

      storeTokenPair(tokenPair);

      history.push('/');

      return;
    }

    setIsLoading(false);
  };

  const renderSubmitButton = () => {
    if (isLoading) {
      return (
        <Grid container justify="center">
          <CircularProgress className={classes.submit} />
        </Grid>
      );
    }

    if (submitDisabled) {
      const tooltipTitle = 'username and password are required.';

      return (
        <Tooltip arrow title={tooltipTitle}>
          <span>
            <Button
              disabled
              fullWidth
              className={classes.submit}
              color="primary"
              type="submit"
              variant="contained"
              onClick={onSubmit}
            >
              Log In
            </Button>
          </span>
        </Tooltip>
      );
    }

    return (
      <Button
        fullWidth
        className={classes.submit}
        color="primary"
        type="submit"
        variant="contained"
        onClick={onSubmit}
      >
        Log In
      </Button>
    );
  };

  return (
    <Container component="main" maxWidth="xs">
      <div className={classes.contentWrapper}>
        <Grid container justify="center">
          <Typography component="h1" variant="h5">
            Log In
          </Typography>
        </Grid>
        <form noValidate className={classes.form}>
          <Grid container alignItems="center" direction="column">
            <Grid item className={classes.formItem} xs={12}>
              <FormControl className={classes.formControl}>
                <TextField
                  autoFocus
                  required
                  aria-describedby="username-help-text"
                  error={!!formError}
                  id="username"
                  label="Username"
                  type="text"
                  value={username}
                  variant="outlined"
                  onChange={onUsernameChange}
                />
              </FormControl>
            </Grid>
            <Grid item className={classes.formItem} xs={12}>
              <FormControl className={classes.formControl}>
                <TextField
                  required
                  aria-describedby="password-help-text"
                  error={!!formError}
                  id="password"
                  label="Password"
                  type="password"
                  value={password}
                  variant="outlined"
                  onChange={onPasswordChange}
                />
              </FormControl>
            </Grid>
          </Grid>
          {!!formError && <FormHelperText className={classes.formErrorText}>{formError}</FormHelperText>}
          {renderSubmitButton()}
        </form>
        <Grid container className={classes.registerRedirect} justify="center">
          <Grid item>
            <Typography variant="body2">
              Need an account?{' '}
              <Link component={RouterLink} to="/register">
                Register
              </Link>
              .
            </Typography>
          </Grid>
        </Grid>
      </div>
    </Container>
  );
}
