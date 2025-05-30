import { useNavigate } from 'react-router-dom';
import MovieTile from "./MovieTile";
import "../styles/movie.css"

export default function MovieListSection({ 
    title, 
    movies, 
    maxItems = null, 
    seeMoreLink = null, 
    opposingList, 
    additionalClass, 
    onAddToWatchlist,
    onRemoveFromWatchlist,
    onAddToWishlist,
    onRemoveFromWishlist
    }) {
    const displayedMovies = maxItems ? movies.slice(0, maxItems) : movies;
    const navigate = useNavigate();

    const handleSeeMoreClick = () => {
        navigate(seeMoreLink);
    };

    const currentList = title === "To watch list" ? "wishlist" : "watchlist";

    return (
        <section className="movies-section">
            <div className={`movies-section-header ${additionalClass}`}>
                <h2>{title}</h2>
                {seeMoreLink && <button className="show-more" onClick={handleSeeMoreClick}>
                    See more
                </button>}
            </div>
            <div className="movie-grid">
                {displayedMovies.map((movie) => (
                    <MovieTile 
                        key={movie.id} 
                        movie={movie} 
                        currentList={currentList} 
                        opposingList={opposingList} 
                        onAddToWatchlist={onAddToWatchlist}
                        onRemoveFromWatchlist={onRemoveFromWatchlist}
                        onAddToWishlist={onAddToWishlist}
                        onRemoveFromWishlist={onRemoveFromWishlist}
                    />
                ))}
            </div>
        </section>
    );
};

