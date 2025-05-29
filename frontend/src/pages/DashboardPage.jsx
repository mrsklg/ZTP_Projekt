import MovieSearch from '../components/MovieSearch';
import MovieListSection from '../components/MovieListSection';
import '../styles/dashboard.css'
import { fetchMoviesFromLists } from '../api/fetchLists';
import React, { useEffect, useState } from 'react';
import { addToWatchList, removeFromWatchList } from '../api/watchList';
import { addToWishList, removeFromWishList } from '../api/wishList';

export default function DashboardPage() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [wishlistMovies, setWishlistMovies] = useState([]);
  const [watchlistMovies, setWatchlistMovies] = useState([]);


  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      
      const { wishlistMovies, watchlistMovies } = await fetchMoviesFromLists();

      setWishlistMovies(wishlistMovies);
      setWatchlistMovies(watchlistMovies);

      console.log(`wishlist w dashboard: ${wishlistMovies}`)
      console.log(`watchlist w dashboard: ${watchlistMovies}`)
    } catch (err) {
      setError(err.message || "Błąd podczas ładowania danych.");
    } finally {
      setLoading(false);
    }
  };

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
        <title>Dashboard</title>
        <div className='dashboard-summary'>
          <MovieSearch showLimit={true} maxResults={3} withPagination={false}></MovieSearch>
          <div className='dashboard-stats'>
            <div className='dashboard-tile'>
              <h3>Movies watched</h3>
              <p>{watchlistMovies.length}</p>
            </div>
            <div className='dashboard-tile'>
              <h3>Movies to watch</h3>
              <p>{wishlistMovies.length}</p>
            </div>
          </div>
        </div>
        <MovieListSection
              title="Watched movies"
              movies={watchlistMovies}
              maxItems={3}
              seeMoreLink="/watched"
              opposingList={wishlistMovies}
              additionalClass={'movies-section-header-dashboard'}
              onAddToWatchlist={handleAddToWatchlist}
              onRemoveFromWatchlist={handleRemoveFromWatchlist}
              onAddToWishlist={handleAddToWishlist}
              onRemoveFromWishlist={handleRemoveFromWishlist}
              />
        <MovieListSection
              title="To watch list"
              movies={wishlistMovies}
              maxItems={3}
              seeMoreLink="/to_watch"
              opposingList={watchlistMovies}
              additionalClass={'movies-section-header-dashboard'}
              onAddToWatchlist={handleAddToWatchlist}
              onRemoveFromWatchlist={handleRemoveFromWatchlist}
              onAddToWishlist={handleAddToWishlist}
              onRemoveFromWishlist={handleRemoveFromWishlist}
        />
    </>
  );
}
