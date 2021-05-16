import React, { ChangeEvent, ReactElement, useState } from 'react';
import {
  Button,
  CircularProgress,
  Container,
  FormControl,
  FormHelperText,
  Grid,
  makeStyles,
  TextField,
  Theme,
  Tooltip,
} from '@material-ui/core';
import { AxiosError } from 'axios';
import { useSnackbar } from 'notistack';
import { Left, Nullable } from '../utils/types';
import makeApiRequest, { RequestMethods } from '../utils/apiClient';

const useStyles = makeStyles(({ spacing }: Theme) => ({
  contentWrapper: {
    marginTop: spacing(2),
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
}));

export default function PasswordChangeForm(): ReactElement {
  const [oldPassword, setOldPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [passwordConfirmation, setPasswordConfirmation] = useState('');
  const [formError, setFormError] = useState<Nullable<string>>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [unhandledError, setUnhandledError] = useState<Nullable<Error>>(null);
  const { enqueueSnackbar } = useSnackbar();
  const classes = useStyles();

  const submitDisabled = newPassword !== passwordConfirmation || newPassword.length < 9 || !oldPassword;

  const onOldPasswordChange = (event: ChangeEvent<HTMLInputElement>) => {
    if (formError) setFormError(null);

    setOldPassword(event.target.value);
  };

  const onNewPasswordChange = (event: ChangeEvent<HTMLInputElement>) => {
    if (formError) setFormError(null);

    setNewPassword(event.target.value);
  };

  const onPasswordConfirmationChange = (event: ChangeEvent<HTMLInputElement>) => {
    if (formError) setFormError(null);

    setPasswordConfirmation(event.target.value);
  };

  const onSubmit = async (event: { preventDefault: () => void }): Promise<void> => {
    event.preventDefault();

    setIsLoading(true);

    const response = await makeApiRequest<string>(
      RequestMethods.PUT,
      'users/change_password',
      {
        old_password: oldPassword,
        new_password: newPassword,
        new_password_confirmation: passwordConfirmation,
      },
      {}
    );

    if (response instanceof Left) {
      const error = response.unsafeUnwrap();

      if ((error as AxiosError).isAxiosError) {
        setFormError('Failed to change password.');
      } else {
        // Something else, job for the ErrorBoundary.
        setUnhandledError(error);
      }
    } else {
      enqueueSnackbar('Password successfully changed.', {
        variant: 'success',
      });
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
      const tooltipTitle = 'Passwords must match, and be at least 9 characters long. Old password is required.';

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
              Change Password
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
        Submit
      </Button>
    );
  };

  if (unhandledError !== null) throw unhandledError;

  return (
    <Container className={classes.contentWrapper} maxWidth="xs">
      <form noValidate className={classes.form}>
        <Grid container alignItems="center" direction="column">
          <Grid item className={classes.formItem} xs={12}>
            <FormControl className={classes.formControl}>
              <TextField
                autoFocus
                required
                error={!!formError}
                id="old-password"
                label="Old Password"
                type="password"
                value={oldPassword}
                variant="outlined"
                onChange={onOldPasswordChange}
              />
            </FormControl>
          </Grid>
          <Grid item className={classes.formItem} xs={12}>
            <FormControl className={classes.formControl}>
              <TextField
                autoFocus
                required
                error={!!formError}
                id="new-password"
                label="New Password"
                type="password"
                value={newPassword}
                variant="outlined"
                onChange={onNewPasswordChange}
              />
            </FormControl>
          </Grid>
          <Grid item className={classes.formItem} xs={12}>
            <FormControl className={classes.formControl}>
              <TextField
                required
                error={!!formError}
                id="password-confirm"
                label="Confirm Password"
                type="password"
                value={passwordConfirmation}
                variant="outlined"
                onChange={onPasswordConfirmationChange}
              />
            </FormControl>
          </Grid>
        </Grid>
        {!!formError && <FormHelperText className={classes.formErrorText}>{formError}</FormHelperText>}
        {renderSubmitButton()}
      </form>
    </Container>
  );
}
