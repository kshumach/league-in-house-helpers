import React, { ReactElement, useState } from 'react';
import {
  Button,
  CircularProgress,
  Container,
  Dialog,
  Grid,
  makeStyles,
  MenuItem,
  Select,
  Theme,
  Typography,
} from '@material-ui/core';
import gfm from 'remark-gfm';
import ReactMarkdown from 'react-markdown';
import { RequestMethods, useApiClient } from '../../utils/apiClient';
import { User, useUserContext } from '../../context/user';
import { coalesce } from '../../utils/general';
import { Ballot, Rankings } from '../../utils/types';

const useStyles = makeStyles(({ spacing }: Theme) => ({
  contentWrapper: {
    marginTop: spacing(4),
  },
  title: {
    marginBottom: spacing(4),
  },
  dialog: {
    paddingLeft: spacing(2),
  },
  summonerRow: {
    marginTop: spacing(2),
    marginBottom: spacing(2),
  },
}));

export default function RankingsPage(): ReactElement {
  const { user: currentUser, updateBallot } = useUserContext();
  const [isFetching, users, usersError] = useApiClient<User[]>(RequestMethods.GET, 'users');
  const [isRankingsHelpOpen, setIsRankingsHelpOpen] = useState(false);
  const classes = useStyles();

  if (isFetching) return <CircularProgress />;

  if (usersError) throw usersError;

  const onRankingsHelpClick = () => setIsRankingsHelpOpen(true);

  const onDialogClose = () => setIsRankingsHelpOpen(false);

  const renderRankingOptions = () =>
    [Rankings.S, Rankings.A, Rankings.B, Rankings.C, Rankings.D].map((ranking) => (
      <MenuItem key={`${ranking}-${Rankings[ranking]}`} value={ranking}>
        {Rankings[ranking]}
      </MenuItem>
    ));

  const renderUserRow = ({ id, summoners }: User) => {
    const primarySummoner = summoners[0];
    const currentUserRankingBallots = coalesce(currentUser?.rankingBallots, []);
    const currentUserRankingOfThisUser = currentUserRankingBallots.find((ballot: Ballot) => ballot.user_id === id);

    const rankingValue = currentUserRankingOfThisUser ? Rankings[currentUserRankingOfThisUser.ranking] : '';

    const boundOnChange = (event: React.ChangeEvent<{ value: unknown }>) =>
      updateBallot(id as number, event.target.value as number, primarySummoner);

    return (
      <Grid
        key={primarySummoner}
        container
        alignItems="flex-end"
        className={classes.summonerRow}
        direction="row"
        justify="space-between"
      >
        {primarySummoner}
        <Select id={`${primarySummoner}-ranking-selector`} value={rankingValue} onChange={boundOnChange}>
          {renderRankingOptions()}
        </Select>
      </Grid>
    );
  };

  const usersWithLinkedSummoners = coalesce(users, []).filter((user) => user.summoners && user.summoners.length > 0);

  const rankingsHelpMarkdown = `
### S Tier
* excellent communication
* excellent map play
* excellent level of play
* excellent team effort
### A Tier
* great communication
* great map play
* great level of play
* great team effort
### B Tier
* good communication
* good map play
* good level of play
* good team effort
### C Tier
* average communication
* average map play
* average level of play
* average team effort
### D Tier
* basic communication
* basic map play
* basic level of play
* basic team effort
  `;

  return (
    <React.Fragment>
      <Container className={classes.contentWrapper} maxWidth="md">
        <Grid container direction="row">
          <Grid item>
            <Typography className={classes.title} component="h3" variant="h5">
              Rank Other Players
            </Typography>
          </Grid>
          <Grid item>
            <span>
              <Typography component="p">
                Rank other players on a scale of S-D (S being the best) on how well you think they place among everyone
                else.
              </Typography>
              <Typography component="p">
                Click{' '}
                <Button color="primary" onClick={onRankingsHelpClick}>
                  here
                </Button>{' '}
                for more information about what the rankings mean.
              </Typography>
            </span>
          </Grid>
        </Grid>
      </Container>
      <Container maxWidth="sm">{usersWithLinkedSummoners.map((user: User) => renderUserRow(user))}</Container>
      <Dialog
        fullWidth
        maxWidth="xs"
        open={isRankingsHelpOpen}
        PaperProps={{ className: classes.dialog }}
        onClose={onDialogClose}
      >
        <ReactMarkdown remarkPlugins={[gfm]}>{rankingsHelpMarkdown}</ReactMarkdown>
      </Dialog>
    </React.Fragment>
  );
}
