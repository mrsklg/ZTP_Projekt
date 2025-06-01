import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import SearchBar from '../components/SearchBar';
import { Icon } from 'react-icons-kit';

// Mockujemy ikony, ponieważ mogą powodować problemy w testach
jest.mock('react-icons-kit', () => ({
  Icon: ({ icon, className, onClick }) => (
    <div 
      className={className} 
      onClick={onClick}
      data-testid={className.includes('close') ? 'close-icon' : 'search-icon'}
    />
  )
}));

describe('SearchBar Component', () => {
  const mockProps = {
    query: '',
    onChange: jest.fn(),
    onSearch: jest.fn(),
    onClear: jest.fn()
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders basic search bar with input and search button', () => {
    render(<SearchBar {...mockProps} />);
    
    expect(screen.getByPlaceholderText('Search for title')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /search/i })).toBeInTheDocument();
    expect(screen.getByTestId('search-icon')).toBeInTheDocument();
    expect(screen.queryByTestId('close-icon')).not.toBeInTheDocument();
  });

  test('shows close icon when query is not empty', () => {
    render(<SearchBar {...mockProps} query="test" />);
    
    expect(screen.getByTestId('close-icon')).toBeInTheDocument();
  });

  test('calls onChange when typing in input', async () => {
    render(<SearchBar {...mockProps} />);
    
    const input = screen.getByPlaceholderText('Search for title');
    await userEvent.type(input, 'movie');
    
    expect(mockProps.onChange).toHaveBeenCalledTimes(5); // Dla każdej litery
  });

  test('calls onSearch when search button is clicked', async () => {
    render(<SearchBar {...mockProps} query="test" />);
    
    const searchButton = screen.getByRole('button', { name: /search/i });
    await userEvent.click(searchButton);
    
    expect(mockProps.onSearch).toHaveBeenCalledTimes(1);
  });

  test('calls onClear when close icon is clicked', async () => {
    render(<SearchBar {...mockProps} query="test" />);
    
    const closeIcon = screen.getByTestId('close-icon');
    await userEvent.click(closeIcon);
    
    expect(mockProps.onClear).toHaveBeenCalledTimes(1);
  });

  test('calls onSearch when Enter key is pressed', async () => {
    render(<SearchBar {...mockProps} query="test" />);
    
    const input = screen.getByPlaceholderText('Search for title');
    await userEvent.type(input, '{enter}');
    
    expect(mockProps.onSearch).toHaveBeenCalledTimes(1);
  });
});