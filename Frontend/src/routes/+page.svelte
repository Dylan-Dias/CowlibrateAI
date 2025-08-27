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

  // Information Tab Data
const infoItems = [
  {
    title: "About CowlibrateAI",
    content: "CowlibrateAI is a specialized web application platform that collaborates with local and foreign farms to provide exceptional software at an affordable cost. Our goal is to assist farmers and individuals in the agriculture industry by offering this cutting edge application that streamlines dairy operations."
  },
  {
    title: "Contact Information",
    content: "Reach out to us via email, phone, or contact form for personalized consultations and support."
  }
];


  // Features Data
  const features = [
    { title: "Health & Nutrition Insights", description: "Optimize feeding and health management using AI-driven recommendations." },
    { title: "Farm Efficiency Analytics", description: "Streamline operations and boost productivity with data-backed decisions." },
    { title: "Future Work", description: "Computer Vision to help find patterns in cow birth defects or deficiencies for LLMs and AI work." }
  ];

  // FAQ Data
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

  function scrollToSection(id) {
    const el = document.getElementById(id);
    if (el) el.scrollIntoView({ behavior: 'smooth' });
  }

  function submitContactForm(event) {
    event.preventDefault();
    console.log("Name:", contactName);
    console.log("Email:", contactEmail);
    console.log("Message:", contactMessage);
    alert("Thank you! Your message has been sent.");
    contactName = '';
    contactEmail = '';
    contactMessage = '';
  }
</script>

<!-- Dark page wrapper -->
<div class="dark-page">
  <!-- Top Navigation -->
  <Header company="CowlibrateAI" class="nav-bar">
    <HeaderNav>
      <HeaderNavItem on:click={() => scrollToSection('About')}>About</HeaderNavItem>
      <HeaderNavItem on:click={() => scrollToSection('Features')}>Features</HeaderNavItem>
      <HeaderNavItem on:click={() => scrollToSection('Contact')}>Contact</HeaderNavItem>
      <HeaderNavItem on:click={() => scrollToSection('FAQ')}>FAQ</HeaderNavItem>
    </HeaderNav>
    <div class="auth-buttons">
      <Button kind="tertiary" size="sm" on:click={() => goto('/dashboard/Login')}>Login</Button>
      <Button kind="primary" size="sm" on:click={() => goto('/dashboard/registration')}>Register</Button>
    </div>
  </Header>

  <main class="container">
    <!-- About -->
    <section id="About" class="info-section">
      {#each infoItems as { title, content }}
        <div class="info-item">
          <h2>{title}</h2>
          <p>{content}</p>
        </div>
      {/each}
    </section>

    <!-- Features -->
    <section id="Features" class="features-section">
      {#each features as { title, description }}
        <div class="feature-item">
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

    <!-- Contact Form -->
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
            <Button type="submit">Send Message</Button>
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
  .dark-page {
    background: linear-gradient(180deg, #0d0d0d 0%, #1e1e1e 100%);
    color: #e0e0e0;
    min-height: 100vh;
    scroll-behavior: smooth;
    font-family: 'IBM Plex Sans', sans-serif;
    line-height: 1.6;
  }

  .auth-buttons {
    display: flex;
    gap: 0.5rem;
    margin-right: 1rem;
  }

  .container {
    max-width: 900px;
    margin: 3rem auto;
    padding: 0 1rem;
  }

  .info-section, .features-section {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    padding: 2rem 0;
  }

  .info-item h2, .feature-item h2 {
    margin-bottom: 0.5rem;
    color: #fff;
  }

  .info-item p, .feature-item p {
    color: #bbb;
    margin: 0;
  }

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
    text-align: left;
    background: none;
    border: none;
    font-size: 1.2rem;
    cursor: pointer;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem 0;
    color: #e0e0e0;
  }

  .faq-question:hover {
    color: #4fc3f7;
  }

  .faq-answer {
    margin-top: 0.5rem;
    padding-left: 1rem;
    color: #ccc;
    font-size: 1rem;
    animation: fadeIn 0.3s ease-in-out;
  }

  .arrow {
    font-size: 0.9rem;
    transition: transform 0.2s ease;
  }

  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(-5px); }
    to { opacity: 1; transform: translateY(0); }
  }

  /* Contact form spacing */
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

  .footer {
    background: #121212;
    color: #aaa;
    text-align: center;
    padding: 2rem 1rem;
    font-size: 0.9rem;
    margin-top: 3rem;
  }
</style>
