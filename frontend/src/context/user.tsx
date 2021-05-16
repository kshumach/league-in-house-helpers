import React, { ReactChild, ReactElement, useEffect, useReducer, useState } from 'react';
import jwtDecode from 'jwt-decode';
import { CircularProgress } from '@material-ui/core';
import { Redirect, useLocation } from 'react-router-dom';
import { useSnackbar } from 'notistack';
import { CustomJwtPayload, InspectableObject, Left, Nullable, Optional, PreferredRoles } from '../utils/types';
import { GenericContextConsumer, useGenericContextHelper } from '../utils/context-helpers';
import makeApiRequest, { refreshAccessToken, RequestMethods } from '../utils/apiClient';
import { camelizeKeys, hasStoredTokenPair } from '../utils/general';

export interface User extends InspectableObject {
  id: Nullable<number>;
  username: Nullable<string>;
  summoners: Array<string>;
  preferredRoles: PreferredRoles;
}

function initializeUser(): User {
  return {
    id: null,
    username: null,
    summoners: [],
    preferredRoles: {
      primaryRole: null,
      secondaryRole: null,
      offRole: null,
    },
  };
}

export interface UserCtx {
  user: Nullable<User>;
  userError: Nullable<Error>;
  isFetchingUser: boolean;
  removeSummoner: (summonerName: string) => Promise<void>;
  addSummoner: (summonerName: string) => Promise<void>;
}

export type UserContextType = Optional<UserCtx>;

type UserContextProps = {
  children: ReactChild;
  handleErrors: boolean;
};

const UserContext = React.createContext<UserContextType>(undefined);

enum UserReducerActions {
  REMOVE_SUMMONER = 'REMOVE_SUMMONER',
  ADD_SUMMONER = 'ADD_SUMMONER',
  INITIALIZE_USER_DATA = 'INITIALIZE_USER_DATA',
}

type UserReducerPayloadTypes = {
  [UserReducerActions.INITIALIZE_USER_DATA]: User;
  [UserReducerActions.REMOVE_SUMMONER]: string;
  [UserReducerActions.ADD_SUMMONER]: string;
};

function reducer(
  user: User,
  action: { type: UserReducerActions; payload: UserReducerPayloadTypes[UserReducerActions] }
): User {
  switch (action.type) {
    case UserReducerActions.INITIALIZE_USER_DATA:
      // First fetch from api so will contain all the data we need.
      return action.payload as User;
    case UserReducerActions.ADD_SUMMONER: {
      const summonerToAdd = action.payload as string;

      return {
        ...user,
        summoners: [...user.summoners, summonerToAdd],
      };
    }
    case UserReducerActions.REMOVE_SUMMONER: {
      const summonerToRemove = action.payload;

      return {
        ...user,
        summoners: user.summoners.filter((summoner) => summoner !== summonerToRemove),
      };
    }
    default:
      return user;
  }
}

function UserContextProvider({ children, handleErrors }: UserContextProps): Nullable<ReactElement> {
  const location = useLocation();
  const [loginRequired, setLoginRequired] = useState(false);
  const [error, setError] = useState<Nullable<Error>>(null);
  const [user, dispatch] = useReducer(reducer, initializeUser());
  const [hasLoaded, setHasLoaded] = useState(false);
  const { enqueueSnackbar } = useSnackbar();

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

      dispatch({ type: UserReducerActions.INITIALIZE_USER_DATA, payload: camelizeKeys<User>(userData) });
      setHasLoaded(true);
    }

    if (!hasStoredTokenPair()) {
      setLoginRequired(true);
    } else {
      onMount();
    }
  }, []);

  async function removeSummoner(summonerName: string): Promise<void> {
    const response = await makeApiRequest(RequestMethods.DELETE, `summoners/${summonerName}`);

    if (response instanceof Left) {
      enqueueSnackbar(`Failed to remove ${summonerName}.`, { variant: 'error' });

      return;
    }

    dispatch({ type: UserReducerActions.REMOVE_SUMMONER, payload: summonerName });
  }

  async function addSummoner(summonerName: string): Promise<void> {
    const response = await makeApiRequest(RequestMethods.POST, 'summoners/register', {
      in_game_name: summonerName,
    });

    if (response instanceof Left) {
      enqueueSnackbar(`Failed to add ${summonerName}.`, { variant: 'error' });

      return;
    }

    dispatch({ type: UserReducerActions.ADD_SUMMONER, payload: summonerName });
  }

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
        removeSummoner,
        addSummoner,
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
