import { render, screen } from '@testing-library/react';
import App from './App';

test('renders learn react link', () => {
  render(<App />);
  const linkElement = screen.getByText(/learn react/i);
  expect(linkElement).toBeInTheDocument();
});

it('should render menu within Layout without crashing', () => {
  render(
    <App />
  );
  
  // Możesz też sprawdzić czy niektóre linki są obecne
  expect(screen.getByText('Dashboard')).toBeInTheDocument();
  expect(screen.getByText('Browse')).toBeInTheDocument();
});