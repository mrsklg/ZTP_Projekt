import { Link } from 'react-router-dom';


export default function LinksPage() {
  return (
    <>
         <div style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '80vh',
        gap: '20px',
        padding: '20px',
        backgroundColor: '#f5f5f5'
      }}>
        <h1 style={{ 
          color: '#333',
          marginBottom: '30px',
          textAlign: 'center'
        }}>Navigation Links</h1>

          <Link to="login">login</Link>
          <Link to="register">register</Link>
          <Link to="dashboard">dashboard</Link>
          <Link to="browse">browse</Link>
          <Link to="film_details">film_details</Link>
          <Link to="liked">liked</Link>
          <Link to="settings">settings</Link>
          <Link to="to_watch">to_watch</Link>
          <Link to="watched">watched</Link>
        </div>
    </>
  );
}
