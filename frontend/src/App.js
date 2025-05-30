import './styles/global.css'
import React from 'react';
import LoginPage from "./pages/LoginPage";
import RegisterPage from './pages/RegisterPage';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import DashboardPage from './pages/DashboardPage';
import BrowsePage from './pages/BrowsePage';
import FilmDetailsPage from './pages/FilmDetailsPage';
import SettingsPage from './pages/SettingsPage';
import ToWatchPage from './pages/ToWatchPage';
import WatchedPage from './pages/WatchedPage';
//import LinksPage from './pages/LinksPage';
import Layout from './components/Layout';
import LayoutNotLogged from './components/LayoutNotLogged';
import { AuthProvider } from './components/AuthContext';
import PrivateRoute from './components/PrivateRoute';

function App() {
  return (
    <Router>
        <AuthProvider>
        <div className='app-container'>
          <Routes>
            
            <Route element={<LayoutNotLogged />}>
              <Route path='login' element={<LoginPage/>} />
              <Route path='register' element={<RegisterPage/>} />|
              <Route path='/' element={<RegisterPage />} />|
            </Route>

            <Route element={<PrivateRoute />}>
              <Route element={<Layout />}>
                <Route path='dashboard' element={<DashboardPage/>} />|
                <Route path='browse' element={<BrowsePage/>} />|
                <Route path="/movie/:id" element={<FilmDetailsPage />} />
                <Route path='settings' element={<SettingsPage/>} />|
                <Route path='to_watch' element={<ToWatchPage/>} />|
                <Route path='watched' element={<WatchedPage/>} />|
                
              </Route>
            </Route>

            <Route path='*' element={<Navigate to="/login" replace />} />
          </Routes>
        </div>
      </AuthProvider>
    </Router>
  )
}

export default App;