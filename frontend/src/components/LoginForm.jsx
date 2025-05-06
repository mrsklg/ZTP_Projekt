import { useState } from "react";
import { loginUser } from "../api/auth";
import { mail } from 'react-icons-kit/ikons/mail'
import { lock } from 'react-icons-kit/ikons/lock';
import { Icon } from 'react-icons-kit';

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
                    <a href="/register">Don't have an account?</a>
                </div>
                <button type="submit">Log in</button>
            </form>
        </div>
    )
}