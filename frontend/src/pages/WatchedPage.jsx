import { useEffect, useState } from 'react';
import MovieListSection from "../components/MovieListSection";
import { fetchMoviesFromLists } from '../api/fetchLists';
import { addToWatchList, removeFromWatchList } from '../api/watchList';
import { addToWishList, removeFromWishList } from '../api/wishList';

export default function WatchedPage() {
  const [wishlistMovies, setWishlistMovies] = useState([]);
  const [watchlistMovies, setWatchlistMovies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        
        const { wishlistMovies, watchlistMovies } = await fetchMoviesFromLists();

        setWishlistMovies(wishlistMovies);
        setWatchlistMovies(watchlistMovies);
      } catch (err) {
        setError(err.message || "Błąd podczas ładowania danych.");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleAddToWatchlist = (movie) => {
    setWatchlistMovies(prev => [...prev, movie]);
    setWishlistMovies(prev => prev.filter(m => m.imdbID !== movie.imdbID)); // jeśli przenosisz z wishlist
    addToWatchList(movie.imdbID);
  };
  
  const handleRemoveFromWatchlist = (movie) => {
    setWatchlistMovies(prev => prev.filter(m => m.imdbID !== movie.imdbID));
    removeFromWatchList(movie.imdbID);
  };
  
  const handleAddToWishlist = (movie) => {
    setWishlistMovies(prev => [...prev, movie]);
    setWatchlistMovies(prev => prev.filter(m => m.imdbID !== movie.imdbID));
    addToWishList(movie.imdbID);
  };
  
  const handleRemoveFromWishlist = (movie) => {
    setWishlistMovies(prev => prev.filter(m => m.imdbID !== movie.imdbID));
    removeFromWishList(movie.imdbID);
  };

  return (
    <>
      {loading && <p>Loading...</p>}
      {error && <p className="error">{error}</p>}
      <MovieListSection
              title="Watched movies"
              movies={watchlistMovies}
              opposingList={wishlistMovies}
              onAddToWatchlist={handleAddToWatchlist}
              onRemoveFromWatchlist={handleRemoveFromWatchlist}
              onAddToWishlist={handleAddToWishlist}
              onRemoveFromWishlist={handleRemoveFromWishlist}
        >
      </MovieListSection>
    </>
  );
}
