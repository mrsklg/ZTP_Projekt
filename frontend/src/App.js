import './styles/global.css'
import React, { useEffect, useState } from 'react';
import { Container, Typography, Button, CircularProgress, List, ListItem, ListItemText } from '@mui/material';
import LoginPage from "./pages/LoginPage";
import RegisterPage from './pages/RegisterPage';

function App() {
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(true);
  const [users, setUsers] = useState([]);

  const [view, setView] = useState("home");
  useEffect(() => {
    fetch('http://localhost:8080/api/')
      .then(response => response.json())
      .then(data => {
        setMessage(data.message);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });

    fetch('http://localhost:8080/api/users')
      .then(response => response.json())
      .then(data => setUsers(data))
      .catch(err => console.error(err));
  }, []);

  return (

    <>
      {view ==="home" && 
      <Container>
        <Typography variant="h2" gutterBottom>
          Welcome to React & Flask Integration!
        </Typography>

        {loading ? (
          <CircularProgress />
        ) : (
          <Typography variant="h5" gutterBottom>
            {message}
          </Typography>
        )}

        <Button
          variant="contained"
          color="primary"
          onClick={() => window.alert('Button Clicked!')}
          style={{ marginTop: '20px' }}
        >
          Click Me
        </Button>

        <Typography variant="h4" style={{ marginTop: '40px' }}>
          User List
        </Typography>
        <List>
          {users.map((user) => (
            <ListItem key={user.id}>
              <ListItemText primary={`${user.name} (${user.email})`} />
            </ListItem>
          ))}
        </List>
        <Button onClick={()=> setView("login")}> Login </Button>
        <Button onClick={()=> setView("register")}> Register </Button>
        
      </Container> }
      {view === "login" && <LoginPage />}
      {view === "register" && <RegisterPage />}

    </>
    
  );
}

export default App;