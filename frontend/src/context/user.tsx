import React, { ReactChild, ReactElement, useEffect, useState } from 'react';
import jwtDecode from 'jwt-decode';
import { CircularProgress } from '@material-ui/core';
import { Redirect, useLocation } from 'react-router-dom';
import { CustomJwtPayload, InspectableObject, Left, Nullable, Optional, PreferredRoles } from '../utils/types';
import { GenericContextConsumer, useGenericContextHelper } from '../utils/context-helpers';
import makeApiRequest, { refreshAccessToken, RequestMethods } from '../utils/apiClient';
import { camelizeKeys, hasStoredTokenPair } from '../utils/general';

export interface User extends InspectableObject {
  id: number;
  username: Nullable<string>;
  preferredRoles: PreferredRoles;
}

export interface UserCtx {
  user: Nullable<User>;
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
  const [user, setUser] = useState<Nullable<User>>(null);
  const [hasLoaded, setHasLoaded] = useState(false);

  useEffect(() => {
    async function parseAccessTokenClaimsForUserId(): Promise<Nullable<string>> {
      const accessToken = localStorage.getItem('access_token');

      if (!accessToken) {
        const response = await refreshAccessToken();

        if (response instanceof Left) {
          setError(response.unsafeUnwrap());
          setLoginRequired(true);
        }

        return null;
      }

      const decoded = jwtDecode<CustomJwtPayload>(accessToken);

      return String(decoded.user_id);
    }

    async function fetchUserData(userId: string): Promise<User> {
      const response = await makeApiRequest<User>(RequestMethods.GET, `users/${userId}`);

      return response.isRight && response.unwrapOrThrow();
    }

    async function onMount() {
      const userId = await parseAccessTokenClaimsForUserId();

      if (userId === null) return;

      const userData = await fetchUserData(userId);

      setUser(camelizeKeys<User>(userData));
      setHasLoaded(true);
    }

    if (!hasStoredTokenPair()) {
      setLoginRequired(true);
    } else {
      onMount();
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
    return <Redirect to={`/login?redirect_to=${location.pathname}`} />;
  }

  return (
    <UserContext.Provider
      value={{
        user,
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

function UserContextConsumer({ children }: { children: (context: UserContextType) => ReactElement }): ReactElement {
  return (
    <GenericContextConsumer contextName="UserContext" ContextObject={UserContext}>
      {children}
    </GenericContextConsumer>
  );
}

export { useUserContext, UserContextConsumer, UserContextProvider };
