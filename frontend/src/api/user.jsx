
export async function changePassword(currentPassword, newPassword) {
    // const res = await fetch("/api/user/change-password", {
    //   method: "POST",
    //   headers: {
    //     "Content-Type": "application/json",
    //     Authorization: `Bearer ${localStorage.getItem("token")}`,
    //   },
    //   body: JSON.stringify({ currentPassword, newPassword }),
    // });
  
    // const data = await res.json();
    // if (!res.ok) {
    //   throw new Error(data.error || "Błąd zmiany hasła.");
    // }
  
    return new Response({
        status: 200,
        headers: {
            'Content-Type': 'application/json'
        }
    });
  }
  
  export async function deleteAccount() {
    // const res = await fetch("/api/user/delete", {
    //   method: "DELETE",
    //   headers: {
    //     Authorization: `Bearer ${localStorage.getItem("token")}`,
    //   },
    // });
  
    // if (!res.ok) {
    //   const data = await res.json();
    //   throw new Error(data.error || "Nie udało się usunąć konta.");
    // }
  
    return new Response({
        status: 200,
        headers: {
            'Content-Type': 'application/json'
        }
    });
  }
  