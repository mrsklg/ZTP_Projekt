import { useEffect, useState } from 'react';
import MovieListSection from "../components/MovieListSection";
import { fetchMoviesFromLists } from '../api/fetchLists';

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

  return (
    <>
      {loading && <p>Loading...</p>}
      {error && <p className="error">{error}</p>}
      <MovieListSection
              title="Watched movies"
              movies={watchlistMovies}
              opposingList={wishlistMovies}
        >
      </MovieListSection>
    </>
  );
}
