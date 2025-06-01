import { useEffect } from 'react';
import { useState } from 'react';
import { useParams } from 'react-router';
import MovieTile from '../components/MovieTile';
import { getMovie } from '../api/movies';
import { fetchMoviesFromLists } from '../api/fetchLists';
import { addToWatchList, removeFromWatchList } from '../api/watchList';
import { addToWishList, removeFromWishList } from '../api/wishList';
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
          opposingList={
            getCurrentList() === "wishlist" ? watchlistMovies : wishlistMovies
          }
          onAddToWatchlist={handleAddToWatchlist}
          onRemoveFromWatchlist={handleRemoveFromWatchlist}
          onAddToWishlist={handleAddToWishlist}
          onRemoveFromWishlist={handleRemoveFromWishlist}
        />
      )}
    </>
  );
}
