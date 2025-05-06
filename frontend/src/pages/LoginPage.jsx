import '../styles/login.css'
import LoginForm from "../components/LoginForm";
import loginImg from '../assets/login-vector.svg';

export default function LoginPage() {
  return (
    <div className='login-page'>
      <LoginForm />
      <img className='login-image' src={loginImg} alt="Login"></img>
    </div>
  );
}
