import '../styles/search.css'
import { useNavigate } from 'react-router-dom';
import noPoster from '../assets/No data.svg';
import { addToWishList } from '../api/wishList';
import { addToWatchList } from '../api/watchList';

export default function MovieResult({ movie }) {
    const navigate = useNavigate();

    const handleMovieClick = () => {
        navigate(`/movie/${movie.imdbID}`);
    };

    const handleAddWishlist = () => {
        addToWishList(movie.imdbID);
        };

    const handleAddWatchlist = () => {
        addToWatchList(movie.imdbID);
    };
    
    return (
        <div
            className="movie-result"
            onClick={handleMovieClick}
        >
            <img
                src={movie.Poster !== 'N/A' ? movie.Poster : noPoster}
                alt={movie.Title}
            />
            <div className="movie-info">
                <h3>{movie.Title}</h3>
                <p>{movie.Year}</p>
                <p>{movie.Type}</p>
                <div className="genre" >
                    <p>{movie.Genre}</p>
                </div>
            </div>
            <div className='movie-options'>
                <button className='movie-options-button'
                    onClick={(e) => {
                        e.stopPropagation();
                        handleAddWishlist();
                    }}>Add to favorites/wishlist</button>
                <button className='movie-options-button'
                    onClick={(e) => {
                        e.stopPropagation();
                        handleAddWatchlist()
                    }}>Add to watchlist</button>
            </div>
        </div>
    )

}