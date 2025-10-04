import {render, screen} from '@testing-library/react';
import {describe, it, expect} from 'vitest';
import App from './App';

describe('App Component', () => {
  it('renders learn react link', () => {
    render(<App />);
    const linkElement = screen.getByText(/Vite \+ React/i);
    expect(linkElement).toBeInTheDocument();
  });
});