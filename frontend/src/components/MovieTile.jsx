import { useNavigate } from 'react-router-dom';
import noPoster from '../assets/No data.svg';
import '../styles/movie.css'

export default function MovieTile({ movie }) {
    const navigate = useNavigate();

    const handleMovieClick = () => {
        navigate(`/movie/${movie.imdbID}`);
    };

    return (
        <div className="movie-tile" onClick={handleMovieClick}>
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
    )

}