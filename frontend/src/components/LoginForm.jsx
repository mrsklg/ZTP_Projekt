import { useState } from "react";
import { loginUser } from "../api/auth";
import { mail } from 'react-icons-kit/ikons/mail'
import { lock } from 'react-icons-kit/ikons/lock';
import { Icon } from 'react-icons-kit';
import { Link } from "react-router";

export default function LoginForm() {
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")

    const handleSubmit = async (e) => {
        e.preventDefault();
        await loginUser(email, password);
    }

    return (
        <div className="form-container">
            <h2>Login</h2>
            <form onSubmit={handleSubmit}>
                <label className="form-label">Email
                    <div className="input-icon-wrapper">
                        <Icon icon={mail} className="input-icon"/>
                        <input value={email} onChange={e=>setEmail(e.target.value)} placeholder="Email" />
                    </div>
                </label>
                <label className="form-label">Password
                    <div className="input-icon-wrapper">
                        <Icon icon={lock} className="input-icon"/>
                        <input value={password} onChange={e=>setPassword(e.target.value)} type='password' placeholder="Password" />
                    </div>
                </label>
                <div className="form-bottom">
                    <Link to="/register">Don't have an account?</Link>
                </div>
                <button type="submit">Log in</button>
            </form>
        </div>
    )
}