import './styles/global.css'
import React, { useEffect, useState } from 'react';
import { Container, Typography, Button, CircularProgress, List, ListItem, ListItemText } from '@mui/material';
import LoginPage from "./pages/LoginPage";
import RegisterPage from './pages/RegisterPage';
import { BrowserRouter as Router, Routes, Route, Navigate, Link } from 'react-router-dom';
import DashboardPage from './pages/DashboardPage';
import BrowsePage from './pages/BrowsePage';
import FilmDetailsPage from './pages/FilmDetailsPage';
import LikedPage from './pages/LikedPage';
import SettingsPage from './pages/SettingsPage';
import ToWatchPage from './pages/ToWatchPage';
import WatchedPage from './pages/WatchedPage';
import LinksPage from './pages/LinksPage';

function App() {
  return (
    <Router>
      <div className='App'>
        <Routes>
          <Route path='login' element={<LoginPage/>} />
          <Route path='register' element={<RegisterPage/>} />|
          <Route path='dashboard' element={<DashboardPage/>} />|
          <Route path='browse' element={<BrowsePage/>} />|
          <Route path="/movie/:id" element={<FilmDetailsPage />} />
          <Route path='liked' element={<LikedPage/>} />|
          <Route path='settings' element={<SettingsPage/>} />|
          <Route path='to_watch' element={<ToWatchPage/>} />|
          <Route path='watched' element={<WatchedPage/>} />|
          
          <Route path='/' element={<LinksPage />} />|

          <Route path='*' element={<Navigate to="/login" replace />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App;