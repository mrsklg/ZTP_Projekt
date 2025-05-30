import { getWishList } from './wishList';
import { getWatchList } from './watchList';
import { getMovie } from './movies';

/**
 * Pobiera pełne dane filmów z wishlisty i watchlisty.
 * Zwraca obiekt: { wishlistMovies, watchlistMovies }
 */
export async function fetchMoviesFromLists() {
  const [wishlistRes, watchlistRes] = await Promise.all([
    getWishList(),
    getWatchList()
  ]);

  const wishlistData = await wishlistRes.json();
  const watchlistData = await watchlistRes.json();

  console.log(wishlistData)
  console.log(watchlistData)

  if (!Array.isArray(wishlistData.wishlist) || !Array.isArray(watchlistData.watchlist)) {
    throw new Error("Nieprawidłowy format danych.");
  }

  const wishlistMovies = await Promise.all(wishlistData.wishlist.map((id) => getMovie(id)));
  const watchlistMovies = await Promise.all(watchlistData.watchlist.map((id) => getMovie(id)));

  return { wishlistMovies, watchlistMovies };
}
