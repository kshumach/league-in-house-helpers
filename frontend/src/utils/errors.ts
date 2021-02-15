/* eslint-disable max-classes-per-file */
export class EmptyResultError extends Error {}

export class UnsafeResultAccessError extends Error {}

export class UnsafeAccessError extends Error {
  constructor() {
    super('Accessed value of Left instance without performing `isLeft`, `isRight` or `instanceof` check.');
  }
}

export class ApiError extends Error {
  readonly error: Error;

  constructor(error: Error) {
    super();

    this.error = error;
  }
}