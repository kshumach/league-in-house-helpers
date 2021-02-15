/* eslint-disable max-classes-per-file */
import _camelCase from 'lodash/camelCase';
import isPlainObject from 'lodash/isPlainObject';
import { InspectableObject } from './types';
import { UnsafeAccessError } from './errors';

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

interface EitherInterface<T, E extends Error> {
  isLeft: () => boolean;
  isRight: () => boolean;
  unwrapOrThrow: () => T;
  unwrapOrElse: (fallback: T) => T;
  unsafeUnwrap: () => T | E;
}

export class Left<T, E extends Error> implements EitherInterface<T, E> {
  /* eslint-disable no-underscore-dangle, class-methods-use-this */
  private readonly _data: E;

  private hasPerformedSanityCheck: boolean;

  constructor(data: E) {
    this._data = data;

    this.hasPerformedSanityCheck = false;
  }

  isLeft(): boolean {
    this.hasPerformedSanityCheck = true;

    return true;
  }

  isRight(): boolean {
    this.hasPerformedSanityCheck = true;

    return false;
  }

  unwrapOrThrow(): T {
    throw this._data;
  }

  unsafeUnwrap(): E {
    if (!this.hasPerformedSanityCheck) throw new UnsafeAccessError();

    return this._data;
  }

  unwrapOrElse(fallback: T): T {
    return fallback;
  }
}

export class Right<T, E extends Error> implements EitherInterface<T, E> {
  /* eslint-disable no-underscore-dangle, class-methods-use-this */
  private readonly _data: T;

  constructor(data: T) {
    this._data = data;
  }

  isLeft(): boolean {
    return false;
  }

  isRight(): boolean {
    return true;
  }

  unwrapOrThrow(): T {
    return this._data;
  }

  unsafeUnwrap(): T {
    return this.unwrapOrThrow();
  }

  unwrapOrElse(fallback: T): T {
    if (!this._data) return fallback;

    return this._data;
  }
}

Object.defineProperty(Left, Symbol.hasInstance, {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  value: (instance: any): boolean => (instance.isLeft && instance.isLeft())
});

Object.defineProperty(Right, Symbol.hasInstance, {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  value: (instance: any): boolean => (instance.isRight && instance.isRight())
});

export type Either<T, E extends Error> = Left<T, E> | Right<T, E>;
export const right = <T, E extends Error>(value: T): Either<T, E> => new Right<T, E>(value);
export const left = <T, E extends Error>(value: E): Either<T, E> => new Left<T, E>(value);