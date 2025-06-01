import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import MovieResult from '../components/MovieResult';
import * as ReactRouterDom from 'react-router';
import * as wishListAPI from '../api/wishList';
import * as watchListAPI from '../api/watchList';
import * as fetchListsAPI from '../api/fetchLists';
import React from 'react';

const mockNavigate = jest.fn();
jest.mock('react-router', () => ({
    ...jest.requireActual('react-router'),
    useNavigate: () => mockNavigate, // Directly return the mock function
}));

jest.mock('../api/fetchLists');
jest.mock('../api/wishList');
jest.mock('../api/watchList');

const mockMovie = {
    imdbID: 'tt1234567',
    Title: 'Test Movie',
    Year: '2020',
    Type: 'movie',
    Poster: 'https://example.com/poster.jpg'
};

describe('MovieResult', () => {
    beforeEach(() => {
        // Reset the mock before each test
        mockNavigate.mockClear();
    });


    test('renders movie basic info', async () => {
        fetchListsAPI.fetchMoviesFromLists.mockResolvedValue({ wishlistMovies: [], watchlistMovies: [] });

        render(<MovieResult movie={mockMovie} showLimit={false} />);

        await waitFor(() => expect(fetchListsAPI.fetchMoviesFromLists).toHaveBeenCalled());

        expect(screen.getByText('Test Movie')).toBeInTheDocument();
        expect(screen.getByText('2020')).toBeInTheDocument();
        expect(screen.getByText('movie')).toBeInTheDocument();
    });

    test('navigates to movie details on click', async () => {
        fetchListsAPI.fetchMoviesFromLists.mockResolvedValue({ wishlistMovies: [], watchlistMovies: [] });

        render(<MovieResult movie={mockMovie} showLimit={false} />);

        await waitFor(() => expect(fetchListsAPI.fetchMoviesFromLists).toHaveBeenCalled());

        fireEvent.click(screen.getByText('Test Movie'));
        expect(mockNavigate).toHaveBeenCalledWith('/movie/tt1234567');
    });

    test('renders add buttons when not in any list', async () => {
        fetchListsAPI.fetchMoviesFromLists.mockResolvedValue({ wishlistMovies: [], watchlistMovies: [] });

        render(<MovieResult movie={mockMovie} showLimit={false} />);

        await waitFor(() => {
            expect(screen.getByText('Add to wishlist')).toBeInTheDocument();
            expect(screen.getByText('Add to watchlist')).toBeInTheDocument();
        });
    });

    test('clicking "Add to wishlist" calls API and updates local state', async () => {
        fetchListsAPI.fetchMoviesFromLists.mockResolvedValue({ wishlistMovies: [], watchlistMovies: [] });
        wishListAPI.addToWishList.mockImplementation(() => { });

        render(<MovieResult movie={mockMovie} showLimit={false} />);

        await waitFor(() => screen.getByText('Add to wishlist'));

        fireEvent.click(screen.getByText('Add to wishlist'));

        expect(wishListAPI.addToWishList).toHaveBeenCalledWith('tt1234567');
    });

    test('renders only "Add to watchlist" when movie is in wishlist', async () => {
        fetchListsAPI.fetchMoviesFromLists.mockResolvedValue({ wishlistMovies: [mockMovie], watchlistMovies: [] });

        render(<MovieResult movie={mockMovie} showLimit={false} />);

        await waitFor(() => screen.getByText('Add to watchlist'));

        expect(screen.getByText('Add to watchlist')).toBeInTheDocument();
        expect(screen.queryByText('Add to wishlist')).not.toBeInTheDocument();
    });

    test('renders info when movie is in watchlist', async () => {
        fetchListsAPI.fetchMoviesFromLists.mockResolvedValue({ wishlistMovies: [], watchlistMovies: [mockMovie] });

        render(<MovieResult movie={mockMovie} showLimit={false} />);

        await waitFor(() => screen.getByText('Already in watchlist'));

        expect(screen.getByText('Already in watchlist')).toBeInTheDocument();
        expect(screen.queryByText('Add to wishlist')).not.toBeInTheDocument();
    });

    test('does not show buttons if showLimit is true', async () => {
        fetchListsAPI.fetchMoviesFromLists.mockResolvedValue({ wishlistMovies: [], watchlistMovies: [] });

        render(<MovieResult movie={mockMovie} showLimit={true} />);

        await waitFor(() => expect(fetchListsAPI.fetchMoviesFromLists).toHaveBeenCalled());

        expect(screen.queryByText('Add to wishlist')).not.toBeInTheDocument();
        expect(screen.queryByText('Add to watchlist')).not.toBeInTheDocument();
    });
});
