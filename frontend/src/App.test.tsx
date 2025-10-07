import {render, screen} from './utils/test_utils';
import {describe, it, expect} from 'vitest';
import App from './App';

describe('App Component', () => {
  it('renders learn react link', () => {
    render(<App />);

    const OAuthLink = screen.getByText('Connect to Notion');
    expect(OAuthLink).toBeInTheDocument();

    const signatureElement = screen.getByText('Made by RANDRIANJAFY Joelas');
    expect(signatureElement).toBeInTheDocument();
  });
});