<svelte:head>
  <!-- Primary SEO -->
  <title>CowlibrateAI | AI-Powered Dairy Farm Optimization</title>
  <meta
    name="description"
    content="CowlibrateAI is an AI-powered platform helping dairy farms optimize herd health, nutrition, and milk production using data-driven analytics."
  />
  <link rel="canonical" href="https://cowlibrate.ai/" />

  <!-- Favicon -->
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon.png" />
  <link rel="icon" type="image/png" sizes="16x16" href="/favicon.png" />
  <link rel="apple-touch-icon" href="/favicon.png" />

  <!-- Open Graph -->
  <meta property="og:title" content="CowlibrateAI | AI-Powered Dairy Farm Optimization" />
  <meta
    property="og:description"
    content="AI-driven analytics for dairy herd health, nutrition, and milk production optimization."
  />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="https://cowlibrate.ai/" />

  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="CowlibrateAI" />
  <meta
    name="twitter:description"
    content="Affordable AI tools for dairy farm efficiency and milk production optimization."
  />

  <!-- FAQ Schema -->
  <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "What is CowlibrateAI?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "CowlibrateAI is an AI-powered platform designed to help dairy farms improve herd health, nutrition, and milk production."
          }
        },
        {
          "@type": "Question",
          "name": "Who can use CowlibrateAI?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Dairy farmers and agricultural professionals looking to improve efficiency and productivity."
          }
        },
        {
          "@type": "Question",
          "name": "Is CowlibrateAI affordable?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Yes. It is designed for farms that cannot afford expensive dairy parlor systems."
          }
        }
      ]
    }
  </script>
</svelte:head>

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
  } from 'carbon-components-svelte';

  const features = [
    {
      title: 'Health & Nutrition Insights',
      description:
        'Optimize feeding strategies and herd health using AI-driven recommendations.'
    },
    {
      title: 'Farm Efficiency Analytics',
      description:
        'Make data-backed decisions to streamline operations and increase productivity.'
    },
    {
      title: 'Future Work',
      description:
        'Computer vision models to detect cow health deficiencies and birth defects.'
    }
  ];

  let faqs = [
    {
      question: 'What is CowlibrateAI?',
      answer:
        'CowlibrateAI is an AI-powered platform designed to help dairy farms optimize production and herd health.',
      open: false
    },
    {
      question: 'Who can use it?',
      answer:
        'Dairy farmers and agricultural professionals seeking better operational efficiency.',
      open: false
    },
    {
      question: 'Is it affordable?',
      answer:
        'Yes. It is designed specifically for farms that cannot afford expensive dairy parlors.',
      open: false
    }
  ];

  function toggleFAQ(index) {
    faqs = faqs.map((faq, i) => ({
      ...faq,
      open: i === index ? !faq.open : false
    }));
  }

  let contactName = '';
  let contactEmail = '';
  let contactMessage = '';
  let sending = false;

  async function submitContactForm(event) {
    event.preventDefault();
    sending = true;

    try {
      const res = await fetch('https://cowlibrate.onrender.com/api/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: contactName,
          email: contactEmail,
          message: contactMessage
        })
      });

      if (res.ok) {
        alert('Thank you! Your message has been sent.');
        contactName = '';
        contactEmail = '';
        contactMessage = '';
      } else {
        alert('Error sending message.');
      }
    } catch (err) {
      console.error(err);
      alert('Unexpected error.');
    } finally {
      sending = false;
    }
  }

  function scrollToSection(id) {
    document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' });
  }
</script>

<div class="dark-page">
  <Header company="CowlibrateAI">
    <HeaderNav>
      <HeaderNavItem on:click={() => scrollToSection('about')}>About</HeaderNavItem>
      <HeaderNavItem on:click={() => scrollToSection('features')}>Features</HeaderNavItem>
      <HeaderNavItem on:click={() => scrollToSection('contact')}>Contact</HeaderNavItem>
      <HeaderNavItem on:click={() => scrollToSection('faq')}>FAQ</HeaderNavItem>
    </HeaderNav>
    <div class="auth-buttons">
      <Button kind="tertiary" size="sm" on:click={() => goto('/login')}>Login</Button>
      <Button kind="primary" size="sm" on:click={() => goto('/registration')}>
        Register
      </Button>
    </div>
  </Header>

  <main class="container">
    <!-- ABOUT -->
    <section id="about" class="info-section">
      <h1 class="main-title">CowlibrateAI</h1>
      <p class="subtitle">
        AI-powered dairy farm management to optimize herd health, nutrition,
        and milk production using advanced analytics.
      </p>
    </section>

    <!-- FEATURES -->
    <section id="features" class="features-section">
      {#each features as feature, i}
        <article class="feature-item" style="animation-delay: {i * 0.3}s">
          <h2>{feature.title}</h2>
          <p>{feature.description}</p>
        </article>
      {/each}
    </section>

    <!-- FAQ -->
    <section
      id="faq"
      class="faq-section"
      itemscope
      itemtype="https://schema.org/FAQPage"
    >
      <h2 class="faq-title">Frequently Asked Questions</h2>

      {#each faqs as faq, i}
        <div class="faq-item">
          <button class="faq-question" on:click={() => toggleFAQ(i)}>
            {faq.question}
            <span>{faq.open ? '▲' : '▼'}</span>
          </button>

          {#if faq.open}
            <div class="faq-answer">
              <p>{faq.answer}</p>
            </div>
          {/if}
        </div>
      {/each}
    </section>

    <!-- CONTACT -->
    <section id="contact" class="contact-section">
      <Form on:submit={submitContactForm}>
        <FormGroup legendText="Contact Us">
          <TextInput
            bind:value={contactName}
            id="name"
            labelText="Name"
            required
          />
          <TextInput
            bind:value={contactEmail}
            id="email"
            type="email"
            labelText="Email"
            required
          />
          <TextArea
            bind:value={contactMessage}
            id="message"
            labelText="Message"
            rows="4"
            required
          />
          <Button type="submit" disabled={sending}>
            {sending ? 'Sending...' : 'Send Message'}
          </Button>
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
    background: linear-gradient(180deg, #000, #1e1e1e);
    color: #e0e0e0;
    min-height: 100vh;
    font-family: 'IBM Plex Sans', sans-serif;
  }

  .container {
    max-width: 900px;
    margin: 3rem auto;
    padding: 0 1rem;
  }

  .main-title {
    font-size: clamp(2.5rem, 8vw, 6rem);
    font-weight: 900;
    color: #fff;
  }

  .subtitle {
    color: #bbb;
    max-width: 700px;
  }

  .features-section {
    text-align: center;
  }

  .feature-item {
    opacity: 0;
    animation: fadeInUp 0.8s forwards;
    padding: 2rem;
  }

  @keyframes fadeInUp {
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  .faq-question {
    width: 100%;
    background: none;
    border: none;
    color: #fff;
    text-align: left;
    cursor: pointer;
  }

  .footer {
    text-align: center;
    padding: 2rem;
    color: #aaa;
  }

  @media (prefers-reduced-motion: reduce) {
    .feature-item {
      animation: none;
    }
  }
</style>
