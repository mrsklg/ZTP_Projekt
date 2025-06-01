import { Outlet } from "react-router";
import Footer from "./Footer";

export default function LayoutNotLogged() {
    return (
        <>
            <div className="content-container">
                <Outlet />
                <Footer />
            </div>
        </>
    )
}