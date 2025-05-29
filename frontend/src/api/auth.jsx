const API_URL = process.env.REACT_APP_API_URL;
const LOGOUT_API_URL=`${API_URL}/logout`;
const LOGIN_API_URL = `${API_URL}/login`;
const REGISTER_API_URL = `${API_URL}/register`;

export async function loginUser(email, password){
    const response = await fetch(LOGIN_API_URL, {
        method: "POST",
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({email, password})
    });

    return response.json();
}

export async function logoutUser(){
    const response = await fetch(LOGOUT_API_URL, {
        method: "POST",
        headers: {'Content-Type':'application/json'},
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