import axios, { AxiosRequestConfig } from 'axios';
import { useEffect, useState } from 'react';
import appConfig from '../config/app';
import { ApiMethodReturnValue, InspectableObject, Left, Nullable } from './types';
import { deleteStoredTokenPair, left, right, storeTokenPair } from './general';
import { LoginRequiredError } from './errors';

export const enum RequestMethods {
  GET = 'GET',
  POST = 'POST',
  PUT = 'PUT',
  PATCH = 'PATCH',
  DELETE = 'DELETE',
}

export interface ApiClientOptions extends AxiosRequestConfig {
  apiUrl?: string;
  headers?: InspectableObject;
}

function applyAuthHeader(requestOptions: AxiosRequestConfig): AxiosRequestConfig {
  if (requestOptions.headers) {
    return {
      ...requestOptions,
      headers: {
        ...requestOptions.headers,
        Authorization: `Bearer ${localStorage.getItem('access_token')}`,
      },
    };
  }

  return {
    ...requestOptions,
    headers: {
      Authorization: `Bearer ${localStorage.getItem('access_token')}`,
    },
  };
}

type RefreshTokenPayload = { access: string; refresh: string };

/**
 * Requests a new access_token with the refresh_token stored in localStorage.
 *
 * If the refresh_token does not exist in localStorage or the request returns a 401, returns a LoginRequiredError
 */
export async function refreshAccessToken(): Promise<ApiMethodReturnValue<NonNullable<RefreshTokenPayload>>> {
  const refreshToken = localStorage.getItem('refresh_token');

  if (!localStorage.getItem('refresh_token')) {
    return left(new LoginRequiredError());
  }

  const url = `${appConfig.API_URL}/api/users/token/refresh`;
  const requestOptions = {
    method: RequestMethods.POST,
    url,
    headers: {
      'Content-Type': 'application/json',
    },
    data: {
      refresh: refreshToken,
    },
  };

  try {
    const { data } = await axios(requestOptions);

    return right(data);
  } catch (error) {
    if (error.response?.status === 401) {
      return left(new LoginRequiredError());
    }

    return left(error);
  }
}

/**
 * Utility to request a new access token and replay the same request with the new access token. Use by `makeApiRequest`
 * if it sees a 401 error.
 */
async function replayRequestWithTokenRefresh<R>(requestOptions: AxiosRequestConfig): Promise<ApiMethodReturnValue<R>> {
  const tokenResult = await refreshAccessToken();

  if (tokenResult instanceof Left) return left<R, Error | LoginRequiredError>(tokenResult.unsafeUnwrap());

  const tokenPair = tokenResult.unwrapOrThrow();

  storeTokenPair(tokenPair);

  try {
    const { data } = await axios(applyAuthHeader(requestOptions));

    return data;
  } catch (error) {
    return left(error);
  }
}

interface MakeApiRequestOptions {
  withAuthHeader?: boolean;
}

/**
 * Helper to make to an API request to the backend.
 *
 * Automatically handles retries on a 401 (token expired/invalid) by requesting a new access_token token via a stored
 * refresh_token.
 *
 * If fetching a new access_token fails, this will return a LoginRequiredError.
 */
export default async function makeApiRequest<R>(
  method: RequestMethods,
  path: string,
  data: InspectableObject | null = null,
  options: ApiClientOptions = {},
  { withAuthHeader = true }: MakeApiRequestOptions = {}
): Promise<ApiMethodReturnValue<R>> {
  const apiUrl = options.apiUrl || appConfig.API_URL;
  const requestOptions = {
    method,
    url: `${apiUrl}/api/${path}`,
    ...options,
  };

  if (data) {
    requestOptions.data = data;
  }

  const updatedRequestOptions = withAuthHeader ? applyAuthHeader(requestOptions) : requestOptions;

  try {
    const { data: res } = await axios(updatedRequestOptions);

    return right(res);
  } catch (error) {
    // Auth header usage mean 401 was likely due to an expired token
    if (error.response?.status === 401 && withAuthHeader) {
      const response = await replayRequestWithTokenRefresh<R>(requestOptions);

      // Token refresh failure likely means the user has either been deleted or something else. Force log in.
      if (response instanceof Left) {
        deleteStoredTokenPair();

        return left(response.unsafeUnwrap());
      }

      return response;
    }

    return left(error);
  }
}

type UseApiClientReturnValue<T> = [isFetching: boolean, data: Nullable<T>, error: Nullable<Error>];

interface UseApiClientOptions<T> {
  setStateCallback?: Nullable<(data: T) => void>;
  deps?: Array<unknown>;
  withAuthHeader?: boolean;
}

export function useApiClient<R>(
  method: RequestMethods,
  path: string,
  data: InspectableObject | null = null,
  options: ApiClientOptions = {},
  { setStateCallback = null, deps = [], withAuthHeader = true }: UseApiClientOptions<R> = {}
): UseApiClientReturnValue<R> {
  const cancelTokenSource = axios.CancelToken.source();

  const [isFetching, setIsFetching] = useState(true);
  const [error, setError] = useState<Nullable<Error>>(null);
  const [responseData, setResponseData] = useState<Nullable<R>>(null);

  useEffect(() => {
    async function makeApiCall() {
      const response = await makeApiRequest<R>(
        method,
        path,
        data,
        {
          ...options,
          cancelToken: cancelTokenSource.token,
        },
        { withAuthHeader }
      );

      const responseCb = setStateCallback !== null ? setStateCallback : setResponseData;

      if (response instanceof Left) {
        const err = response.unsafeUnwrap();

        // We don't want to call any react callbacks since the most likely case of a cancellation is an unmount event
        // ApiError instances wrap other errors
        if (axios.isCancel(err)) return;

        setError(err);
      } else {
        responseCb(response.unwrapOrThrow());
      }

      setIsFetching(false);
    }

    makeApiCall();

    return () => {
      cancelTokenSource.cancel('Aborting due to component unmount');
    };
    // eslint-disable-next-line
  }, deps);

  return [isFetching, responseData, error];
}
