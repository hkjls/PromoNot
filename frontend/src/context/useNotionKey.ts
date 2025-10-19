import { useContext } from "react";
import { notionKeyContext } from './notionKeyContext';
import type { NotionKeyContextProps } from './notionKeyContext';


export const useNotionKey = (): NotionKeyContextProps => {
  const context = useContext(notionKeyContext);
  if (!context) {
    throw new Error('useNotionKey must be used within a NotionKeyProvider');
  }
  return context;
};