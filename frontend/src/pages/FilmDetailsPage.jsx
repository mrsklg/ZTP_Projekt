import { useEffect } from 'react';
import { useState } from 'react';
import { useParams } from 'react-router-dom';
import MovieTile from '../components/MovieTile';
import { getMovie } from '../api/movies';
import { fetchMoviesFromLists } from '../api/fetchLists';
import "../styles/filmDetails.css"

export default function FilmDetailsPage() {
  const [movie, setMovie] = useState(null);
  const [wishlistMovies, setWishlistMovies] = useState([]);
  const [watchlistMovies, setWatchlistMovies] = useState([]);
  const [loading, setLoading] = useState(true);
  const { id } = useParams();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [movieData, { wishlistMovies, watchlistMovies }] = await Promise.all([
          getMovie(id),
          fetchMoviesFromLists()
        ]);

        setMovie(movieData);
        setWishlistMovies(wishlistMovies);
        setWatchlistMovies(watchlistMovies);
      } catch (err) {
        console.error("Błąd podczas pobierania danych:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [id]);

  const isInList = (list) => list.some((m) => m.imdbID === id);

  const getCurrentList = () => {
    if (isInList(wishlistMovies)) return "wishlist";
    if (isInList(watchlistMovies)) return "watchlist";
    return null;
  };


  return (
    <>
      {loading && <p>Loading...</p>}
      {!loading && movie && (
        <MovieTile
          movie={movie}
          isDetailsOpened={true}
          currentList={getCurrentList()}
          // przekazujemy też drugą listę w razie potrzeby
          opposingList={
            getCurrentList() === "wishlist" ? watchlistMovies : wishlistMovies
          }
        />
      )}
    </>
  );
}
