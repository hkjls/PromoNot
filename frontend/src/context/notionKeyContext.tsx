import {createContext, useContext} from "react";
import type { ReactNode } from "react";

interface NotionKeyContextProps {
  clientId: string;
  clientSecret: string;
  authUrl: string;
}

const NotionKeyContext = createContext<NotionKeyContextProps | undefined>(undefined);

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

// eslint-disable-next-line react-refresh/only-export-components
export const useNotionKey = ()=> {
  const context = useContext(NotionKeyContext);
  if (!context) {
    throw new Error('useNotionKey must be used within a NotionKeyProvider');
  }
  return context;
};
