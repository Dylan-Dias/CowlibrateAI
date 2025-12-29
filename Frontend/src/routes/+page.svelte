<script>
  import { goto } from '$app/navigation';
  import {
    Header,
    HeaderNav,
    HeaderNavItem,
    Button,
    TextInput,
    TextArea,
    Form,
    FormGroup
  } from "carbon-components-svelte";

  // Information Section
  const infoItems = [
    {
      title: "CowlibrateAI",
      content:
        "CowlibrateAI is a specialized platform that partners with local and international dairy farms to provide intelligent, data-driven solutions. Using AI and analytics, it helps farmers optimize Herd Management, Feeding, and Environmental Conditions, enabling them to maximize milk production while minimizing affordable costs"
    }
  ];

  // Features Section
  const features = [
    { title: "Health & Nutrition Insights", description: "Optimize feeding and health management using AI-driven recommendations." },
    { title: "Farm Efficiency Analytics", description: "Streamline operations and boost productivity with data-backed decisions." },
    { title: "Future Work", description: "Computer Vision to help find patterns in cow birth defects or deficiencies for LLMs and AI work." }
  ];

  // FAQ Section
  let faqs = [
    { question: "What is CowlibrateAI?", answer: "It’s an AI system to maximize dairy production.", open: false },
    { question: "Who can use it?", answer: "Farmers looking to improve efficiency and productivity.", open: false },
    { question: "Is it affordable?", answer: "Yes, designed for farmers who cannot afford dairy parlors.", open: false }
  ];

  function toggleFAQ(index) {
    faqs = faqs.map((faq, i) => ({
      ...faq,
      open: i === index ? !faq.open : false
    }));
  }

  // Contact form state
  let contactName = '';
  let contactEmail = '';
  let contactMessage = '';
  let sending = false; // Loading state

  async function submitContactForm(event) {
    event.preventDefault();
    sending = true;

    try {
      const res = await fetch("https://cowlibrate.onrender.com/api/contact", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: contactName,
          email: contactEmail,
          message: contactMessage
        })
      });

      const data = await res.json();
      if (res.ok) {
        alert("Thank you! Your message has been sent.");
        contactName = '';
        contactEmail = '';
        contactMessage = '';
      } else {
        alert("Error sending message: " + data.error);
      }
    } catch (err) {
      console.error(err);
      alert("An unexpected error occurred.");
    } finally {
      sending = false;
    }
  }

  function scrollToSection(id) {
    const el = document.getElementById(id);
    if (el) el.scrollIntoView({ behavior: 'smooth' });
  }
</script>

<!-- Dark Page Layout -->
<div class="dark-page">
  <!-- Header Navigation -->
  <Header company="CowlibrateAI" class="nav-bar">
    <HeaderNav>
      <HeaderNavItem on:click={() => scrollToSection('About')}>About</HeaderNavItem>
      <HeaderNavItem on:click={() => scrollToSection('Features')}>Features</HeaderNavItem>
      <HeaderNavItem on:click={() => scrollToSection('Contact')}>Contact</HeaderNavItem>
      <HeaderNavItem on:click={() => scrollToSection('FAQ')}>FAQ</HeaderNavItem>
    </HeaderNav>
    <div class="auth-buttons">
      <Button kind="tertiary" size="sm" on:click={() => goto('/login')}>Login</Button>
      <Button kind="primary" size="sm" on:click={() => goto('/registration')}>Register</Button>
    </div>
  </Header>

  <main class="container">
    <!-- About Section -->
    <section id="About" class="info-section">
      {#each infoItems as { title, content }}
        <div class="info-item">
          <h2>{title}</h2>
          <p>{content}</p>
        </div>
      {/each}
    </section>

    <!-- Features Section (Fades In) -->
    <section id="Features" class="features-section">
      {#each features as { title, description }, i}
        <div class="feature-item" style="animation-delay: {i * 0.4}s">
          <h2>{title}</h2>
          <p>{description}</p>
        </div>
      {/each}
    </section>

    <!-- FAQ Section -->
    <section id="FAQ" class="faq-section">
      <h1 class="faq-title">Frequently Asked Questions</h1>
      {#each faqs as faq, i}
        <div class="faq-item">
          <button class="faq-question" on:click={() => toggleFAQ(i)}>
            {faq.question}
            <span class="arrow">{faq.open ? "▲" : "▼"}</span>
          </button>
          {#if faq.open}
            <div class="faq-answer">
              <p>{faq.answer}</p>
            </div>
          {/if}
        </div>
      {/each}
    </section>

    <!-- Contact Section -->
    <section id="Contact" class="contact-section">
      <Form on:submit={submitContactForm} class="contact-form">
        <FormGroup legendText="Contact Us">
          <div class="form-item">
            <TextInput bind:value={contactName} id="name" labelText="Name" placeholder="Your full name" required />
          </div>
          <div class="form-item">
            <TextInput bind:value={contactEmail} id="email" type="email" labelText="Email" placeholder="Your email address" required />
          </div>
          <div class="form-item">
            <TextArea bind:value={contactMessage} id="message" labelText="Message" placeholder="Write your message here..." rows="4" required />
          </div>
          <div class="form-button">
            <Button type="submit" disabled={sending}>
              {#if sending}Sending...{/if}
              {#if !sending}Send Message{/if}
            </Button>
          </div>
        </FormGroup>
      </Form>
    </section>
  </main>

  <footer class="footer">
    © {new Date().getFullYear()} CowlibrateAI. All rights reserved.
  </footer>
</div>

<style>
  /* ========== Base Layout ========== */
  .dark-page {
    background: linear-gradient(180deg, #000000 0%, #1e1e1e 100%);
    color: #e0e0e0;
    min-height: 100vh;
    font-family: 'IBM Plex Sans', sans-serif;
    scroll-behavior: smooth;
  }

  .container {
    max-width: 900px;
    margin: 3rem auto;
    padding: 0 1rem;
  }

  .auth-buttons {
    display: flex;
    gap: 0.9rem;
    margin-right: 1rem;
  }

  /* ========== Info Section ========== */
  .info-section {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    padding: 2rem 0;
  }

 .info-item:first-child h2 {
  font-size: clamp(2rem, 8vw, 8rem);
  font-weight: 1000;
  color: #fff;
}


  .info-item h2 {
    margin-bottom: 0.5rem;
    color: #fff;
  }

  .info-item p {
    color: #bbb;
  }

  /* ========== Feature Section (Fade In) ========== */
  .features-section {
    display: flex;
    text-align: center;
    flex-direction: column;
  }

  .feature-item {
    opacity: 0;
    transform: translateY(40px);
    padding: 1.8rem;
    border-radius: 10px;
    transition: transform 0.3s ease;
    animation: fadeInUp 0.9s ease forwards;
  }

  .feature-item:hover {
    transform: translateY(-5px);
  }

  .feature-item h2 {
    color: #fff;
    font-size: 1.7rem;
    margin-bottom: 0.5rem;
  }

  .feature-item p {
    color: #bbb;
    font-size: 1.05rem;
  }

  @keyframes fadeInUp {
    from { opacity: 0; transform: translateY(40px); }
    to { opacity: 1; transform: translateY(0); }
  }

  /* ========== FAQ Section ========== */
  .faq-section {
    max-width: 800px;
    margin: 2rem auto;
    padding: 1rem;
  }

  .faq-title {
    font-size: 2rem;
    margin-bottom: 1.5rem;
    text-align: center;
  }

  .faq-item {
    border-bottom: 1px solid #444;
    padding: 1rem 0;
  }

  .faq-question {
    width: 100%;
    background: none;
    border: none;
    font-size: 1.2rem;
    color: #e0e0e0;
    cursor: pointer;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .faq-question:hover {
    color: #4fc3f7;
  }

  .faq-answer {
    margin-top: 0.5rem;
    padding-left: 1rem;
    color: #ccc;
    animation: fadeIn 0.3s ease-in-out;
  }

  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(-5px); }
    to { opacity: 1; transform: translateY(0); }
  }

  /* ========== Contact Section ========== */
  .contact-section {
    margin-top: 3rem;
    padding: 2rem 0;
  }

  .form-item {
    margin-bottom: 1.5rem;
  }

  .form-button {
    margin-top: 1.5rem;
    display: flex;
    justify-content: flex-end;
  }

  /* ========== Footer ========== */
  .footer {
    background: #121212;
    color: #aaa;
    text-align: center;
    padding: 2rem 1rem;
    font-size: 0.9rem;
    margin-top: 3rem;
  }
</style>
