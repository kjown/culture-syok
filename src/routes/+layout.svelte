<script>
    import Header from "$lib/components/layout/Header.svelte";
    import Footer from "$lib/components/layout/Footer.svelte";
    import ToastContainer from "$lib/components/layout/ToastContainer.svelte";

    $: title = "CultureSyok";
</script>

<div class="d-flex flex-column min-vh-100" style="background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);">
    <!-- Header -->
    <div style="background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px); box-shadow: 0 4px 20px rgba(0,0,0,0.08); position: sticky; top: 0; z-index: 1020; border-bottom: 1px solid rgba(102, 126, 234, 0.1);">
        <Header title={title}/>
    </div>
    <!-- Page content -->
    <div class="flex-grow-1" style="background: transparent; padding: 0;">
        <slot />
    </div>
    <!-- Footer -->
    <Footer />
</div>

<ToastContainer />

<style>
    :global(body) {
        margin: 0;
        padding: 0;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        color: #2d3748;
    }

        :global(*) {
            box-sizing: border-box;
        }

        /* Scrollbar styling */
        .sidebar-container::-webkit-scrollbar {
            width: 6px;
        }

        .sidebar-container::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 3px;
        }

        .sidebar-container::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.3);
            border-radius: 3px;
        }

        .sidebar-container::-webkit-scrollbar-thumb:hover {
            background: rgba(255, 255, 255, 0.5);
        }

        /* Smooth transitions */
        :global(.nav-link, .btn) {
            transition: all 0.3s ease;
        }

        /* Custom scroll behavior */
        :global(html) {
            scroll-behavior: smooth;
        }
    </style>