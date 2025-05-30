const API_URL = process.env.REACT_APP_API_URL;

export async function addToWishList(imdbID){
    //tu implementacja POST żey dodac film od danym imdbID do wishlisty
    const response = await fetch(`${API_URL}/wishlist`,{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        credentials: "include",
        body: JSON.stringify({imdbID})
    })
    // alert("Tu sie powinno dodać do wishListy")
    const data = await response.json();

    return data;
}

export async function removeFromWishList(imdbID){
    //tu implementacja DELETE żey usunąć film o danym imdbID z wishlisty
    const response = await fetch(`${API_URL}/wishlist`,{
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        },
        credentials: "include",
        body: JSON.stringify({imdbID})
    })
    // alert("Tu sie powinno usunąć z wishListy")
    const data = await response.json();
    
    return data;
}

export async function getWishList(){
    const response = await fetch(`${API_URL}/wishlist`,{
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
        credentials: "include"
    })
    return response;

    //symulacja
    // const dummyMovieIDs = {"wishlist":["tt0120338","tt0133093", "tt0111161", "tt1375666", "tt0120338"]}


    // return new Response(JSON.stringify(dummyMovieIDs), {
    //     status: 200,
    //     headers: {
    //         'Content-Type': 'application/json'
    //     }
    // });
}