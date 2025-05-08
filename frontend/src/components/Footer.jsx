import { Typography } from "@mui/material"
import logoImg from '../assets/logo.png';
import '../styles/footer.css';

export default function Footer() {
    return (
        <footer className="footer">
            <img src={logoImg} className="logo-footer" alt="Watchy Logo" />
            <div className="footer-column">
                <Typography variant="body2" color="textSecondary">Made with ❤️ by people</Typography>
                <a href="https://storyset.com/user">User illustrations by Storyset</a>
            </div>
        </footer>
    )
}