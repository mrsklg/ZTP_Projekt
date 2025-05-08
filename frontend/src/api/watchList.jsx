const BACKEND_API='/api'

export async function addToWatchList(imdbID){
    //tu implementacja POST żey dodac film od danym imdbID do wishlisty
    const response = await fetch(`${BACKEND_API}/watchlist`,{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({imdbID})
    })
    alert("Tu sie powinno dodać do watchListy")
}