import React, { ErrorInfo, ReactElement } from 'react';
import { InspectableObject, Nullable } from '../utils/types';

type ErrorBoundaryState = {
  hasError: boolean;
  error: Nullable<Error>;
};

type ErrorBoundaryProps = {
  children: ReactElement;
};

export default class ErrorBoundary extends React.Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);

    this.state = {
      hasError: false,
      // eslint-disable-next-line react/no-unused-state
      error: null,
    };
  }

  static getDerivedStateFromError(error: Error): InspectableObject {
    return { hasError: true, error };
  }

  componentDidCatch(errorObj: Error, errorInfo: ErrorInfo): void {
    console.error(errorObj, errorInfo);
  }

  render(): ReactElement {
    const { hasError } = this.state;
    const { children } = this.props;

    if (hasError) {
      return <div className="container">An Error Occurred</div>;
    }

    return children;
  }
}
