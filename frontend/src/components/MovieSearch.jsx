import { useState, useEffect } from "react";
import { useNavigate } from 'react-router-dom';
import SearchBar from './SearchBar';
import MovieResult from './MovieResult';
import { fetchMovies } from '../api/movies';
import { BeatLoader } from "react-spinners";

export default function MovieSearch({ showLimit = false, maxResults = 3, withPagination = false, initialQuery = '' }) {
    const [query, setQuery] = useState('');
    const [movies, setMovies] = useState(null);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

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

    const handleSeeMoreClick = () => {
        navigate(`/browse?query=${encodeURIComponent(query)}`);
    };

    useEffect(() => {
        if (initialQuery.trim()) {
            setQuery(initialQuery);
        }
    }, [initialQuery]);

    useEffect(() => {
        if (query.trim() && query === initialQuery) {
            handleSearch();
        }
    }, [query, initialQuery]);

    return (
            <div className={showLimit ? 'limited-search-container' : 'search-container'}>
            <SearchBar
                query={query}
                onChange={(e) => setQuery(e.target.value)}
                onSearch={handleSearch}
                onClear={handleClearSearch}
            />
            {error && <p>Error: {error}</p>}
            {movies && movies.length > 0 && (
                <div className="search-results">
                    <h2 className={showLimit ? 'search-header-small' : ''}>Search Results</h2>
                    {loading ? (
                        <BeatLoader />
                    ) : (
                        <>
                            {(showLimit ? movies.slice(0, maxResults) : movies).map((movie) => (
                                <MovieResult
                                    key={movie.imdbID}
                                    movie={movie}
                                    showLimit={showLimit}
                                />
                            ))}
                            {showLimit && movies.length > maxResults && (
                                <button className="show-more" onClick={handleSeeMoreClick}>
                                    Show more
                                </button>
                            )}
                            {withPagination && (
                                <div className="pagination">
                                    {/* Tutaj dodaj komponent do paginacji jak będzie czas */}
                                    {/* <PaginationComponent /> */}
                                </div>
                            )}
                        </>
                    )}
                </div>
            )}
        </div>
    );

}