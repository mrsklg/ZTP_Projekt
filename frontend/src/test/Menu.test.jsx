import { render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router';
import userEvent from '@testing-library/user-event';
import Menu from '../components/Menu';

test('marks Dashboard link as active when on dashboard route', () => {
    render(
        <MemoryRouter initialEntries={['/dashboard']}>
            <Menu />
        </MemoryRouter>
    );

    const dashboardLink = screen.getByText('Dashboard').closest('a');
    expect(dashboardLink).toHaveClass('active');

    const browseLink = screen.getByText('Browse').closest('a');
    expect(browseLink).not.toHaveClass('active');
});

test('renders all menu items correctly', () => {
    render(
        <MemoryRouter>
            <Menu />
        </MemoryRouter>
    );

    const expectedItems = ['Dashboard', 'Browse', 'Settings', 'To Watch', 'Watched'];

    expectedItems.forEach(itemText => {
        expect(screen.getByText(itemText)).toBeInTheDocument();
    });
});

test('renders logout button', () => {
    render(
        <MemoryRouter>
            <Menu />
        </MemoryRouter>
    );

    expect(screen.getByText('Logout')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /logout/i })).toBeInTheDocument();
});


test('navigates to correct routes', () => {
    const { container } = render(
        <MemoryRouter>
        <Menu />
      </MemoryRouter>
    );
    
    // Sprawdzamy atrybuty href linków
    const dashboardLink = screen.getByText('Dashboard').closest('a');
    expect(dashboardLink).toHaveAttribute('href', '/dashboard');
    
    const browseLink = screen.getByText('Browse').closest('a');
    expect(browseLink).toHaveAttribute('href', '/browse');
});

test('toggles mobile menu when button is clicked', async () => {
    // 1. Symulujemy mniejszy ekran
    window.innerWidth = 500;
    
    // 2. Renderujemy komponent
    render(
        <MemoryRouter>
            <Menu />
        </MemoryRouter>
    );

    // 3. Menu powinno być początkowo zamknięte na mobile
    expect(screen.queryByText('Dashboard')).not.toBeInTheDocument();

    // 4. Znajdujemy i klikamy przycisk menu
    const menuButtons = screen.getAllByRole('button'); // Znajdź wszystkie przyciski
    const toggleButton = menuButtons.find(button => 
        button.classList.contains('menu-toggle-button')
    );
    
    await userEvent.click(toggleButton);
    

    // 5. Menu powinno być teraz widoczne
    expect(screen.getByText('Dashboard')).toBeInTheDocument();
    
});