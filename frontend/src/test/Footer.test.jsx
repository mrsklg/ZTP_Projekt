import { render, screen } from '@testing-library/react';
import Footer from '../components/Footer';

describe('Footer component', () => {
  test('renders logo image with correct alt text', () => {
    render(<Footer />);
    const logo = screen.getByAltText(/watchy logo/i);
    expect(logo).toBeInTheDocument();
    expect(logo.tagName).toBe('IMG');
  });

  test('renders copyright text', () => {
    render(<Footer />);
    const text = screen.getByText(/made with/i);
    expect(text).toBeInTheDocument();
    expect(text).toHaveTextContent('Made with ❤️ by people');
  });

  test('renders link to Storyset with correct href', () => {
    render(<Footer />);
    const link = screen.getByRole('link', { name: /user illustrations by storyset/i });
    expect(link).toBeInTheDocument();
    expect(link).toHaveAttribute('href', 'https://storyset.com/user');
  });
});
