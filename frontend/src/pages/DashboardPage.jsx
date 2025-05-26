import MovieSearch from '../components/MovieSearch';
import MovieListSection from '../components/MovieListSection';
import '../styles/dashboard.css'
import { fetchMoviesFromLists } from '../api/fetchLists';
import React, { useEffect, useState } from 'react';

export default function DashboardPage() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [wishlistMovies, setWishlistMovies] = useState([]);
  const [watchlistMovies, setWatchlistMovies] = useState([]);


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
        <title>Dashboard</title>
        <MovieSearch showLimit={true} maxResults={3} withPagination={false}></MovieSearch>
        <MovieListSection
              title="Watched movies"
              movies={watchlistMovies}
              maxItems={3}
              seeMoreLink="/watched"
              opposingList={wishlistMovies}
        />
        <MovieListSection
              title="To watch list"
              movies={wishlistMovies}
              maxItems={3}
              seeMoreLink="/to_watch"
              opposingList={watchlistMovies}
        />
        dashboard z podsumowaniem, statystykami, linkami do list, itp.
    </>
  );
}
