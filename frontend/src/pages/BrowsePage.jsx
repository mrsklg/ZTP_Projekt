import { useSearchParams } from 'react-router-dom';
import MovieSearch from "../components/MovieSearch";
import '../styles/browse.css'

export default function BrowsePage() {
  const [searchParams] = useSearchParams();
  const query = searchParams.get('query') || '';
  return (
    <>
        <h1>Browse</h1>
        <MovieSearch 
              initialQuery={query}
              showLimit={false}
              withPagination={true} 
        />
    </>
  );
}
