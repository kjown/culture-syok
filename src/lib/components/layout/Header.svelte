<script>
    export let title;
    import { page } from '$app/stores';
    
    $: currentPath = $page.url.pathname;
    
    // Mobile menu state
    let mobileMenuOpen = false;
    
    // Mock user data - in real app this would come from a store or API
    const user = {
        name: "LeBron",
        avatar: "https://i.redd.it/g02yu8ecgvca1.jpg"
    };
    
    const navItems = [
        { href: '/', label: 'Dashboard', icon: 'fas fa-chart-line' },
        { href: '/scheduler', label: 'Scheduler', icon: 'fas fa-calendar-alt' },
        { href: '/inspiration', label: 'Inspiration', icon: 'fas fa-lightbulb' },
        { href: '/collaborate', label: 'Collaborate', icon: 'fas fa-users' },
        { href: '/library', label: 'Library', icon: 'fas fa-folder-open' }
    ];
    
    function toggleMobileMenu() {
        mobileMenuOpen = !mobileMenuOpen;
    }
    
    function closeMobileMenu() {
        mobileMenuOpen = false;
    }
</script>

<nav class="navbar px-4 py-3">
    <div class="container-fluid d-flex justify-content-between align-items-center">
        <!-- Brand/Logo -->
        <div class="d-flex align-items-center">
            <div class="brand-logo me-3">
                <i class="fas fa-rocket"></i>
            </div>
            <h5 class="brand-title mb-0">{title}</h5>
        </div>
        
        <!-- Navigation Links (Desktop) -->
        <div class="nav-container d-flex align-items-center">
            {#each navItems as item}
                <a 
                    class="nav-item" 
                    href={item.href}
                    class:active={currentPath === item.href}
                >
                    <i class={item.icon}></i>
                    <span>{item.label}</span>
                </a>
            {/each}
        </div>

        <!-- Right Section -->
        <div class="d-flex align-items-center gap-4">
            <!-- Google Calendar Connect Button (Desktop) -->
            <a class="connect-btn desktop-only" href="/api/auth/google">
                <i class="fab fa-google me-2"></i>
                Connect
            </a>

            <!-- User Profile (Desktop) -->
            <div class="dropdown desktop-only">
                <button 
                    class="user-profile-btn"
                    type="button"
                    data-bs-toggle="dropdown"
                >
                    <img
                        src={user.avatar}
                        alt="User Avatar"
                        class="user-avatar"
                    />
                </button>
                <ul class="dropdown-menu dropdown-menu-end user-dropdown">
                    <li class="user-info">
                        <div class="user-name">{user.name}</div>
                        <div class="user-role">Administrator</div>
                    </li>
                    <li><a class="dropdown-item logout-item" href="/api/auth/logout"><i class="fas fa-sign-out-alt me-2"></i>Logout</a></li>
                </ul>
            </div>
            
            <!-- Mobile Menu Toggle -->
            <button 
                class="mobile-menu-toggle mobile-only"
                on:click={toggleMobileMenu}
                aria-label="Toggle navigation menu"
            >
                <span class="hamburger-line" class:open={mobileMenuOpen}></span>
                <span class="hamburger-line" class:open={mobileMenuOpen}></span>
                <span class="hamburger-line" class:open={mobileMenuOpen}></span>
            </button>
        </div>
    </div>
    
    <!-- Mobile Navigation Menu -->
    <div class="mobile-nav" class:open={mobileMenuOpen}>
        <!-- Backdrop - click to close -->
        <!-- svelte-ignore a11y-no-static-element-interactions a11y-click-events-have-key-events -->
        <div class="mobile-nav-backdrop" on:click={closeMobileMenu}></div>
        
        <div class="mobile-nav-content">
            <!-- Close button -->
            <div class="mobile-nav-header">
                <h6 class="mobile-nav-title">Menu</h6>
                <button class="mobile-close-btn" on:click={closeMobileMenu} aria-label="Close menu">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            
            <!-- Mobile Navigation Items -->
            <div class="mobile-nav-items">
                {#each navItems as item}
                    <a 
                        class="mobile-nav-item" 
                        href={item.href}
                        class:active={currentPath === item.href}
                        on:click={closeMobileMenu}
                    >
                        <i class={item.icon}></i>
                        <span>{item.label}</span>
                    </a>
                {/each}
            </div>
            
            <!-- Mobile User Section -->
            <div class="mobile-user-section">
                <div class="mobile-user-info">
                    <img
                        src={user.avatar}
                        alt="User Avatar"
                        class="mobile-user-avatar"
                    />
                    <div class="mobile-user-details">
                        <div class="mobile-user-name">{user.name}</div>
                        <div class="mobile-user-role">Administrator</div>
                    </div>
                </div>
                
                <a class="mobile-connect-btn" href="/api/auth/google" on:click={closeMobileMenu}>
                    <i class="fab fa-google me-2"></i>
                    Connect Calendar
                </a>
                
                <a class="mobile-logout-btn" href="/api/auth/logout" on:click={closeMobileMenu}>
                    <i class="fas fa-sign-out-alt me-2"></i>
                    Logout
                </a>
            </div>
        </div>
    </div>
</nav>

<style>
    .navbar {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(20px);
        border: none;
        border-bottom: 1px solid rgba(0, 0, 0, 0.05);
        padding: 1rem 0;
    }

    /* Brand */
    .brand-logo {
        width: 36px;
        height: 36px;
        background: #667eea;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 1rem;
    }

    .brand-title {
        color: #1a202c;
        font-weight: 600;
        font-size: 1.25rem;
        letter-spacing: -0.025em;
    }

    /* Navigation */
    .nav-container {
        gap: 0.5rem;
    }

    .nav-item {
        display: flex;
        align-items: center;
        padding: 0.75rem 1rem;
        color: #64748b;
        text-decoration: none;
        border-radius: 8px;
        font-weight: 500;
        font-size: 0.875rem;
        transition: all 0.2s ease;
        position: relative;
    }

    .nav-item i {
        margin-right: 0.5rem;
        font-size: 0.875rem;
        width: 16px;
        text-align: center;
    }

    .nav-item:hover {
        color: #667eea;
        background: rgba(102, 126, 234, 0.05);
        text-decoration: none;
    }

    .nav-item.active {
        color: #667eea;
        background: rgba(102, 126, 234, 0.1);
        font-weight: 600;
    }

    /* Connect Button */
    .connect-btn {
        display: flex;
        align-items: center;
        padding: 0.625rem 1rem;
        background: #667eea;
        color: white;
        text-decoration: none;
        border-radius: 8px;
        font-weight: 500;
        font-size: 0.875rem;
        transition: all 0.2s ease;
        border: none;
    }

    .connect-btn:hover {
        background: #5a67d8;
        color: white;
        text-decoration: none;
        transform: translateY(-1px);
    }

    /* User Profile */
    .user-profile-btn {
        background: none;
        border: none;
        padding: 0;
        position: relative;
    }

    .user-avatar {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        border: 2px solid rgba(102, 126, 234, 0.1);
        transition: all 0.2s ease;
    }

    .user-profile-btn:hover .user-avatar {
        border-color: #667eea;
        transform: scale(1.05);
    }

    /* Dropdown */
    .user-dropdown {
        border: none;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        border-radius: 12px;
        padding: 0.5rem;
        min-width: 200px;
        margin-top: 0.5rem;
    }

    .user-info {
        padding: 0.75rem 1rem 0.5rem;
        border-bottom: 1px solid rgba(0, 0, 0, 0.05);
        margin-bottom: 0.5rem;
    }

    .user-name {
        font-weight: 600;
        font-size: 0.875rem;
        color: #1a202c;
        margin-bottom: 0.25rem;
    }

    .user-role {
        font-size: 0.75rem;
        color: #64748b;
    }

    .dropdown-item {
        padding: 0.5rem 1rem;
        border-radius: 6px;
        font-size: 0.875rem;
        color: #374151;
        transition: all 0.2s ease;
        margin-bottom: 0.25rem;
    }

    .dropdown-item:hover {
        background: rgba(102, 126, 234, 0.05);
        color: #667eea;
    }

    .logout-item:hover {
        background: rgba(239, 68, 68, 0.05);
        color: #ef4444;
    }

    .dropdown-divider {
        margin: 0.5rem 0;
        border-color: rgba(0, 0, 0, 0.05);
    }

    /* Mobile Menu Toggle */
    .mobile-menu-toggle {
        display: none;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        width: 40px;
        height: 40px;
        background: none;
        border: none;
        cursor: pointer;
        padding: 8px;
        border-radius: 6px;
        transition: background-color 0.2s ease;
    }

    .mobile-menu-toggle:hover {
        background: rgba(102, 126, 234, 0.1);
    }

    .hamburger-line {
        width: 24px;
        height: 2px;
        background-color: #64748b;
        margin: 3px 0;
        transition: all 0.3s ease;
        border-radius: 2px;
    }

    .hamburger-line.open:nth-child(1) {
        transform: rotate(45deg) translate(5px, 5px);
    }

    .hamburger-line.open:nth-child(2) {
        opacity: 0;
    }

    .hamburger-line.open:nth-child(3) {
        transform: rotate(-45deg) translate(7px, -6px);
    }

    /* Mobile Navigation */
    .mobile-nav {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100vh;
        z-index: 9998;
        transform: translateX(-100%);
        transition: transform 0.3s ease;
        display: none;
    }

    .mobile-nav.open {
        transform: translateX(0);
    }

    .mobile-nav-backdrop {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(10px);
    }

    .mobile-nav-content {
        position: relative;
        width: 280px;
        height: 100%;
        background: white;
        padding: 0;
        box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
        display: flex;
        flex-direction: column;
        z-index: 10;
    }

    .mobile-nav-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 1.5rem 1rem;
        border-bottom: 1px solid rgba(0, 0, 0, 0.1);
        background: rgba(102, 126, 234, 0.05);
    }

    .mobile-nav-title {
        margin: 0;
        font-weight: 600;
        color: #2d3748;
        font-size: 1.125rem;
    }

    .mobile-close-btn {
        background: none;
        border: none;
        color: #64748b;
        font-size: 1.25rem;
        cursor: pointer;
        padding: 0.5rem;
        border-radius: 50%;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 36px;
        height: 36px;
    }

    .mobile-close-btn:hover {
        background: rgba(102, 126, 234, 0.1);
        color: #667eea;
    }

    .mobile-nav-items {
        padding: 1rem;
        flex: 1;
    }

    .mobile-nav-item {
        display: flex;
        align-items: center;
        padding: 1rem;
        color: #64748b;
        text-decoration: none;
        border-radius: 8px;
        font-weight: 500;
        font-size: 1rem;
        transition: all 0.2s ease;
        margin-bottom: 0.5rem;
    }

    .mobile-nav-item i {
        margin-right: 1rem;
        font-size: 1.125rem;
        width: 20px;
        text-align: center;
    }

    .mobile-nav-item:hover {
        color: #667eea;
        background: rgba(102, 126, 234, 0.05);
        text-decoration: none;
    }

    .mobile-nav-item.active {
        color: #667eea;
        background: rgba(102, 126, 234, 0.1);
        font-weight: 600;
    }

    /* Mobile User Section */
    .mobile-user-section {
        padding: 1rem;
        border-top: 1px solid rgba(0, 0, 0, 0.1);
    }

    .mobile-user-info {
        display: flex;
        align-items: center;
        padding: 1rem;
        margin-bottom: 1rem;
        background: rgba(102, 126, 234, 0.05);
        border-radius: 12px;
    }

    .mobile-user-avatar {
        width: 48px;
        height: 48px;
        border-radius: 50%;
        border: 2px solid rgba(102, 126, 234, 0.2);
        margin-right: 1rem;
    }

    .mobile-user-name {
        font-weight: 600;
        font-size: 1rem;
        color: #1a202c;
        margin-bottom: 0.25rem;
    }

    .mobile-user-role {
        font-size: 0.875rem;
        color: #64748b;
    }

    .mobile-connect-btn,
    .mobile-logout-btn {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 0.875rem 1rem;
        border-radius: 8px;
        font-weight: 500;
        font-size: 0.875rem;
        text-decoration: none;
        transition: all 0.2s ease;
        margin-bottom: 0.5rem;
        width: 100%;
    }

    .mobile-connect-btn {
        background: #667eea;
        color: white;
    }

    .mobile-connect-btn:hover {
        background: #5a67d8;
        color: white;
        text-decoration: none;
    }

    .mobile-logout-btn {
        background: rgba(239, 68, 68, 0.1);
        color: #ef4444;
    }

    .mobile-logout-btn:hover {
        background: rgba(239, 68, 68, 0.2);
        color: #dc2626;
        text-decoration: none;
    }

    /* Responsive Visibility Classes */
    .desktop-only {
        display: flex;
    }

    .mobile-only {
        display: none;
    }

    /* Responsive */
    @media (max-width: 992px) {
        .nav-container {
            display: none !important;
        }
        
        .desktop-only {
            display: none !important;
        }
        
        .mobile-only {
            display: flex !important;
        }
        
        .mobile-nav {
            display: block;
        }
        
        .brand-title {
            font-size: 1.125rem;
        }
    }
</style>
