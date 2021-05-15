import React, { ChangeEvent, ReactElement, useState } from 'react';
import {
  Button,
  CircularProgress,
  Container,
  FormControl,
  Grid,
  Link,
  makeStyles,
  TextField,
  Theme,
  Tooltip,
  Typography,
} from '@material-ui/core';
// eslint-disable-next-line import/no-named-as-default
import { AxiosError } from 'axios';
import { Link as RouterLink, useHistory } from 'react-router-dom';
import makeApiRequest, { RequestMethods } from '../../utils/apiClient';
import { Left, Nullable } from '../../utils/types';
import { camelizeKeys, reduceErrors, storeTokenPair } from '../../utils/general';

interface CreateUserSuccessPayload {
  token: {
    access: string;
    refresh: string;
  };
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
  loginRedirect: {
    marginTop: spacing(1),
  },
}));

export default function RegisterPage(): ReactElement {
  const [username, setUsername] = useState('');
  const [usernameError, setUsernameError] = useState<Nullable<string>>(null);

  const [password, setPassword] = useState('');
  const [passwordError, setPasswordError] = useState<Nullable<string>>(null);

  const [registrationToken, setRegistrationToken] = useState('');
  const [registrationTokenError, setRegistrationTokenError] = useState<Nullable<string>>(null);

  const [isLoading, setIsLoading] = useState(false);
  const history = useHistory();
  const classes = useStyles();

  const usernameHelperText =
    usernameError ??
    `Your display name. Can be anything.
  You can link your league account later.`;

  const passwordHelperText = passwordError ?? 'Must be at least 9 characters.';

  const tokenHelperText =
    registrationTokenError ??
    `The registration token provided to you by @TheCrimsonChin.
  If you do not have one, ping him on discord.`;

  const submitDisabled = !password || !username || !registrationToken || password.length < 9;

  const onUsernameChange = (event: ChangeEvent<HTMLInputElement>): void => {
    if (usernameError) {
      setUsernameError(null);
    }

    setUsername(event.target.value);
  };

  const onPasswordChange = (event: ChangeEvent<HTMLInputElement>): void => {
    if (passwordError) {
      setPasswordError(null);
    }

    setPassword(event.target.value);
  };

  const onTokenChange = (event: ChangeEvent<HTMLInputElement>): void => {
    if (registrationTokenError) {
      setRegistrationTokenError(null);
    }

    setRegistrationToken(event.target.value);
  };

  const handleErrors = (error: Error): void => {
    if ((error as AxiosError).isAxiosError) {
      const castError = error as AxiosError;

      if (castError.response?.status === 400) {
        const parsedResponse: {
          registrationToken?: Array<string>;
          username?: Array<string>;
          password?: Array<string>;
        } = camelizeKeys(castError.response?.data ?? {});

        if (parsedResponse.password) setPasswordError(reduceErrors(parsedResponse.password));

        if (parsedResponse.username) setUsernameError(reduceErrors(parsedResponse.username));

        if (parsedResponse.registrationToken) {
          setRegistrationTokenError(reduceErrors(parsedResponse.registrationToken));
        }
      }
    } else {
      // Either a custom error or something outside of axios. Throw it for error boundary to handle.
      throw error;
    }
  };

  const onSubmit = async (event: { preventDefault: () => void }): Promise<void> => {
    event.preventDefault();

    setIsLoading(true);

    const response = await makeApiRequest<CreateUserSuccessPayload>(
      RequestMethods.POST,
      'users/create',
      {
        registration_token: registrationToken,
        username,
        password,
      },
      {},
      { withAuthHeader: false }
    );

    if (response instanceof Left) {
      const error = response.unsafeUnwrap();

      console.error(error);

      handleErrors(error);
    } else {
      const { token: tokenPair } = response.unwrapOrThrow();

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
      const tooltipTitle = `username, password, and registration token cannot be empty
      and password must be at least 9 characters.`;

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
              Sign Up
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
        Sign Up
      </Button>
    );
  };

  return (
    <Container component="main" maxWidth="xs">
      <div className={classes.contentWrapper}>
        <Grid container justify="center">
          <Typography component="h1" variant="h5">
            Register
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
                  error={!!usernameError}
                  helperText={usernameHelperText}
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
                  error={!!passwordError}
                  helperText={passwordHelperText}
                  id="password"
                  label="Password"
                  type="password"
                  value={password}
                  variant="outlined"
                  onChange={onPasswordChange}
                />
              </FormControl>
            </Grid>
            <Grid item className={classes.formItem} xs={12}>
              <FormControl className={classes.formControl}>
                <TextField
                  required
                  aria-describedby="register-token-help-text"
                  error={!!registrationTokenError}
                  helperText={tokenHelperText}
                  id="register-token"
                  label="Registration Token"
                  type="text"
                  value={registrationToken}
                  variant="outlined"
                  onChange={onTokenChange}
                />
              </FormControl>
            </Grid>
          </Grid>
          {renderSubmitButton()}
        </form>
        <Grid container className={classes.loginRedirect} justify="center">
          <Grid item>
            <Typography variant="body2">
              Already have an account?{' '}
              <Link component={RouterLink} to="/login">
                Log In
              </Link>
              .
            </Typography>
          </Grid>
        </Grid>
      </div>
    </Container>
  );
}
