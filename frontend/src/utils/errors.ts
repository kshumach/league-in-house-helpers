/* eslint-disable max-classes-per-file */
export class UnsafeAccessError extends Error {
  constructor() {
    super('Accessed value of Left instance without performing `isLeft`, `isRight` or `instanceof` check.');

    this.name = 'UnsafeAccessError';
  }
}

export class LoginRequiredError extends Error {
  constructor(originPath = '') {
    super(originPath);

    this.name = 'LoginRequiredError';
  }
}

export class NoRouteMatchError extends Error {
  constructor() {
    super();

    this.name = 'NoRouteMatchError';
  }
}

[UnsafeAccessError, LoginRequiredError, NoRouteMatchError].forEach((error) => {
  Object.defineProperty(error, Symbol.hasInstance, {
    value: (instance: Error): boolean => instance.name === error.name,
  });
});
