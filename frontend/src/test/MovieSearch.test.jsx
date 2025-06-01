import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import MovieSearch from '../components/MovieSearch';
import * as moviesAPI from '../api/movies';
import * as ReactRouterDom from 'react-router';

jest.mock('../api/movies');
const mockNavigate = jest.fn();
jest.mock('react-router', () => ({
    ...jest.requireActual('react-router'),
    useNavigate: () => mockNavigate, // Directly return the mock function
}));

describe('MovieSearch', () => {
    beforeEach(() => {
        // Reset the mock before each test
        mockNavigate.mockClear();
    });

  test('renders search bar and handles input change', () => {
    render(<MovieSearch />);
    const input = screen.getByRole('textbox');
    fireEvent.change(input, { target: { value: 'Batman' } });
    expect(input.value).toBe('Batman');
  });

  test('shows error message when searching with empty query', async () => {
    render(<MovieSearch />);
    const button = screen.getByRole('button', { name: /search/i });
    fireEvent.click(button);
    expect(await screen.findByText(/please enter a search term/i)).toBeInTheDocument();
  });

  test('clears search and results when clear button clicked', () => {
    render(<MovieSearch />);
    const input = screen.getByRole('textbox');
    fireEvent.change(input, { target: { value: 'Batman' } });

    const clearButton = document.querySelector('.close-icon');
    fireEvent.click(clearButton);

    expect(input.value).toBe('');
    expect(screen.queryByText('Search Results')).not.toBeInTheDocument();
  });

  test('initialQuery prop triggers search on mount', async () => {
    const mockMovies = [
      { imdbID: 'tt999', Title: 'Init Movie', Year: '2022', Type: 'movie', Poster: 'N/A' }
    ];
    moviesAPI.fetchMovies.mockResolvedValue(mockMovies);

    render(<MovieSearch initialQuery="init" />);

    await waitFor(() => {
      expect(moviesAPI.fetchMovies).toHaveBeenCalledWith('init');
      expect(screen.getByText('Init Movie')).toBeInTheDocument();
    });
  });
});
