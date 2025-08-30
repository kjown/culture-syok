<script>
    import { page } from '$app/stores';
    
    $: currentPath = $page.url.pathname;
    
    const navItems = [
        { href: '/', label: 'Dashboard', icon: 'fas fa-chart-line' },
        { href: '/trends', label: 'Trends', icon: 'fas fa-trending-up' },
        { href: '/scheduler', label: 'Scheduler', icon: 'fas fa-calendar-alt' },
        { href: '/inspiration', label: 'Inspiration', icon: 'fas fa-lightbulb' },
        { href: '/collaborate', label: 'Collaborate', icon: 'fas fa-users' },
        { href: '/library', label: 'Library', icon: 'fas fa-folder-open' }
    ];
</script>

<div class="d-flex flex-column h-100" style="padding: 2rem 1.5rem;">
    <!-- Logo Section -->
    <div class="text-center mb-5">
        <div class="logo-container mb-3">
            <div class="rounded-circle d-flex align-items-center justify-content-center mx-auto" style="width: 60px; height: 60px; background: rgba(255, 255, 255, 0.15); backdrop-filter: blur(10px); border: 2px solid rgba(255, 255, 255, 0.2);">
                <i class="fas fa-rocket" style="font-size: 1.5rem; color: white;"></i>
            </div>
        </div>
        <div class="fw-bold text-white" style="font-size: 1.4rem; letter-spacing: -0.5px;">
            TrendSpotter
        </div>
        <div class="text-white" style="opacity: 0.8; font-size: 0.85rem; margin-top: 4px;">
            Social Media Analytics
        </div>
    </div>

    <!-- Navigation -->
    <nav class="nav flex-column flex-grow-1">
        {#each navItems as item}
            <a 
                class="nav-link d-flex align-items-center mb-2" 
                href={item.href}
                class:active={currentPath === item.href}
                style="
                    color: {currentPath === item.href ? '#2d3748' : 'rgba(255, 255, 255, 0.8)'};
                    background: {currentPath === item.href ? 'rgba(255, 255, 255, 0.95)' : 'transparent'};
                    border-radius: 12px;
                    padding: 14px 16px;
                    text-decoration: none;
                    font-weight: {currentPath === item.href ? '600' : '500'};
                    transition: all 0.3s ease;
                    backdrop-filter: {currentPath === item.href ? 'blur(10px)' : 'none'};
                    box-shadow: {currentPath === item.href ? '0 4px 20px rgba(0,0,0,0.1)' : 'none'};
                    border: {currentPath === item.href ? '1px solid rgba(255, 255, 255, 0.2)' : '1px solid transparent'};
                "
                on:mouseenter={e => {
                    if (currentPath !== item.href) {
                        e.target.style.background = 'rgba(255, 255, 255, 0.1)';
                        e.target.style.transform = 'translateX(4px)';
                    }
                }}
                on:mouseleave={e => {
                    if (currentPath !== item.href) {
                        e.target.style.background = 'transparent';
                        e.target.style.transform = 'translateX(0)';
                    }
                }}
            >
                <i class={item.icon} style="margin-right: 12px; width: 18px; font-size: 1rem;"></i>
                {item.label}
            </a>
        {/each}
    </nav>

    <!-- Footer Section -->
    <div class="mt-auto pt-4" style="border-top: 1px solid rgba(255, 255, 255, 0.1);">
        <div class="d-flex align-items-center text-white" style="opacity: 0.7; font-size: 0.85rem;">
            <div class="rounded-circle me-2" style="width: 8px; height: 8px; background: #48bb78;"></div>
            All systems operational
        </div>
        <div class="text-white mt-2" style="opacity: 0.5; font-size: 0.75rem;">
            Version 2.1.0
        </div>
    </div>
</div>

<style>
    .nav-link.active {
        position: relative;
    }
    
    .nav-link.active::before {
        content: '';
        position: absolute;
        left: -1.5rem;
        top: 50%;
        transform: translateY(-50%);
        width: 4px;
        height: 24px;
        background: white;
        border-radius: 2px;
        opacity: 0.8;
    }
    
    .logo-container {
        position: relative;
    }
    
    .logo-container::after {
        content: '';
        position: absolute;
        top: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 80px;
        height: 80px;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        border-radius: 50%;
        z-index: -1;
    }
</style>
