import React, { Context, ReactElement } from 'react';

interface PropsWithCallableChild<T> {
  // eslint-disable-next-line react/no-unused-prop-types
  children: (context: T) => ReactElement;
  ContextObject: Context<T>;
  contextName: string;
}

export function useGenericContextHelper<C>(
  ContextObject: Context<C>,
  hookName: string,
  contextName: string
): NonNullable<C> {
  const context = React.useContext<C>(ContextObject);

  if (context === undefined) {
    throw new Error(`${hookName} must be used within a ${contextName}Provider`);
  }

  return context as NonNullable<C>;
}

export function GenericContextConsumer<C>({
  children,
  ContextObject,
  contextName,
}: PropsWithCallableChild<C>): ReactElement {
  return (
    <ContextObject.Consumer>
      {(context) => {
        if (context === undefined) {
          throw new Error(`${contextName}Consumer must be defined within a ${contextName}Provider`);
        }

        return children(context);
      }}
    </ContextObject.Consumer>
  );
}
