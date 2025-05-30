import { useNavigate } from 'react-router-dom';
import noPoster from '../assets/No data.svg';
import '../styles/movie.css'
// import { addToWatchList, removeFromWatchList } from '../api/watchList';
// import { addToWishList, removeFromWishList } from '../api/wishList';

export default function MovieTile({ movie, isDetailsOpened = false, currentList, opposingList, 
    onAddToWatchlist,
    onRemoveFromWatchlist,
    onAddToWishlist,
    onRemoveFromWishlist
 }) {
    const navigate = useNavigate();

    const handleMovieClick = () => {
        navigate(`/movie/${movie.imdbID}`);
    };

    const handleAddWishlist = (e) => {
        onAddToWishlist(movie);
    };
    
    const handleAddWatchlist = (e) => {
        onAddToWatchlist(movie);
    };
    
    const handleRemoveWishlist = (e) => {
        onRemoveFromWishlist(movie);
    };
    
    const handleRemoveWatchlist = (e) => {
        onRemoveFromWatchlist(movie);
    };

    const isInOpposingList = opposingList?.some(m => m.imdbID === movie.imdbID);

    const renderActionButtons = () => {
        if (currentList === "wishlist") {
            return (
                <>
                    { !isInOpposingList && (
                        <button className="movie-options-button" onClick={(e) => { e.stopPropagation(); handleAddWatchlist(movie); }}>
                            Add to Watchlist
                        </button>
                    ) }
                    <button className="movie-options-button" onClick={(e) => { e.stopPropagation(); handleRemoveWishlist(movie); }}>
                        Remove from Wishlist
                    </button>
                </>
            );
        }
        if (currentList === "watchlist") {
            return (
                <>
                    <button className="movie-options-button" onClick={(e) => { e.stopPropagation(); handleRemoveWatchlist(movie); }}>
                        Remove from Watchlist
                    </button>
                </>
            );
        }
        if (currentList === null || opposingList === null) {
            return (
                <>
                    <button className="movie-options-button" onClick={(e) => { e.stopPropagation(); handleAddWishlist(movie); }}>
                        Add to Wishlist
                    </button>
                    <button className="movie-options-button" onClick={(e) => { e.stopPropagation(); handleAddWatchlist(movie); }}>
                        Add to watchlist
                    </button>
                </>
            );
        }
        return null;
    };

    return (
        <div className={!isDetailsOpened ? "movie-tile" : "movie-tile movie-tile-details"} onClick={!isDetailsOpened ? handleMovieClick : undefined}>
            <div className='movie-tile-top'>
                <img src={movie.Poster !== 'N/A' ? movie.Poster : noPoster}
                    alt={movie.Title} />
                <div className="movie-info">
                    <h3>{movie.Title}</h3>
                    <p>{movie.Year}</p>
                    <p>{movie.Type}</p>
                    <div className="genre" >
                        <p>{movie.Genre}</p>
                    </div>
                    <div className='movie-actions'>
                        {renderActionButtons()}
                    </div>
                </div>
            </div>
            {isDetailsOpened && (
                <div className="movie-details">
                    <p className='movie-details-part'><strong>Plot:</strong> {movie.Plot}</p>
                    <p className='movie-details-part'><strong>Director:</strong> {movie.Director}</p>
                    <p className='movie-details-part'><strong>Actors:</strong> {movie.Actors}</p>
                    <p className='movie-details-part'><strong>Language:</strong> {movie.Language}</p>
                    <p className='movie-details-part'><strong>Country:</strong> {movie.Country}</p>
                    <p className='movie-details-part'><strong>Box Office:</strong> {movie.BoxOffice}</p>
                    <p className='movie-details-part'><strong>IMDb Rating:</strong> ⭐ {movie.imdbRating}</p>
                    <div className="ratings movie-details-part">
                        <strong>Ratings:</strong>
                        <ul>
                            {movie.Ratings?.map((r, index) => (
                                <li key={index}>{r.Source}: {r.Value}</li>
                            ))}
                        </ul>
                    </div>
                </div>
            )}
        </div>
    )

}