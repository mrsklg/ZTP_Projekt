import { Outlet } from "react-router";
import Footer from "./Footer";
import SideMenu from "./Menu";

export default function Layout() {
    return (
        <>
            <SideMenu />
            <div className="content-container">
                <Outlet />
                <Footer />
            </div>
        </>
    )
}