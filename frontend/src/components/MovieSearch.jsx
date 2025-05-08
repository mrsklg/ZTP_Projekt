import { useState } from "react";
import SearchBar from './SearchBar';
import MovieResult from './MovieResult';
import { fetchMovies } from '../api/movies';

export default function MovieSearch() {
    const [query, setQuery] = useState('');
    const [movies, setMovies] = useState(null);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);
    
    const handleSearch = async () => {
        if (!query.trim()) {
            setError("Please enter a search term");
            return; 
        }
        setLoading(true);
        setError(null);
        setMovies(null);
        try {
            const data = await fetchMovies(query);
            setMovies(data);
        } catch (error) {
            setError(error.message);
        } finally {
            setLoading(false);
        }
    };

    const handleClearSearch = () => {
        setQuery(''); 
        setMovies(null); 
    };

    return (
        <div>
            <SearchBar
                query={query}
                onChange={(e) => setQuery(e.target.value)}
                onSearch={handleSearch}
                onClear={handleClearSearch}
            />
            {loading && <p>Loading...</p>}
            {error && <p>Error: {error}</p>}
            {movies && movies.length > 0 && (
                <div className="search-results">
                    <h2>Search Results</h2>
                    {movies.map((movie) => (
                        <MovieResult
                            key={movie.imdbID}
                            movie={movie}
                            
                        />
                    ))}
                </div>
            )}

        </div>

    )

}