import MovieSearch from '../components/MovieSearch';
import MovieListSection from '../components/MovieListSection';
import '../styles/dashboard.css'
import { getWatchList } from '../api/watchList';
import { getWishList } from '../api/wishList';
import { getMovie } from '../api/movies';
import React, { useEffect, useState } from 'react';

export default function DashboardPage() {
  const [watchList, setWatchList] = useState([]);
  const [wishList, setWishList] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);


   useEffect(() => {
      const fetchWatchedMovies = async () => {
        try {
          setLoading(true);
          const response = await getWatchList();
          const data = await response.json();

          if (!Array.isArray(data)) {
            throw new Error("Nieprawidłowy format danych z listy obejrzanych.");
          }
  
          const moviePromises = data.map((id) => getMovie(id));
          const moviesData = await Promise.all(moviePromises);
          setWatchList(moviesData);
        } catch (err) {
          setError(err.message || "Błąd podczas ładowania obejrzanych filmów.");
        } finally {
          setLoading(false);
        }
      };

      const fetchWishListMovies = async () => {
        try {
          setLoading(true);
          const response = await getWishList();
          const data = await response.json();
          if (!Array.isArray(data)) {
            throw new Error("Nieprawidłowy format danych z listy obejrzanych.");
          }

          const moviePromises = data.map((id) => getMovie(id));
          const moviesData = await Promise.all(moviePromises);
          setWishList(moviesData);
        } catch (err) {
          setError(err.message || "Błąd podczas ładowania obejrzanych filmów.");
        } finally {
          setLoading(false);
        }
      };
  
      fetchWatchedMovies();
      fetchWishListMovies();
    }, []);

  return (
    <>
      {loading && <p>Loading...</p>}
      {error && <p className="error">{error}</p>}
        <title>Dashboard</title>
        <MovieSearch showLimit={true} maxResults={3} withPagination={false}></MovieSearch>
        <MovieListSection
              title="Watched movies"
              movies={watchList}
              maxItems={3}
              seeMoreLink="/watched"
        />
        <MovieListSection
              title="To watch movies"
              movies={wishList}
              maxItems={3}
              seeMoreLink="/to_watch"
        />
        dashboard z podsumowaniem, statystykami, linkami do list, itp.
    </>
  );
}
