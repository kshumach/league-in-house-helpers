import axios, { AxiosRequestConfig } from 'axios';
import { useEffect, useState } from 'react';
import appConfig from '../config/app';
import { InspectableObject, Nullable} from './types';
import { ApiError } from './errors';
import { Either, Left, left, right, storeTokenPair } from './general';

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

export type SetStateCallback<R> = (response: R) => void;

export class LoginRequiredError extends Error {}

function applyAuthHeader(requestOptions: AxiosRequestConfig): AxiosRequestConfig {
  if (requestOptions.headers) {
    return {
      ...requestOptions,
      headers: {
        ...requestOptions.headers,
        Authorization: `Bearer: ${localStorage.getItem('access_token')}`,
      },
    };
  }

  return {
    ...requestOptions,
    headers: {
      Authorization: `Bearer: ${localStorage.getItem('access_token')}`,
    },
  };
}

type RefreshTokenPayload = { access: string; refresh: string };

export async function refreshAccessToken(): Promise<Either<NonNullable<RefreshTokenPayload>, ApiError>> {
  const refreshToken = localStorage.getItem('refresh_token');

  if (!localStorage.getItem('refresh_token')) {
    return left(new ApiError(new LoginRequiredError()));
  }

  const url = `${appConfig.API_ULR}/api/token/refresh`;
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
    return left(new ApiError(error));
  }
}

async function replayRequestWithTokenRefresh<R>(requestOptions: AxiosRequestConfig): Promise<Either<R, ApiError>> {
  const tokenResult = await refreshAccessToken();

  if (tokenResult instanceof Left) return left<R, ApiError>(tokenResult.unsafeUnwrap());

  const tokenPair = tokenResult.unwrapOrThrow();

  storeTokenPair(tokenPair);

  try {
    const { data } = await axios(applyAuthHeader(requestOptions));

    return data;
  } catch (error) {
    return left(new ApiError(error));
  }
}

export async function makeApiRequest<R>(
  method: RequestMethods,
  path: string,
  data: InspectableObject | null = null,
  options: ApiClientOptions = {},
  withAuth = false
): Promise<Either<R, ApiError>> {
  const apiUrl = options.apiUrl || appConfig.API_ULR;
  const requestOptions = {
    method,
    url: `${apiUrl}/api/${path}`,
    ...options,
  };

  if (data) {
    requestOptions.data = data;
  }

  if (withAuth) {
    requestOptions.headers = {
      ...requestOptions.headers,
      Authorization: `Bearer: ${localStorage.getItem('access_token')}`,
    };
  }

  const updatedRequestOptions = withAuth ? applyAuthHeader(requestOptions) : requestOptions;

  try {
    const { data: res } = await axios(updatedRequestOptions);

    return right(res);
  } catch (error) {
    if (error.response.statusCode === 401) {
      const response = await replayRequestWithTokenRefresh<R>(requestOptions);

      return response;
    }

    return left(new ApiError(error));
  }
}

type useApiClientReturnValue<T> = [isFetching: boolean, data: Nullable<T>, error: Nullable<ApiError>];

export function useApiClient<R>(
  method: RequestMethods,
  path: string,
  data: InspectableObject | null = null,
  options: ApiClientOptions = {},
  setStateCallback: Nullable<SetStateCallback<R>> = null,
  deps: Array<unknown> = []
): useApiClientReturnValue<R> {
  const cancelTokenSource = axios.CancelToken.source();

  const [isFetching, setIsFetching] = useState(true);
  const [error, setError] = useState<Nullable<ApiError>>(null);
  const [responseData, setResponseData] = useState<Nullable<R>>(null);

  useEffect(() => {
    async function makeApiCall() {
      const response = await makeApiRequest<R>(method, path, data, {
        ...options,
        cancelToken: cancelTokenSource.token,
      });

      const responseCb = setStateCallback !== null ? setStateCallback : setResponseData;

      if (response instanceof Left) {
        const err: ApiError = response.unsafeUnwrap();

        // We don't want to call any react callbacks since the most likely case of a cancellation is an unmount event
        // ApiError instances wrap other errors
        if (axios.isCancel(err.error)) return;

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

export default makeApiRequest;
