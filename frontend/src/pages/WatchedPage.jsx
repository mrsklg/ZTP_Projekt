import { useEffect, useState } from 'react';
import MovieListSection from "../components/MovieListSection";
import { getWatchList } from '../api/watchList';
import { getMovie } from '../api/movies';


export default function WatchedPage() {
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchWatchedMovies = async () => {
      try {
        setLoading(true);
        const response = await getWatchList();
        const data = await response.json();

        // Zakładamy, że data to tablica ID np. ["tt1234567", "tt9876543"]
        if (!Array.isArray(data)) {
          throw new Error("Nieprawidłowy format danych z listy obejrzanych.");
        }

        const moviePromises = data.map((id) => getMovie(id));
        const moviesData = await Promise.all(moviePromises);
        setMovies(moviesData);
      } catch (err) {
        setError(err.message || "Błąd podczas ładowania obejrzanych filmów.");
      } finally {
        setLoading(false);
      }
    };

    fetchWatchedMovies();
  }, []);

  return (
    <>
      {loading && <p>Loading...</p>}
      {error && <p className="error">{error}</p>}
      <MovieListSection
              title="Watched movies"
              movies={movies}>
      </MovieListSection>
    </>
  );
}
