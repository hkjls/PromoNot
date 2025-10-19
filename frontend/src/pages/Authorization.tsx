import type { ReactElement } from "react";
import { useNotionKey } from "../context/useNotionKey";

const Authorization = (): ReactElement => {
    const {authUrl} = useNotionKey();
  return (
    <div>
        <a href={authUrl}>Connect to Notion</a>
    </div>
  )
}

export default Authorization;