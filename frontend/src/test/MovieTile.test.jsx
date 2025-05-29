import { render, screen, fireEvent } from '@testing-library/react';
import MovieTile from '../components/MovieTile';
import { MemoryRouter } from 'react-router';
import * as watchListAPI from '../api/watchList';
import * as wishListAPI from '../api/wishList';
  
const mockMovie = {
  imdbID: 'tt1234567',
  Title: 'Test Movie',
  Year: '2020',
  Type: 'movie',
  Poster: 'https://example.com/poster.jpg',
  Genre: 'Action',
  Plot: 'Test plot',
  Director: 'Test Director',
  Actors: 'Actor One, Actor Two',
  Language: 'English',
  Country: 'USA',
  BoxOffice: '$100M',
  imdbRating: '8.0',
  Ratings: [{ Source: 'Internet', Value: '8/10' }],
};

describe('MovieTile component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders movie title and info', () => {
    render(
      <MemoryRouter>
        <MovieTile movie={mockMovie} />
      </MemoryRouter>
    );

    expect(screen.getByText('Test Movie')).toBeInTheDocument();
    expect(screen.getByText('2020')).toBeInTheDocument();
    expect(screen.getByText('Action')).toBeInTheDocument();
  });

  test('renders detailed info if isDetailsOpened is true', () => {
    render(
      <MemoryRouter>
        <MovieTile movie={mockMovie} isDetailsOpened={true} />
      </MemoryRouter>
    );

    expect(screen.getByText(/Plot:/)).toBeInTheDocument();
    expect(screen.getByText(/Director:/)).toBeInTheDocument();
    expect(screen.getByText(/IMDb Rating:/)).toBeInTheDocument();
    expect(screen.getByText('Internet: 8/10')).toBeInTheDocument();
  });

  test('calls add/remove handlers when buttons clicked (wishlist)', () => {
    const addToWatchListMock = jest.spyOn(watchListAPI, 'addToWatchList').mockImplementation(() => {});
    const removeFromWishListMock = jest.spyOn(wishListAPI, 'removeFromWishList').mockImplementation(() => {});

    render(
      <MemoryRouter>
        <MovieTile movie={mockMovie} currentList="wishlist" opposingList={[]} />
      </MemoryRouter>
    );

    fireEvent.click(screen.getByText('Add to Watchlist'));
    fireEvent.click(screen.getByText('Remove from Wishlist'));

    expect(addToWatchListMock).toHaveBeenCalledWith('tt1234567');
    expect(removeFromWishListMock).toHaveBeenCalledWith('tt1234567');
  });

  test('calls add/remove handlers when buttons clicked (watchlist)', () => {
    const addToWishListMock = jest.spyOn(wishListAPI, 'addToWishList').mockImplementation(() => {});
    const removeFromWatchListMock = jest.spyOn(watchListAPI, 'removeFromWatchList').mockImplementation(() => {});

    render(
      <MemoryRouter>
        <MovieTile movie={mockMovie} currentList="watchlist" opposingList={[]} />
      </MemoryRouter>
    );

    fireEvent.click(screen.getByText('Add to Wishlist'));
    fireEvent.click(screen.getByText('Remove from Watchlist'));

    expect(addToWishListMock).toHaveBeenCalledWith('tt1234567');
    expect(removeFromWatchListMock).toHaveBeenCalledWith('tt1234567');
  });

  test('does not render "add" buttons if movie is in opposingList', () => {
    render(
      <MemoryRouter>
        <MovieTile movie={mockMovie} currentList="wishlist" opposingList={[mockMovie]} />
      </MemoryRouter>
    );

    expect(screen.queryByText('Add to Watchlist')).not.toBeInTheDocument();
    expect(screen.getByText('Remove from Wishlist')).toBeInTheDocument();
  });
});
