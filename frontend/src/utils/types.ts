import { JwtPayload } from 'jwt-decode';

export type Nullable<T> = T | null;
export type Optional<T> = T | undefined;
export type InspectableObject = NonNullable<Record<string, unknown>>;
export interface CustomJwtPayload extends JwtPayload {
  // eslint-disable-next-line camelcase
  user_id?: string;
}
