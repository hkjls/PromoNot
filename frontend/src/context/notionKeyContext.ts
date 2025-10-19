import { createContext } from "react";

export interface NotionKeyContextProps {
  clientId: string;
  clientSecret: string;
  authUrl: string;
}

export const notionKeyContext = createContext<NotionKeyContextProps | undefined>(undefined);