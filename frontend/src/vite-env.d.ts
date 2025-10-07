/// <reference types="vite/client" />

interface ImportMetaEnv {
    readonly VITE_CLIENT_ID: string;
    readonly VITE_CLIENT_SECRET: string;
    readonly VITE_AUTH_URL: string;
    // more env variables...
  }
  
  interface ImportMeta {
    readonly env: ImportMetaEnv;
  }


  /*
    Ce fichier permet de dire à TypeScript : 
    "Fais confiance aux variables que je vais te déclarer ici, elles existent !".
  */