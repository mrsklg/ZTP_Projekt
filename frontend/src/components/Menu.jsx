import { NavLink, useNavigate } from "react-router"
import '../styles/menu.css';
import { 
    magnifying_glass, 
    cog, 
    home  
} from 'react-icons-kit/ikons';
import { check, clockO, signOut, bars } from 'react-icons-kit/fa/'
import { Icon } from 'react-icons-kit';
import { useState } from "react";
import { logoutUser } from "../api/auth";

export default function Menu() {

    const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
    const navigate = useNavigate();
    
    const handleLogout = async () => {
        const data = await logoutUser();
        if (data.message === "Wylogowano") {
            navigate('/login');
        } else {
            alert('Nastąpił problem z wylogowaniem');
        }
    };

    const menuItems = [
        { to: "dashboard", icon: home, label: "Dashboard" },
        { to: "browse", icon: magnifying_glass, label: "Browse" },
        { to: "settings", icon: cog, label: "Settings" },
        { to: "to_watch", icon: clockO, label: "To Watch" },
        { to: "watched", icon: check, label: "Watched" }
    ];

    return (
        <>
            {(isMobileMenuOpen || window.innerWidth >= 768) ? (
                <div className="menu-container">
                    <div className="menu-toggle">
                        <button onClick={() => setIsMobileMenuOpen(prev => !prev)} className="menu-toggle-button">
                            <Icon icon={bars} size={20} />
                        </button>
                    </div>
                    <div className="menu-top">
                        {menuItems.map((item) => (
                            <NavLink 
                                key={item.to}
                                to={item.to}
                                className={({ isActive }) => 
                                    `menu-link ${isActive ? 'active' : ''}`
                                }
                            >
                                <Icon icon={item.icon} size={20} className="menu-icon" />
                                <span>{item.label}</span>
                            </NavLink>
                        ))}
                    </div>

                    <div className="menu-bottom">
                        <button onClick={handleLogout} className="logout-button">
                            <Icon icon={signOut} size={20} className="menu-icon" />
                            <span>Logout</span>
                        </button>
                    </div>
                </div>) : (
                    <div className="menu-toggle menu-toggle-floating">
                        <button
                            onClick={() => setIsMobileMenuOpen(true)}
                            className="menu-toggle-button"
                        >
                            <Icon icon={bars} size={24} />
                        </button>
                    </div>
                )}
        </>
    )
}