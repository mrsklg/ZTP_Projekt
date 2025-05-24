import { useEffect, useState } from 'react';
import MovieListSection from "../components/MovieListSection";
import { getWishList } from '../api/wishList';
import { getMovie } from '../api/movies';

export default function ToWatchPage() {
    const [movies, setMovies] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
  
    useEffect(() => {
      const fetchToWatchedMovies = async () => {
        try {
          setLoading(true);
          const response = await getWishList();
          const data = await response.json();
  
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
  
      fetchToWatchedMovies();
    }, []);
  
    return (
      <>  
        {loading && <p>Loading...</p>}
        {error && <p className="error">{error}</p>}
        <MovieListSection
                title="To watch movies"
                movies={movies}>
        </MovieListSection>
      </>
    );
}
