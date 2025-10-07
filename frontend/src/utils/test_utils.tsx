import React from 'react';
import type { ReactElement} from 'react';
import { render} from '@testing-library/react';
import type { RenderOptions } from '@testing-library/react';
import { NotionKeyProvider } from '../context/notionKeyContext';

// eslint-disable-next-line react-refresh/only-export-components
const AllTheProviders = ({ children }: { children: React.ReactNode }):ReactElement => {
    return (
        <NotionKeyProvider>
            {children}
        </NotionKeyProvider>
    );
};

const customRender = (
    ui: ReactElement, 
    options?: Omit<RenderOptions, 'wrapper'>) =>
    render(ui, { wrapper: AllTheProviders, ...options });


// eslint-disable-next-line react-refresh/only-export-components
export * from '@testing-library/react';
export { customRender as render };