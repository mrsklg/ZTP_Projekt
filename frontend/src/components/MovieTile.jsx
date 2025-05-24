import { useNavigate } from 'react-router-dom';
import noPoster from '../assets/No data.svg';
import '../styles/movie.css'

export default function MovieTile({ movie, isDetailsOpened = false }) {
    const navigate = useNavigate();

    const handleMovieClick = () => {
        navigate(`/movie/${movie.imdbID}`);
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
                </div>
            </div>
            {isDetailsOpened && (
                <div className="movie-details">
                    <p><strong>Plot:</strong> {movie.Plot}</p>
                    <p><strong>Director:</strong> {movie.Director}</p>
                    <p><strong>Actors:</strong> {movie.Actors}</p>
                    <p><strong>Language:</strong> {movie.Language}</p>
                    <p><strong>Country:</strong> {movie.Country}</p>
                    <p><strong>Box Office:</strong> {movie.BoxOffice}</p>
                    <p><strong>IMDb Rating:</strong> ⭐ {movie.imdbRating}</p>
                    <div className="ratings">
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