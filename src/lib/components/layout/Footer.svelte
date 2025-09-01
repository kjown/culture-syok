<script>
    import { onMount } from 'svelte';
    
    let currentYear = new Date().getFullYear();
    
    const socialLinks = [
        { name: 'Twitter', icon: 'fab fa-x-twitter', url: 'https://x.com/DebuggingA83409' },
        { name: 'Instagram', icon: 'fab fa-instagram', url: 'https://www.instagram.com/ayamdebugging/' },
    ];
    
    const quickLinks = [
        { name: 'Dashboard', href: '/' },
        { name: 'Scheduler', href: '/scheduler' },
        { name: 'Inspiration', href: '/inspiration' },
        { name: 'Collaborate', href: '/collaborate' },
        { name: 'Library', href: '/library' }
    ];
    
    const supportLinks = [
        { name: 'Help Center', href: '/help' },
        { name: 'Documentation', href: '/docs' },
        { name: 'API Reference', href: '/api-docs' },
        { name: 'Contact Support', href: '/contact' }
    ];
    

</script>

<footer class="footer mt-5">
    <div class="footer-container">
        <!-- Main Footer Content -->
        <div class="footer-content">
            <!-- Brand Section -->
            <div class="footer-brand">
                <div class="brand-logo">
                    <div class="brand-icon">
                        <i class="fas fa-rocket"></i>
                    </div>
                    <h4 class="brand-name">CultureSyok</h4>
                </div>
                <p class="brand-description">
                    Empowering content creators with advanced social media analytics and AI-powered insights 
                    to grow their digital presence across all platforms.
                </p>
                <div class="social-links">
                    {#each socialLinks as social}
                        <a 
                            href={social.url} 
                            class="social-link"
                            aria-label={social.name}
                            target="_blank"
                            rel="noopener noreferrer"
                        >
                            <i class={social.icon}></i>
                        </a>
                    {/each}
                </div>
            </div>
            
            <!-- Quick Links -->
            <div class="footer-section">
                <h5 class="section-title">
                    <i class="fas fa-link me-2"></i>
                    Quick Links
                </h5>
                <ul class="footer-links">
                    {#each quickLinks as link}
                        <li>
                            <a href={link.href} class="footer-link">
                                {link.name}
                            </a>
                        </li>
                    {/each}
                </ul>
            </div>
            
            <!-- Support -->
            <div class="footer-section">
                <h5 class="section-title">
                    <i class="fas fa-headset me-2"></i>
                    Support
                </h5>
                <ul class="footer-links">
                    {#each supportLinks as link}
                        <li>
                            <a href={link.href} class="footer-link">
                                {link.name}
                            </a>
                        </li>
                    {/each}
                </ul>
            </div>
            
            <!-- Newsletter Signup -->
            <div class="footer-section newsletter-section">
                <h5 class="section-title">
                    <i class="fas fa-envelope me-2"></i>
                    Stay Updated
                </h5>
                <p class="newsletter-description">
                    Get the latest features, tips, and insights delivered to your inbox.
                </p>
                <form class="newsletter-form" on:submit|preventDefault>
                    <div class="input-group">
                        <input 
                            type="email" 
                            class="newsletter-input"
                            placeholder="Enter your email"
                            required
                        />
                        <button type="submit" class="newsletter-btn">
                            <i class="fas fa-paper-plane"></i>
                        </button>
                    </div>
                </form>
            </div>
        </div>
        
        <!-- Footer Bottom -->
        <div class="footer-bottom">
            <div class="footer-bottom-content">
                <div class="copyright">
                    <p class="copyright-text">
                        © {currentYear} CultureSyok by Ayam Debugging Team. All rights reserved.
                    </p>
                </div>
            </div>
        </div>
    </div>
</footer>

<style>
    .footer {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-top: auto;
        position: relative;
        overflow: hidden;
    }
    
    .footer::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="20" cy="20" r="1" fill="rgba(255,255,255,0.03)"/><circle cx="80" cy="40" r="1" fill="rgba(255,255,255,0.03)"/><circle cx="40" cy="80" r="1" fill="rgba(255,255,255,0.03)"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
        opacity: 0.5;
        pointer-events: none;
    }
    
    .footer-container {
        max-width: 1400px;
        margin: 0 auto;
        padding: 0 1rem;
        position: relative;
        z-index: 1;
    }
    
    .footer-content {
        display: grid;
        grid-template-columns: 2fr 1fr 1fr 1.5fr;
        gap: 3rem;
        padding: 4rem 0 2rem;
    }
    
    .footer-brand {
        max-width: 400px;
    }
    
    .brand-logo {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    
    .brand-icon {
        width: 50px;
        height: 50px;
        background: rgba(255, 255, 255, 0.15);
        border-radius: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        flex-shrink: 0;
    }
    
    .brand-name {
        color: white;
        font-weight: 700;
        font-size: 1.5rem;
        margin: 0;
        letter-spacing: -0.5px;
        line-height: 1.2;
        display: flex;
        align-items: center;
    }
    
    .brand-description {
        color: rgba(255, 255, 255, 0.8);
        line-height: 1.6;
        margin-bottom: 2rem;
        font-size: 0.95rem;
    }
    
    .social-links {
        display: flex;
        gap: 1rem;
    }
    
    .social-link {
        width: 40px;
        height: 40px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        text-decoration: none;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .social-link:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: translateY(-2px);
        color: white;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .footer-section {
        display: flex;
        flex-direction: column;
    }
    
    .section-title {
        color: white;
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
    }
    
    .section-title i {
        color: rgba(255, 255, 255, 0.8);
    }
    
    .footer-links {
        list-style: none;
        padding: 0;
        margin: 0;
    }
    
    .footer-links li {
        margin-bottom: 0.75rem;
    }
    
    .footer-link {
        color: rgba(255, 255, 255, 0.8);
        text-decoration: none;
        font-size: 0.9rem;
        transition: all 0.3s ease;
        display: inline-block;
        position: relative;
    }
    
    .footer-link:hover {
        color: white;
        transform: translateX(5px);
    }
    
    .footer-link::before {
        content: '';
        position: absolute;
        left: -15px;
        top: 50%;
        transform: translateY(-50%);
        width: 0;
        height: 2px;
        background: white;
        transition: width 0.3s ease;
    }
    
    .footer-link:hover::before {
        width: 8px;
    }
    
    .newsletter-section {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 2rem;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .newsletter-description {
        color: rgba(255, 255, 255, 0.8);
        font-size: 0.9rem;
        line-height: 1.5;
        margin-bottom: 1.5rem;
    }
    
    .newsletter-form {
        margin-top: 1rem;
    }
    
    .input-group {
        display: flex;
        gap: 0.5rem;
    }
    
    .newsletter-input {
        flex: 1;
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 12px;
        padding: 0.875rem 1rem;
        color: white;
        font-size: 0.9rem;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .newsletter-input::placeholder {
        color: rgba(255, 255, 255, 0.6);
    }
    
    .newsletter-input:focus {
        outline: none;
        border-color: rgba(255, 255, 255, 0.4);
        background: rgba(255, 255, 255, 0.15);
        box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.1);
    }
    
    .newsletter-btn {
        background: white;
        color: #667eea;
        border: none;
        border-radius: 12px;
        width: 50px;
        height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 1rem;
    }
    
    .newsletter-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(255, 255, 255, 0.2);
        background: rgba(255, 255, 255, 0.95);
    }
    
    .footer-bottom {
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        padding: 2rem 0;
    }
    
    .footer-bottom-content {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 2rem;
    }
    
    .copyright-text {
        color: rgba(255, 255, 255, 0.8);
        font-size: 0.9rem;
        margin: 0;
        text-align: center;
    }
    
    /* Responsive Design */
    @media (max-width: 1200px) {
        .footer-content {
            grid-template-columns: 1fr 1fr 1fr;
            gap: 2rem;
        }
        
        .newsletter-section {
            grid-column: 1 / -1;
            margin-top: 2rem;
        }
    }
    
    @media (max-width: 768px) {
        .footer-content {
            grid-template-columns: 1fr;
            gap: 2rem;
            padding: 3rem 0 2rem;
        }
        
        .newsletter-section {
            grid-column: 1;
            margin-top: 1rem;
            padding: 1.5rem;
        }
        
        .footer-bottom-content {
            flex-direction: column;
            text-align: center;
            gap: 1rem;
        }
        
        .brand-logo {
            justify-content: center;
            text-align: center;
        }
        
        .brand-description {
            text-align: center;
        }
        
        .social-links {
            justify-content: center;
        }
        
        .footer-brand {
            text-align: center;
            max-width: none;
        }
    }
    
    @media (max-width: 480px) {
        .footer-container {
            padding: 0 0.5rem;
        }
        
        .footer-content {
            padding: 2rem 0 1.5rem;
        }
        
        .newsletter-section {
            padding: 1rem;
        }
        
        .input-group {
            flex-direction: column;
        }
        
        .newsletter-btn {
            width: 100%;
            height: 45px;
        }
    }
</style>