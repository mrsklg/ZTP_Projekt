const BACKEND_API='/api'

export async function addToWishList(imdbID){
    //tu implementacja POST żey dodac film od danym imdbID do wishlisty
    const response = await fetch(`${BACKEND_API}/wishlist`,{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({imdbID})
    })
    alert("Tu sie powinno dodać do wishListy")
}