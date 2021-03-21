import React, { ReactChild, ReactElement, useEffect, useState } from 'react';
import jwtDecode from 'jwt-decode';
import { CircularProgress } from '@material-ui/core';
import { Redirect, useLocation } from 'react-router-dom';
import { CustomJwtPayload, Nullable, Optional } from '../utils/types';
import { GenericContextConsumer, useGenericContextHelper } from "../utils/context-helpers";
import { refreshAccessToken } from '../utils/apiClient';
import { hasStoredTokenPair, Left } from '../utils/general';

export interface UserCtx {
  username: Nullable<string>;
  userError: Nullable<Error>;
  isFetchingUser: boolean;
}

export type UserContextType = Optional<UserCtx>;

type UserContextProps = {
  children: ReactChild;
  handleErrors: boolean;
};

const UserContext = React.createContext<UserContextType>(undefined);

function UserContextProvider({ children, handleErrors }: UserContextProps): Nullable<ReactElement> {
  const location = useLocation();
  const [loginRequired, setLoginRequired] = useState(false);
  const [error, setError] = useState<Nullable<Error>>(null);
  const [username, setUsername] = useState<Nullable<string>>(null);
  const [hasLoaded, setHasLoaded] = useState(false);

  useEffect(() => {
    async function parseAccessTokenClaims() {
      const accessToken = localStorage.getItem('access_token');

      if (!accessToken) {
        const response = await refreshAccessToken();

        if (response instanceof Left) {
          setError(response.unsafeUnwrap());
          setLoginRequired(true);
        }
      } else {
        const decoded = jwtDecode<CustomJwtPayload>(accessToken);

        setUsername(decoded.user_id || null);
        setHasLoaded(true);
      }
    }

    if (!hasStoredTokenPair()) {
      setLoginRequired(true);
    } else {
      parseAccessTokenClaims();
    }
  }, []);

  const renderContent = () => {
    if (!hasLoaded) return <CircularProgress />;

    if (hasLoaded && error && handleErrors) {
      throw error;
    }

    return children;
  };

  if (loginRequired) {
    return <Redirect to={`/login?redirect_to=${location.pathname}`} />
  }

  return (
    <UserContext.Provider
      value={{
        username,
        userError: error,
        isFetchingUser: !hasLoaded,
      }}
    >
      {renderContent()}
    </UserContext.Provider>
  );
}

function useUserContext(): NonNullable<UserContextType> {
  return useGenericContextHelper<UserContextType>(UserContext, 'useUserContext', 'UserContext');
}

function UserContextConsumer({ children } : { children: (context: UserContextType) => ReactElement }): ReactElement {
  return (
    <GenericContextConsumer ContextObject={UserContext} contextName="UserContext">
      {children}
    </GenericContextConsumer>
  )
}

export { useUserContext, UserContextConsumer, UserContextProvider };
