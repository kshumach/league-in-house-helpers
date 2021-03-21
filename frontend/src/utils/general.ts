import _camelCase from 'lodash/camelCase';
import isPlainObject from 'lodash/isPlainObject';
import { Either, InspectableObject, Left, Right } from './types';

export function camelizeKeys(object: InspectableObject, keysToSkip: Array<string> = []): InspectableObject {
  return Object.entries(object).reduce(
    (acc: InspectableObject, [key, value]: [string, InspectableObject]): InspectableObject => {
      if (keysToSkip.includes(key)) {
        return acc;
      }

      if (isPlainObject(value)) {
        return {
          ...acc,
          [_camelCase(key)]: camelizeKeys(value),
        };
      }

      return {
        ...acc,
        [_camelCase(key)]: value,
      };
    },
    {}
  );
}

export function reduceErrors(errors: Array<string>): string {
  if (errors.length === 0) return '';

  return errors.join(' ')
}

export function storeTokenPair({ access, refresh }: { access: string, refresh: string }): void {
  localStorage.setItem('access_token', access);
  localStorage.setItem('refresh_token', refresh);
}

export function deleteStoredTokenPair(): void {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
}

export function hasStoredTokenPair(): boolean {
  return !!localStorage.getItem('access_token') && !!localStorage.getItem('refresh_token');
}

export const right = <T, E extends Error>(value: T): Either<T, E> => new Right<T, E>(value);
export const left = <T, E extends Error>(value: E): Either<T, E> => new Left<T, E>(value);