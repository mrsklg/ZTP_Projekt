import { useNavigate } from 'react-router-dom';
import MovieTile from "./MovieTile";
import { BeatLoader } from "react-spinners";
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
    onRemoveFromWishlist,
    isLoading
    }) {
    const displayedMovies = maxItems ? movies.slice(0, maxItems) : movies;
    const navigate = useNavigate();

    const handleSeeMoreClick = () => {
        navigate(seeMoreLink);
    };

    const handleBrowseClick = () => {
        navigate("/browse");
    };

    const currentList = title === "To watch list" ? "wishlist" : "watchlist";

    return (
        <section className="movies-section">
            <div className={`movies-section-header ${additionalClass}`}>
                <h2>{title}</h2>
                {seeMoreLink &&  displayedMovies.length!=0 && <button className="show-more" onClick={handleSeeMoreClick}>
                    See more
                </button>}
            </div>
            <div className="movie-grid">
                {isLoading ? (
                    <div className="spinner-wrapper">
                        <BeatLoader color="#8FB6ABff"/>
                    </div>
                ) : displayedMovies.length === 0 ? (
                    <div className="empty-message">
                        <p>No movies on this list.</p>
                        <button className="browse-link" onClick={handleBrowseClick}>
                            Browse movies to add some →
                        </button>
                    </div>
                ) : (    
                    displayedMovies.map((movie) => (
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
                    )))}
            </div>
        </section>
    );
};

