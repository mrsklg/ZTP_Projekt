import '../styles/search.css'
import { useNavigate } from 'react-router-dom';
import noPoster from '../assets/No data.svg';
import { BeatLoader } from "react-spinners";
import { addToWishList } from '../api/wishList';
import { addToWatchList } from '../api/watchList';
import { fetchMoviesFromLists } from '../api/fetchLists';
import { useState, useEffect } from 'react';

export default function MovieResult({ movie, showLimit }) {
    const navigate = useNavigate();
    const [wishlistMovies, setWishlistMovies] = useState([]);
    const [watchlistMovies, setWatchlistMovies] = useState([]);
    const [isLoadingLists, setIsLoadingLists] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const { wishlistMovies, watchlistMovies } = await fetchMoviesFromLists();

                setWishlistMovies(wishlistMovies);
                setWatchlistMovies(watchlistMovies);
            } catch (error) {
                console.error('Error fetching movies:', error);
            } finally {
                setIsLoadingLists(false);
            }
        };
        fetchData();
      }, []);

    const handleMovieClick = () => {
        navigate(`/movie/${movie.imdbID}`);
    };

    const handleAddWishlist = () => {
        console.log(wishlistMovies);
        addToWishList(movie.imdbID);
    };

    const handleAddWatchlist = () => {
        addToWatchList(movie.imdbID);
    };

    const inWishlist = wishlistMovies?.some(m => m.imdbID === movie.imdbID);
    const inWatchlist = watchlistMovies?.some(m => m.imdbID === movie.imdbID);

    return (
        <div
            className="movie-result"
            onClick={handleMovieClick}
        >
            <div className='poster-info'>
                {!showLimit &&
                    <img
                        src={movie.Poster !== 'N/A' ? movie.Poster : noPoster}
                        alt={movie.Title}
                    />}
                <div className={`movie-info ${showLimit ? 'limited-movie-info' : ''}`}>
                    <h3>{movie.Title}</h3>
                    <p>{movie.Year}</p>
                    <p>{movie.Type}</p>
                </div>
            </div>
            {!showLimit && (
                <div className='movie-options'>
                    {isLoadingLists ? (
                        <BeatLoader color="#36d7b7" />
                    ) : (
                        <>
                            {!inWatchlist && !inWishlist && (
                            <>
                                <button className='movie-options-button'
                                onClick={(e) => {
                                    e.stopPropagation();
                                    handleAddWishlist();
                                }}>
                                Add to favorites/wishlist
                                </button>
                                <button className='movie-options-button'
                                onClick={(e) => {
                                    e.stopPropagation();
                                    handleAddWatchlist();
                                }}>
                                Add to watchlist
                                </button>
                            </>
                            )}

                            {!inWatchlist && inWishlist && (
                            <button className='movie-options-button'
                                onClick={(e) => {
                                e.stopPropagation();
                                handleAddWatchlist();
                                }}>
                                Add to watchlist
                            </button>
                            )}

                            {inWatchlist && !inWishlist && (
                            <div className='movie-options-button info'>
                            Already in watchlist
                            </div>
                            )}
                        </>
                    )}
                </div>
            )}
        </div>
    );

}

