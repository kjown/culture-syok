<script>
    export let title;
    import { page } from '$app/stores';
    
    $: currentPath = $page.url.pathname;
    
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
        
        <!-- Navigation Links -->
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
            <!-- Google Calendar Connect Button -->
            <a class="connect-btn" href="/api/auth/google">
                <i class="fab fa-google me-2"></i>
                Connect
            </a>

            <!-- User Profile -->
            <div class="dropdown">
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

    /* Responsive */
    @media (max-width: 992px) {
        .nav-container {
            display: none;
        }
        
        .brand-title {
            font-size: 1.125rem;
        }
    }
</style>
