import type { ReactElement } from "react";
// import { useState} from 'react';
import { useNotionKey } from "../context/notionKeyContext";

const Authorization = (): ReactElement => {
    const {authUrl} = useNotionKey();
  return (
    <div>
        <a href={authUrl}>Connect to Notion</a>
    </div>
  )
}

export default Authorization;