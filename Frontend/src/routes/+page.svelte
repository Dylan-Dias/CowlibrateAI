<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import Icon from '@iconify/svelte';

  let heroRef, featuresRef, testimonialsRef, pricingRef, investorsRef, aboutRef;

  const features = [
    {
      title: "AI-Powered Herd Tracking",
      description: "Monitor your cows in real time with smart sensors and predictive analytics.",
     
    },
    {
      title: "Health & Nutrition Insights",
      description: "Optimize feeding and health management using AI-driven recommendations.",
      
    },
    {
      title: "Farm Efficiency Analytics",
      description: "Streamline operations and boost productivity with data-backed decisions.",
      
    },
  ];




  function scrollToSection(ref) {
    ref.scrollIntoView({ behavior: 'smooth' });
  }

  let displayedText = "Smart Dairy Farming Powered by AI";
</script>

<nav class="nav-bar">
  <div class="brand">CowlibrateAI</div>
  <ul class="nav-links">
    <li><button on:click={() => scrollToSection(heroRef)}>Home</button></li>
    <li><button on:click={() => scrollToSection(featuresRef)}>Features</button></li>
    <li><button on:click={() => scrollToSection(testimonialsRef)}>Testimonials</button></li>
    <li><button on:click={() => scrollToSection(pricingRef)}>Pricing</button></li>
    <li><button on:click={() => scrollToSection(investorsRef)}>Investors</button></li>
    <li><button on:click={() => scrollToSection(aboutRef)}>About</button></li>
    <li><button class="nav-cta-btn" on:click={() => goto('/dashboard/registration')}>Registration</button></li>
  </ul>
</nav>

<main class="container">
  <section bind:this={heroRef} class="hero">
    <div class="hero-text">
      <h1>{displayedText}</h1>
      <p>Revolutionize your dairy operations with real-time monitoring and intelligent insights.</p>
      <button class="cta-btn" on:click={() => goto('/dashboard/registration')}>
        Join the Moovement
        <Icon icon="mdi:arrow-right" style="margin-left: 0.6rem; width: 1.25rem; height: 1.25rem;" />
      </button>
    </div>
  </section>

  <section bind:this={featuresRef} class="features">
    {#each features as { title, description, icon }}
      <article class="feature-card">
        <Icon icon={icon} class="feature-icon" />
        <h3>{title}</h3>
        <p>{description}</p>
      </article>
    {/each}
  </section>





  <section bind:this={investorsRef} class="investors">
    <h2>Backed By</h2>
    <div class="investor-logos">
      <img src="" alt="VC Firm 1" />
      <img src="" alt="VC Firm 2" />
    </div>
  </section>

  <section bind:this={aboutRef} class="about">
    <h2>About CowlibrateAI</h2>
    <p>Founded in 2024, we are dedicated to making dairy farming smarter and more sustainable through AI-powered solutions.</p>
    <p>Our mission is to empower farmers with tools that optimize herd health, improve productivity, and reduce environmental impact.</p>
  </section>
</main>

<footer class="footer">
  © {new Date().getFullYear()} CowlibrateAI. All rights reserved.
</footer>

<style>
  :global(body) {
    margin: 0;
    font-family: 'Inter', sans-serif;
    background: white;
    color: #111;
    scroll-behavior: smooth;
  }
  .nav-bar {
    position: fixed;
    top: 0;
    width: 100%;
    background: #000;
    color: white;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 3rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.7);
    z-index: 999;
  }
  .brand {
    font-weight: 700;
    font-size: 1.5rem;
    letter-spacing: 1.2px;
  }
  .nav-links {
    list-style: none;
    display: flex;
    gap: 1rem;
    margin: 0;
    padding: 0;
  }
  .nav-links button, .nav-cta-btn {
    background: transparent;
    border: none;
    color: white;
    cursor: pointer;
    font-size: 1rem;
    font-weight: 500;
    padding: 0.5rem 1rem;
    border-radius: 6px;
    transition: background-color 0.25s ease;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .nav-links button:hover, .nav-cta-btn:hover {
    background-color: #444;
  }
  .container {
    max-width: 1100px;
    margin: 6rem auto 3rem;
    padding: 0 2rem;
  }
  .hero {
    text-align: center;
    padding: 6rem 0 4rem;
  }
  .hero h1 {
    font-size: 3.2rem;
    font-weight: 800;
    letter-spacing: 0.06em;
  }
  .hero p {
    font-size: 1.3rem;
    margin-top: 1rem;
    color: #222;
  }
  .cta-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 2rem auto 0;
    padding: 0.75rem 1.5rem;
    background: black;
    color: white;
    border: none;
    border-radius: 6px;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.3s ease;
  }
  .cta-btn:hover {
    background: #222;
  }

  .footer {
    background: #000;
    color: white;
    text-align: center;
    padding: 2rem 1rem;
    font-size: 0.9rem;
  }
</style>
