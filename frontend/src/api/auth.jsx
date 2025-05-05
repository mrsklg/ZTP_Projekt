const LOGIN_API_URL='http://localhost:5000/api/login';
const REGISTER_API_URL='http://localhost:5000/api/register'

export async function loginUser(email, password){
    const response = await fetch(LOGIN_API_URL, {
        method: "POST",
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({email, password})
    });

    return response.json();
}

export async function registerUser(email, password, name, surname) {
    const response = await fetch(REGISTER_API_URL, {
        method: "POST",
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({email, password, name, surname})
    });
    
    return response.json();
}