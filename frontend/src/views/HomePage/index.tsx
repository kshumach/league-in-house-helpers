import React, { ReactElement } from 'react';
import { useUserContext } from '../../context/user';
import { RequestMethods, useApiClient } from '../../utils/apiClient';
import { Nullable } from '../../utils/types';
import ErrorHandler from '../../components/ErrorHandler';

export default function HomePage(): Nullable<ReactElement> {
  const { user } = useUserContext();

  const [loading, data, error] = useApiClient<unknown>(RequestMethods.GET, 'users', null, {});

  if (loading) return null;

  if (error) return <ErrorHandler error={error} />;

  console.log(data);
  return <div>Welcome {user?.inGameName}</div>;
}
