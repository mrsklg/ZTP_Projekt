import { render, screen, fireEvent } from '@testing-library/react';
import MovieListSection from '../components/MovieListSection';
import { MemoryRouter } from 'react-router';
import * as ReactRouter from 'react-router';

// Mock MovieTile to isolate tests
jest.mock('../components/MovieTile', () => (props) => (
    <div data-testid="movie-tile">{props.movie.Title}</div>
));

const mockNavigate = jest.fn();
jest.mock('react-router', () => ({
    ...jest.requireActual('react-router'),
    useNavigate: () => mockNavigate, // Directly return the mock function
}));

describe('MovieListSection', () => {
    beforeEach(() => {
        // Reset the mock before each test
        mockNavigate.mockClear();
    });


    const sampleMovies = [
        { id: '1', imdbID: 'tt1', Title: 'Movie One' },
        { id: '2', imdbID: 'tt2', Title: 'Movie Two' },
    ];

    test('renders section title', () => {
        render(
            <MemoryRouter>
                <MovieListSection title="Watchlist" movies={sampleMovies} />
            </MemoryRouter>
        );
        expect(screen.getByText('Watchlist')).toBeInTheDocument();
    });

    test('shows loading spinner when isLoading is true', () => {
        render(
            <MemoryRouter>
                <MovieListSection title="Watchlist" movies={sampleMovies} isLoading={true} />
            </MemoryRouter>
        );
        expect(screen.getByText((_, el) => el?.className.includes('spinner-wrapper'))).toBeInTheDocument();
    });

    test('shows empty message and browse button when no movies', () => {
        render(
            <MemoryRouter>
                <MovieListSection title="Watchlist" movies={[]} isLoading={false} />
            </MemoryRouter>
        );
        expect(screen.getByText('No movies on this list.')).toBeInTheDocument();
        expect(screen.getByText(/browse movies/i)).toBeInTheDocument();
    });

    test('navigates to /browse on browse click', () => {
        render(
            <MemoryRouter>
                <MovieListSection title="Watchlist" movies={[]} isLoading={false} />
            </MemoryRouter>
        );
        fireEvent.click(screen.getByText(/browse movies/i));
        expect(mockNavigate).toHaveBeenCalledWith('/browse');
    });

    test('renders movie tiles when movies are present', () => {
        render(
            <MemoryRouter>
                <MovieListSection title="Watchlist" movies={sampleMovies} />
            </MemoryRouter>
        );
        expect(screen.getAllByTestId('movie-tile')).toHaveLength(2);
        expect(screen.getByText('Movie One')).toBeInTheDocument();
    });

    test('limits displayed movies if maxItems is set', () => {
        render(
            <MemoryRouter>
                <MovieListSection title="Watchlist" movies={sampleMovies} maxItems={1} />
            </MemoryRouter>
        );
        expect(screen.getAllByTestId('movie-tile')).toHaveLength(1);
    });

    test('navigates on "See more" button click', () => {
        render(
            <MemoryRouter>
                <MovieListSection
                    title="Watchlist"
                    movies={sampleMovies}
                    seeMoreLink="/more"
                />
            </MemoryRouter>
        );
        fireEvent.click(screen.getByText('See more'));
        expect(mockNavigate).toHaveBeenCalledWith('/more');
    });
});
