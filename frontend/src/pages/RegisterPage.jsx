import '../styles/login.css'
import RegisterForm from '../components/RegisterForm'
import loginImg from '../assets/login-vector.svg';
import Footer from '../components/Footer';

export default function RegisterPage() {
  return (
    <>
    <div className='login-page'>
      <RegisterForm />
      <img className='login-image' src={loginImg} alt="Login"></img>  
    </div>
    <Footer></Footer>
    </>
  );
}