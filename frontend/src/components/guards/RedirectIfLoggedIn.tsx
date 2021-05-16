import React, { ReactElement } from 'react';
import { Redirect } from 'react-router-dom';
import { hasStoredTokenPair } from '../../utils/general';

interface RedirectIfLoggedInProps {
  to?: string;
  children: ReactElement;
}

export default function RedirectIfLoggedIn({ children, to = '/' }: RedirectIfLoggedInProps): ReactElement {
  if (hasStoredTokenPair()) {
    return <Redirect to={to} />;
  }

  return children;
}
