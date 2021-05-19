import React, { ReactElement, useState } from 'react';
import {
  Button,
  CircularProgress,
  Container,
  Divider,
  Grid,
  makeStyles,
  TextField,
  Theme,
  Typography,
} from '@material-ui/core';
import DeleteIcon from '@material-ui/icons/Delete';
import { useUserContext } from '../context/user';
import { coalesce } from '../utils/general';

const useStyles = makeStyles(({ spacing }: Theme) => ({
  contentWrapper: {
    marginTop: spacing(2),
  },
  summonerName: {
    width: '100%',
  },
  divider: {
    marginTop: spacing(4),
    marginBottom: spacing(4),
  },
  newSummonerInput: {
    width: '100%',
  },
  label: {
    marginBottom: spacing(2),
  },
  summonerRow: {
    marginBottom: spacing(4),
  },
  submit: {
    margin: spacing(2, 0),
  },
}));

export default function LinkAccountForm(): ReactElement {
  const { user, removeSummoner, addSummoner } = useUserContext();
  const [newSummonerName, setNewSummonerName] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const classes = useStyles();

  const onNewSummonerNameChange = (event: React.ChangeEvent<{ value: unknown }>) => {
    setNewSummonerName(event.target.value as string);
  };

  const onAddNewSummoner = async () => {
    setIsLoading(true);

    await addSummoner(newSummonerName);

    setIsLoading(false);
  };

  const onDeleteSummoner = async (summonerName: string) => {
    setIsLoading(true);

    await removeSummoner(summonerName);

    setIsLoading(false);
  };

  const renderSummonerRow = (ign: string) => (
    <Grid key={ign} container alignItems="center" className={classes.summonerRow} direction="row">
      <Grid item className={classes.summonerName} xs={8}>
        <Typography>{ign}</Typography>
      </Grid>
      <Grid item xs={4}>
        <Button color="secondary" startIcon={<DeleteIcon />} variant="contained" onClick={() => onDeleteSummoner(ign)}>
          Unlink
        </Button>
      </Grid>
    </Grid>
  );

  const renderLinkedSummoners = () => {
    const summoners = coalesce(user?.summoners, []);
    if (summoners.length === 0) {
      return (
        <Typography className={classes.label} color="textSecondary" component="p">
          You do not have any linked summoners. Please use the input below to link one.
        </Typography>
      );
    }

    return summoners.map((ign) => renderSummonerRow(ign));
  };

  const renderSubmitButton = () => {
    if (isLoading) {
      return (
        <Grid container justify="center">
          <CircularProgress className={classes.submit} />
        </Grid>
      );
    }

    return (
      <Button
        fullWidth
        className={classes.submit}
        color="primary"
        disabled={!newSummonerName}
        type="submit"
        variant="contained"
        onClick={onAddNewSummoner}
      >
        Submit
      </Button>
    );
  };

  return (
    <Container className={classes.contentWrapper} maxWidth="xs">
      <Typography className={classes.label} component="h3" variant="h5">
        Linked Summoners
      </Typography>
      {renderLinkedSummoners()}
      <Divider className={classes.divider} />
      <Typography className={classes.label} component="h3" variant="h5">
        Link New Summoner
      </Typography>
      <Grid container alignItems="center" direction="column">
        <Grid item className={classes.summonerName} xs={12}>
          <TextField
            className={classes.newSummonerInput}
            id="new-summoner-input"
            label="Summoner Name"
            value={newSummonerName}
            variant="outlined"
            onChange={onNewSummonerNameChange}
          />
        </Grid>
        <Grid item className={classes.summonerName} xs={12}>
          {renderSubmitButton()}
        </Grid>
      </Grid>
    </Container>
  );
}
