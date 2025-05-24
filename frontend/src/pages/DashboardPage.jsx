import MovieSearch from '../components/MovieSearch';
import '../styles/dashboard.css'

export default function DashboardPage() {
  return (
    <>
        <title>Dashboard</title>
        <MovieSearch showLimit={true} maxResults={3} withPagination={false}></MovieSearch>
        <h1>Watched movies</h1>
        <p>sekcja z obejrzanymi filmami</p>
        <h1>Wishlist movies</h1>
        <p>sekcja z chce obejrzeć filmami</p>
        dashboard z podsumowaniem, statystykami, linkami do list, itp.
    </>
  );
}
