import { useEffect, useState } from 'react';
import MovieTile from "../components/MovieTile";
import { getToWatchList } from '../api/watchList';
import { getMovie } from '../api/movies';


export default function WatchedPage() {
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchWatchedMovies = async () => {
      try {
        setLoading(true);
        const response = await getToWatchList();
        const data = await response.json();

        // Zakładamy, że data to tablica ID np. ["tt1234567", "tt9876543"]
        if (!Array.isArray(data)) {
          throw new Error("Nieprawidłowy format danych z listy obejrzanych.");
        }

        const moviePromises = data.map((id) => getMovie(id));
        const moviesData = await Promise.all(moviePromises);
        console.log(moviesData);
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
      <h1>Watched</h1>

      {loading && <p>Loading...</p>}
      {error && <p className="error">{error}</p>}

      <div className="movie-grid">
        {movies && movies.map((movie) => (
          <MovieTile key={movie.imdbID} movie={movie} />
        ))}
      </div>
    </>
  );
}
