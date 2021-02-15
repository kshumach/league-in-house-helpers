import React, { ReactElement } from 'react';
import { useUserContext } from "../../context/user";

export default function HomePage(): ReactElement {
  const user = useUserContext();

  return <div>Welcome {user.username}</div>
}