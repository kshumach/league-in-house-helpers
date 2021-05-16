import React, { ReactElement } from 'react';
import { Redirect } from 'react-router-dom';
import { Container } from '@material-ui/core';
import { LoginRequiredError, NoRouteMatchError } from '../utils/errors';
import { deleteStoredTokenPair } from '../utils/general';

export default function ErrorHandler({ error }: { error: Error }): ReactElement {
  if (error instanceof LoginRequiredError) {
    const redirectToAfterLogin = error.message;
    const queryParam = redirectToAfterLogin !== '' ? `?redirect_to=${redirectToAfterLogin}` : redirectToAfterLogin;

    // Remove any left over tokens otherwise login will redirect to home, which will redirect back to login, etc.
    deleteStoredTokenPair();

    return <Redirect to={`/login${queryParam}`} />;
  }

  if (error instanceof NoRouteMatchError) {
    return (
      <Container>
        <p>Page Not Found.</p>
      </Container>
    );
  }

  throw error;
}
