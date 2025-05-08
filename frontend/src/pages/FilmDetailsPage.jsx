import { useParams } from 'react-router-dom';

export default function FilmDetailsPage() {
  const { id } = useParams();
  return (
    <>
        <h1>FilmDetails</h1>
        informacje o filmie {id}
    </>
  );
}
