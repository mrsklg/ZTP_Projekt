import { useState } from "react";
import { registerUser } from "../api/auth";
import {user} from 'react-icons-kit/fa/user';
import {lock} from 'react-icons-kit/ikons/lock';
import {mail} from 'react-icons-kit/ikons/mail'
import { Icon } from 'react-icons-kit';
import { Link, useNavigate } from "react-router-dom";

export default function RegisterForm() {
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [name, setName] = useState("")
    const [surname, setSurname] = useState("")
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        const data = await registerUser(email, password, name, surname);

        if (data.id) {
            navigate("/login");
        } else {
            alert("Register failed: " + (data.error || "Unknown error"));
        }
    }

    return (
        <div className="form-container">
            <h2>Register</h2>
            <form onSubmit={handleSubmit}>
                <div className="full-name">
                    <label className="form-label">Name
                        <div className="input-icon-wrapper">
                            <Icon icon={user} className="input-icon"/>
                            <input value={name} onChange={e=>setName(e.target.value)} placeholder="Name" />
                        </div>
                    </label>
                    <label className="form-label">Surname
                        <div className="input-icon-wrapper">
                            <Icon icon={user} className="input-icon"/>
                            <input value={surname} onChange={e=>setSurname(e.target.value)} placeholder="Surname" />
                        </div>
                    </label>
                </div>
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
                    <Link to="/login">Already have an account?</Link>
                </div>
                <button type="submit">Register</button>
            </form>
        </div>
    )
}
