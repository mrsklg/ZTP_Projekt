const BACKEND_API = '/api'

export async function addToWatchList(imdbID) {
    //tu implementacja POST żey dodac film od danym imdbID do wishlisty
    const response = await fetch(`${BACKEND_API}/watchlist`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ imdbID })
    })
    alert("Tu sie powinno dodać do watchListy")
}

export async function removeFromWatchList(imdbID) {
    //tu implementacja DELETE żey usunąć film o danym imdbID z wishlisty
    const response = await fetch(`${BACKEND_API}/watchlist`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ imdbID })
    })
    alert("Tu się powinno usunąć z watchListy")
}

export async function getWatchList() {
    // const response = await fetch(`${BACKEND_API}/watchlist`,{
    //     method: 'GET',
    //     headers: {
    //         'Content-Type': 'application/json'
    //     }
    // })
    // return response

    //symulacja
    const dummyMovieIDs = ["tt0133093", "tt0111161", "tt1375666", "tt0120338", "tt0133093", "tt0111161", "tt1375666", "tt0120338", "tt0133093", "tt0111161", "tt1375666", "tt0120338"]; // np. Matrix, Shawshank, Inception


    return new Response(JSON.stringify(dummyMovieIDs), {
        status: 200,
        headers: {
            'Content-Type': 'application/json'
        }
    });
}