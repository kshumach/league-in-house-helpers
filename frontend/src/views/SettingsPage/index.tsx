import React, { ReactElement, useState } from 'react';
import { Container, Paper, Tab, Tabs } from '@material-ui/core';
import { useLocation } from 'react-router-dom';
import { InspectableObject } from '../../utils/types';
import PasswordChangeForm from '../../components/PasswordChangeForm';
import RolePreferencesForm from '../../components/RolePreferencesForm';
import LinkAccountForm from '../../components/LinkAccountForm';

enum TabOrdering {
  SETTINGS = 0,
  ROLE_PREFERENCES = 1,
  LINK_ACCOUNT = 2,
}

const hashToSettingMap: { [key: string]: number } = {
  '#change-password': 0,
  '#role-preferences': 1,
  '#link-account': 2,
  '': 0,
};

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
  const location = useLocation();
  const [selectedTab, setSelectedTab] = useState(hashToSettingMap[location.hash]);

  const onTabSelect = (_: React.ChangeEvent<NonNullable<InspectableObject>>, newTab: number) => setSelectedTab(newTab);

  return (
    <Container maxWidth="md">
      <Paper>
        <Tabs centered aria-label="settings" role="tablist" value={selectedTab} onChange={onTabSelect}>
          <Tab
            aria-controls={`nav-tabpanel-${TabOrdering.SETTINGS}`}
            href="#change-password"
            id={`nav-tabpanel-${TabOrdering.SETTINGS}`}
            label="Change Password"
            role="tab"
          />
          <Tab
            aria-controls={`nav-tabpanel-${TabOrdering.ROLE_PREFERENCES}`}
            href="#role-preferences"
            id={`nav-tabpanel-${TabOrdering.ROLE_PREFERENCES}`}
            label="Role Preferences"
            role="tab"
          />
          <Tab
            aria-controls={`nav-tabpanel-${TabOrdering.LINK_ACCOUNT}`}
            href="#link-account"
            id={`nav-tabpanel-${TabOrdering.LINK_ACCOUNT}`}
            label="Link Account"
            role="tab"
          />
        </Tabs>
        <TabPanel currentValue={selectedTab} index={TabOrdering.SETTINGS}>
          <PasswordChangeForm />
        </TabPanel>
        <TabPanel currentValue={selectedTab} index={TabOrdering.ROLE_PREFERENCES}>
          <RolePreferencesForm />
        </TabPanel>
        <TabPanel currentValue={selectedTab} index={TabOrdering.LINK_ACCOUNT}>
          <LinkAccountForm />
        </TabPanel>
      </Paper>
    </Container>
  );
}
