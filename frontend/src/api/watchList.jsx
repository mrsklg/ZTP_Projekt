const API_URL = process.env.REACT_APP_API_URL;

export async function addToWatchList(imdbID) {
    //tu implementacja POST żey dodac film od danym imdbID do wishlisty
    const response = await fetch(`${API_URL}/watchlist`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        credentials: 'include',
        body: JSON.stringify({ imdbID })
    })
    // alert("Tu sie powinno dodać do watchListy")
    const data = await response.json();

    return data;
}

export async function removeFromWatchList(imdbID) {
    //tu implementacja DELETE żey usunąć film o danym imdbID z wishlisty
    const response = await fetch(`${API_URL}/watchlist`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        },
        credentials: 'include',
        body: JSON.stringify({ imdbID })
    })
    // alert("Tu się powinno usunąć z watchListy")

    const data = await response.json();

    return data;
}

export async function getWatchList() {
    const response = await fetch(`${API_URL}/watchlist`,{
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
        credentials: "include"
    })
    return response;
    //symulacja
    // const dummyMovieIDs = {"watchlist":[]}

    // return new Response(JSON.stringify(dummyMovieIDs), {
    //     status: 200,
    //     headers: {
    //         'Content-Type': 'application/json'
    //     }
    // });

}