import { Typography } from "@mui/material"

export default function Footer() {
    return (
        <footer className="footer">
            <span className="footer-text">Aplikacja ZTP</span>
            <div className="footer-column">
                <Typography variant="body2" color="textSecondary">Made with ❤️ by people</Typography>
                <a href="https://storyset.com/user">User illustrations by Storyset</a>
            </div>
        </footer>
    )
}