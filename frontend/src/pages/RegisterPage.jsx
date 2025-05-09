import '../styles/login.css'
import RegisterForm from '../components/RegisterForm'
import loginImg from '../assets/login-vector.svg';


export default function RegisterPage() {
  return (
    <>
    <div className='login-page'>
      <RegisterForm />
      <img className='login-image' src={loginImg} alt="Login"></img>  
    </div>
    </>
  );
}