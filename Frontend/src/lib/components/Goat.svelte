<script>
  import 'carbon-components-svelte/css/g10.css';
  import {
    TextInput,
    NumberInput,
    Button,
    Form,
    FormGroup,
  } from 'carbon-components-svelte';
  import { goto } from '$app/navigation';

  let Goats = [
    { id: 1, milk_yield: '', health: '', breed: '', lactation_stage: '', age: '' }
  ];
  let feeds = [
    { feed_type: '', feed_quantity: '', feed_percentage: '' }
  ];
  let selectedCows = [];
  let successMessage = '';
  let errorMessage = '';

  function addGoat() {
    Goats = [
      ...Goats,
      {
        id: Goats.length + 1,
        milk_yield: '',
        health: '',
        breed: '',
        lactation_stage: '',
        age: ''
      }
    ];
  }

  function addFeed() {
    feeds = [
      ...feeds,
      {
        feed_type: '',
        feed_quantity: '',
        feed_percentage: ''
      }
    ];
  }

  async function submitData() {
    successMessage = '';
    errorMessage = '';

    const input = { Goats, feeds };

    try {
      const res = await fetch('http://localhost:8080/api/optimize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(input)
      });

      if (res.ok) {
        const data = await res.json();
        selectedCows = data.selected_cows;
        successMessage = '✅ Data stored successfully in the database.';
      } else {
        errorMessage = '❌ Error storing data. Please check backend logs.';
      }
    } catch (err) {
      console.error(err);
      errorMessage = '❌ Failed to connect to backend.';
    }
  }

  function navigateTo(path) {
    goto(path);
  }
</script>

<nav class="nav-bar">
  <div class="brand">Goat Entry</div>
  <ul class="nav-links">
    <li><button on:click={() => navigateTo('/dashboard/GoatAnalytics')}>Analytics</button></li>
  </ul>
</nav>

<main>
  <h1>Milk Yield Optimization</h1>

  <Form>
    <h2>Goats</h2>
    {#each Goats as b, i}
      <FormGroup legendText="Goat Entry" class="form-group">
        <NumberInput label="Milk Yield" min="0" bind:value={b.milk_yield} />
        <TextInput labelText="Health" placeholder="Health Status" bind:value={b.health} />
        <TextInput labelText="Breed" placeholder="e.g. Alpine" bind:value={b.breed} />
        <TextInput labelText="Lactation Stage" placeholder="Stage" bind:value={b.lactation_stage} />
        <NumberInput label="Age" min="0" bind:value={b.age} />
      </FormGroup>
    {/each}
    <Button kind="ghost" on:click={addGoat}>➕ Add Goat</Button>

    <h2 style="margin-top: 2rem;">Feeds</h2>
    {#each feeds as f, i}
      <FormGroup legendText="Feed Entry" class="form-group">
        <TextInput labelText="Feed Type" placeholder="e.g. Hay" bind:value={f.feed_type} />
        <NumberInput label="Feed Quantity" min="0" bind:value={f.feed_quantity} />
        <NumberInput label="Feed Percentage" min="0" bind:value={f.feed_percentage} />
      </FormGroup>
    {/each}
    <Button kind="ghost" on:click={addFeed}>➕ Add Feed</Button>

    <div class="submit-area">
      <Button kind="primary" size="lg" on:click={submitData}>🚀 Run Optimization</Button>
    </div>

    {#if successMessage}
      <p class="success">{successMessage}</p>
    {/if}
    {#if errorMessage}
      <p class="error">{errorMessage}</p>
    {/if}
  </Form>

  {#if selectedCows.length > 0}
    <section class="results">
      <h2>Selected Cows</h2>
      <ul>
        {#each selectedCows as cow}
          <li>
            <strong>ID:</strong> {cow.id}, 
            <strong>Breed:</strong> {cow.breed}, 
            <strong>Milk Yield:</strong> {cow.milk_yield}, 
            <strong>Health:</strong> {cow.health}
          </li>
        {/each}
      </ul>
    </section>
  {/if}
</main>

<style>
  .nav-bar {
    display: flex;
    align-items: center;
    background-color: #3949ab;
    padding: 0.75rem 1.5rem;
    color: white;
    font-weight: 700;
  }

  .brand {
    flex-grow: 1;
    font-size: 1.25rem;
  }

  .nav-links {
    list-style: none;
    display: flex;
    gap: 1rem;
    margin: 0;
    padding: 0;
  }

  .nav-links button {
    background: transparent;
    border: none;
    color: white;
    cursor: pointer;
    font-size: 1rem;
    font-weight: 600;
    padding: 0.5rem 1rem;
    border-radius: 6px;
    transition: background-color 0.25s ease;
  }

  .nav-links button:hover {
    background-color: #5561f0;
  }

  main {
    max-width: 800px;
    margin: 3rem auto;
    padding: 2rem;
    background: var(--cds-layer);
    border-radius: 12px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
  }

  h1 {
    text-align: center;
    margin-bottom: 2rem;
    color: var(--cds-text-primary);
  }

  h2 {
    margin-top: 2rem;
    color: var(--cds-text-primary);
  }

  .submit-area {
    display: flex;
    justify-content: center;
    margin-top: 2rem;
  }

  .results {
    margin-top: 3rem;
    padding-top: 1rem;
    border-top: 1px solid var(--cds-border-subtle);
  }

  ul {
    list-style: none;
    padding: 0;
  }

  li {
    padding: 0.75rem 1rem;
    margin-bottom: 0.75rem;
    background: var(--cds-layer-accent);
    border-left: 4px solid var(--cds-interactive);
    border-radius: 6px;
  }

  .success {
    color: green;
    margin-top: 1rem;
    text-align: center;
  }

  .error {
    color: red;
    margin-top: 1rem;
    text-align: center;
  }
</style>
