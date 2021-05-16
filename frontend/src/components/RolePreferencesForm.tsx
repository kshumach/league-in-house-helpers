import React, { ReactElement, useState } from 'react';
import {
  Button,
  CircularProgress,
  Container,
  FormControl,
  FormHelperText,
  Grid,
  InputLabel,
  makeStyles,
  MenuItem,
  Select,
  Theme,
  Tooltip,
} from '@material-ui/core';
import { useSnackbar } from 'notistack';
import { AxiosError } from 'axios';
import { useUserContext } from '../context/user';
import { Left, Nullable, Role } from '../utils/types';
import { coalesce } from '../utils/general';
import makeApiRequest, { RequestMethods } from '../utils/apiClient';

const useStyles = makeStyles(({ spacing }: Theme) => ({
  contentWrapper: {
    marginTop: spacing(4),
  },
  form: {
    width: '100%',
    marginTop: spacing(2),
  },
  formItem: {
    width: '100%',
    marginTop: spacing(2),
    marginBottom: spacing(2),
  },
  formControl: {
    width: '100%',
  },
  submit: {
    margin: spacing(2, 0),
  },
  formErrorText: {
    marginTop: spacing(4),
  },
  hidden: {
    display: 'none',
  },
}));

const allAvailableRoles = [Role.TOP, Role.JUNGLE, Role.MID, Role.MARKSMAN, Role.SUPPORT];

export default function RolePreferencesForm(): ReactElement {
  const { user } = useUserContext();
  const [primaryRole, setPrimaryRole] = useState(coalesce<string>(user?.preferredRoles?.primaryRole, ''));
  const [secondaryRole, setSecondaryRole] = useState(coalesce<string>(user?.preferredRoles?.secondaryRole, ''));
  const [offRole, setOffRole] = useState(coalesce<string>(user?.preferredRoles?.offRole, ''));
  const [formError, setFormError] = useState<Nullable<string>>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [hasMadeChange, setHasMadeChange] = useState(false);
  const [unhandledError, setUnhandledError] = useState<Nullable<Error>>(null);
  const { enqueueSnackbar } = useSnackbar();
  const classes = useStyles();

  const onPrimaryRoleChange = (event: React.ChangeEvent<{ value: unknown }>) => {
    setPrimaryRole(event.target.value as string);
    setHasMadeChange(true);
  };

  const onSecondaryRoleChange = (event: React.ChangeEvent<{ value: unknown }>) => {
    setSecondaryRole(event.target.value as string);
    setHasMadeChange(true);
  };

  const onOffRoleChange = (event: React.ChangeEvent<{ value: unknown }>) => {
    setOffRole(event.target.value as string);
    setHasMadeChange(true);
  };

  const onSubmit = async (event: { preventDefault: () => void }): Promise<void> => {
    event.preventDefault();

    setIsLoading(true);

    const response = await makeApiRequest(RequestMethods.PUT, 'roles/preferences', {
      user_id: user?.id,
      primary_role: primaryRole.toUpperCase(),
      secondary_role: secondaryRole.toUpperCase(),
      off_role: offRole.toUpperCase(),
    });

    if (response instanceof Left) {
      const error = response.unsafeUnwrap();

      if ((error as AxiosError).isAxiosError) {
        setFormError('Failed to update preferences.');
      } else {
        // Something else, job for the ErrorBoundary.
        setUnhandledError(error);
      }
    } else {
      enqueueSnackbar('Preferences successfully changed.', {
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

    const isDisabled = !hasMadeChange || !(primaryRole && secondaryRole && offRole);

    if (isDisabled) {
      const tooltipTitle = 'Must select all 3 preferences or have made a change to any of them.';

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
              Submit
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

  const renderMenuItems = () =>
    allAvailableRoles.map((role) => {
      const hasAlreadySelectedRole = [primaryRole, secondaryRole, offRole].includes(role);

      return (
        <MenuItem
          key={`primary-role-${role}`}
          className={hasAlreadySelectedRole ? classes.hidden : undefined}
          value={role}
        >
          {role}
        </MenuItem>
      );
    });

  if (unhandledError !== null) throw unhandledError;

  return (
    <Container className={classes.contentWrapper} maxWidth="xs">
      <form noValidate className={classes.form}>
        <Grid container alignItems="center" direction="column">
          <Grid item className={classes.formItem} xs={12}>
            <FormControl className={classes.formControl}>
              <InputLabel id="primary-role-selector">Primary Role</InputLabel>
              <Select
                id="primary-role-selector-helper"
                labelId="primary-role-selector-helper-label"
                value={primaryRole}
                onChange={onPrimaryRoleChange}
              >
                {renderMenuItems()}
              </Select>
              <FormHelperText>Your preferred primary role.</FormHelperText>
            </FormControl>
          </Grid>
          <Grid item className={classes.formItem} xs={12}>
            <FormControl className={classes.formControl}>
              <InputLabel id="secondary-role-selector">Secondary Role</InputLabel>
              <Select
                id="secondary-role-selector-helper"
                labelId="secondary-role-selector-helper-label"
                value={secondaryRole}
                onChange={onSecondaryRoleChange}
              >
                {renderMenuItems()}
              </Select>
              <FormHelperText>Your preferred secondary role.</FormHelperText>
            </FormControl>
          </Grid>
          <Grid item className={classes.formItem} xs={12}>
            <FormControl className={classes.formControl}>
              <InputLabel id="off-role-selector">Off Role</InputLabel>
              <Select
                id="off-role-selector-helper"
                labelId="off-role-selector-helper-label"
                value={offRole}
                onChange={onOffRoleChange}
              >
                {renderMenuItems()}
              </Select>
              <FormHelperText>Your off role if you really had to stretch.</FormHelperText>
            </FormControl>
          </Grid>
        </Grid>
        {!!formError && <FormHelperText className={classes.formErrorText}>{formError}</FormHelperText>}
        {renderSubmitButton()}
      </form>
    </Container>
  );
}
