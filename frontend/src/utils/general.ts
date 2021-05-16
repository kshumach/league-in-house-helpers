import _camelCase from 'lodash/camelCase';
import isPlainObject from 'lodash/isPlainObject';
import { Either, InspectableObject, Left, Nullable, Optional, Right } from './types';

export function coalesce<T>(value: Optional<T> | Nullable<T>, fallback: T): T {
  return value ?? fallback;
}

export function camelizeKeys<T extends InspectableObject>(object: T, keysToSkip: Array<string> = []): T {
  return Object.entries(object).reduce((acc, [key, value]): T => {
    if (keysToSkip.includes(key)) {
      return acc;
    }

    if (isPlainObject(value)) {
      return {
        ...acc,
        [_camelCase(key)]: camelizeKeys(value as InspectableObject),
      };
    }

    return {
      ...acc,
      [_camelCase(key)]: value,
    };
  }, {} as T);
}

export function reduceErrors(errors: Array<string>): string {
  if (errors.length === 0) return '';

  return errors.join(' ');
}

export function storeTokenPair({ access, refresh }: { access: string; refresh: string }): void {
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
