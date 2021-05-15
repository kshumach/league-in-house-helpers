import React, { ReactElement, useState } from 'react';
import { Container, Paper, Tab, Tabs } from '@material-ui/core';
import { InspectableObject } from '../../utils/types';
import PasswordChangeForm from '../../components/PasswordChangeForm';

enum TabOrdering {
  SETTINGS = 0,
}

interface TabPanelProps {
  children: ReactElement;
  currentValue: number;
  index: number;
}

function TabPanel({ children, currentValue, index }: TabPanelProps): ReactElement {
  return (
    <div aria-labelledby={`nav-tabpanel-${index}`} hidden={currentValue !== index} role="tabpanel">
      {children}
    </div>
  );
}

export default function SettingsPage(): ReactElement {
  const [selectedTab, setSelectedTab] = useState(0);

  const onTabSelect = (_: React.ChangeEvent<NonNullable<InspectableObject>>, newTab: number) => setSelectedTab(newTab);

  return (
    <Container maxWidth="md">
      <Paper>
        <Tabs
          centered
          aria-label="settings"
          role="tablist"
          value={selectedTab}
          onChange={onTabSelect}
        >
          <Tab
            aria-controls={`nav-tabpanel-${TabOrdering.SETTINGS}`}
            href="#change-password"
            id={`nav-tabpanel-${TabOrdering.SETTINGS}`}
            label="Change Password"
            role="tab"
          />
        </Tabs>
        <TabPanel currentValue={selectedTab} index={TabOrdering.SETTINGS}>
          <PasswordChangeForm />
        </TabPanel>
      </Paper>
    </Container>
  );
}
