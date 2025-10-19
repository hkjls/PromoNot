import type { ReactNode } from "react";
import { notionKeyContext as NotionKeyContext} from "./notionKeyContext";

export const NotionKeyProvider = ({children}: {children: ReactNode}) => {
  const clientId = import.meta.env.VITE_CLIENT_ID;
  const clientSecret = import.meta.env.VITE_CLIENT_SECRET;
  const authUrl = import.meta.env.VITE_AUTH_URL;

  if (!clientId || !clientSecret || !authUrl) {
    throw new Error("Veuillez définir toutes les variables d'environnement Notion dans le fichier .env");
  }

  return (
    <NotionKeyContext.Provider value={{clientId, clientSecret, authUrl}}>
      {children}
    </NotionKeyContext.Provider>
  );
};
