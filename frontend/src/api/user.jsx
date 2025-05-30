const API_URL = process.env.REACT_APP_API_URL;
const CHANGE_PASSWD_API_URL=`${API_URL}/user/change-password`;
const DELETE_ACCOUNT_API_URL = `${API_URL}/user/delete`;

export async function changePassword(oldPassword, newPassword) {
    const res = await fetch(CHANGE_PASSWD_API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
    },
    credentials: 'include',
    body: JSON.stringify({ new_password: newPassword, old_password: oldPassword }),
});

const data = await res.json();
if (!res.ok) {
    throw new Error(data.error || "Błąd zmiany hasła.");
}

return data;
}

export async function deleteAccount() {
    const res = await fetch(DELETE_ACCOUNT_API_URL, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json"
        },
        credentials: 'include'
    });
  
    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.error || "Nie udało się usunąć konta.");
    }

    return data;  
  }
  