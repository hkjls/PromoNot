import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';

import { NotionKeyProvider } from './notionKeyProvider';
import { useNotionKey } from './useNotionKey';

vi.stubGlobal('import', {
    meta:{
        env:{
            VITE_CLIENT_ID: "my_client_id_secret",
            VITE_CLIENT_SECRET: "my_client_secret_value",
            VITE_AUTH_URL: "https://example.com/auth"
        }
    }
});

describe('useKeys hook', ()=>{
    it('should create an error when it is used outside of a NotionKeyProvider', ()=>{
        const errorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
        const TestComponent = () => {
            useNotionKey();
            return <div>Test</div>;
        };

        expect(() => render(<TestComponent />)).toThrow('useNotionKey must be used within a NotionKeyProvider');
        errorSpy.mockRestore();
    });
})

describe('NotionKeyProvider', ()=>{
    it('should provide the keys to its children', ()=>{
        const TestComponent = () => {
            const { clientId, clientSecret, authUrl } = useNotionKey();
            return (
                <div>
                    <span>Client ID: {clientId}</span>
                    <span>Client Secret: {clientSecret}</span>
                    <span>Auth URL: {authUrl}</span>
                </div>
            );
        };

        render(
            <NotionKeyProvider>
                <TestComponent />
            </NotionKeyProvider>
        );

    screen.debug();

    expect(screen.getByText(`Client ID: ${import.meta.env.VITE_CLIENT_ID}`)).toBeInTheDocument();
    expect(screen.getByText(`Client Secret: ${import.meta.env.VITE_CLIENT_SECRET}`)).toBeInTheDocument();
    expect(screen.getByText(`Auth URL: ${import.meta.env.VITE_AUTH_URL}`)).toBeInTheDocument();
    });
})
