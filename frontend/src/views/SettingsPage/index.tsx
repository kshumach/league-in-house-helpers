import React, { ReactElement, useState } from 'react';
import { Container, makeStyles, Paper, Tab, Tabs } from '@material-ui/core';
import { InspectableObject } from '../../utils/types';

const useStyles = makeStyles({

});

export default function SettingsPage(): ReactElement {
  const [selectedTab, setSelectedTab] = useState(0);
  const classes = useStyles();

  const onTabSelect = (_: React.ChangeEvent<NonNullable<InspectableObject>>, newTab: number) => setSelectedTab(newTab);

  return (
    <Container maxWidth="md">
      <Paper>
        <Tabs
          centered
          textColor="primary"
          value={selectedTab}
          onChange={onTabSelect}
        >
          <Tab label="Change Password" />
        </Tabs>
      </Paper>
    </Container>
  )
}