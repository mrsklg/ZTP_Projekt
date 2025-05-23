const MOVIES_URL = "https://www.omdbapi.com/"
const API_KEY = "6205c32a";

export async function fetchMovies(query) {
    
    const url = `${MOVIES_URL}?s=${encodeURIComponent(query)}&apikey=${API_KEY}`;

    const response = await fetch(url);
    const data = await response.json()
    if (data.Response === "True") {
        return data.Search;
    } else {
        throw new Error(data.Error || "Nie znaleziono filmu.");
    }
}

export async function getMovie(movieID) {
    const url = `${MOVIES_URL}?i=${encodeURIComponent(movieID)}&apikey=${API_KEY}`;
    const response = await fetch(url);
    const data = await response.json()
    if (data.Response === "True") {
        return data;
    } else {
        throw new Error(data.Error || "Nie znaleziono filmu.");
    }
}