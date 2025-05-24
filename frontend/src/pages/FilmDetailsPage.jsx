import { useEffect } from 'react';
import { useState } from 'react';
import { useParams } from 'react-router-dom';
import MovieTile from '../components/MovieTile';
import { getMovie } from '../api/movies';
import "../styles/filmDetails.css"

export default function FilmDetailsPage() {
  const [movie, setMovie] = useState(null);
  const { id } = useParams();

  useEffect(() => {
    const fetchMovie = async () => {
      try {
        const data = await getMovie(id);
        setMovie(data);
      } catch (err) {
        console.error(err);
      } 
    };

    fetchMovie();
  }, [id]);

  return (
  <>
    {movie ? (
      <MovieTile movie={movie} isDetailsOpened={true} />
    ) : (
      <p>Loading...</p>
    )}
  </>
);
}
