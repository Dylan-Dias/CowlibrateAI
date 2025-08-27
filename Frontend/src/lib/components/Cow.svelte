<script>
  import 'carbon-components-svelte/css/g10.css';
  import {
    TextInput,
    NumberInput,
    Button,
    Form,
    FormGroup,
    InlineNotification,
  } from 'carbon-components-svelte';
  import { goto } from '$app/navigation';

  let bovines = [
    { id: 1, milk_yield: '', health: '', breed: '', lactation_stage: '', age: '' }
  ];
  let feeds = [
    { feed_type: '', feed_quantity: '', feed_percentage: '' }
  ];
  let selectedBovines = [];
  let success = false;
  let error = false;

  function addBovine() {
    bovines = [
      ...bovines,
      { id: bovines.length + 1, milk_yield: '', health: '', breed: '', lactation_stage: '', age: '' }
    ];
  }

  function addFeed() {
    feeds = [
      ...feeds,
      { feed_type: '', feed_quantity: '', feed_percentage: '' }
    ];
  }

  async function submitData() {
  success = false;
  error = false;

  const input = { bovines, feeds };

  try {
    const token = localStorage.getItem("token"); // grab JWT from storage
    const res = await fetch("http://localhost:8080/api/optimize", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}` // 🔑 include JWT
      },
      body: JSON.stringify(input)
    });

    if (res.ok) {
      const data = await res.json();
      selectedBovines = data.selected_bovines || [];
      success = true;

      setTimeout(() => {
        goto("/dashboard/results");
      }, 2000);
    } else {
      error = true;
    }
  } catch (err) {
    console.error(err);
    error = true;
  }
}


  function navigateTo(path) {
    goto(path);
  }
</script>

<nav class="nav-bar">
  <div class="brand">Bovine Entry</div>
  <ul class="nav-links">
    <li><button on:click={() => navigateTo('/dashboard/CowAnalytics')}>Analytics</button></li>
  </ul>
</nav>

<main>
  <h1>Milk Yield Optimization</h1>

  <Form>
    <h2>Bovines</h2>
    {#each bovines as b}
      <FormGroup legendText="Bovine Entry" class="form-group">
        <NumberInput label="Milk Yield" min="0" bind:value={b.milk_yield} />
        <TextInput labelText="Health" placeholder="Health Status" bind:value={b.health} />
        <TextInput labelText="Breed" placeholder="e.g. Holstein" bind:value={b.breed} />
        <TextInput labelText="Lactation Stage" placeholder="Stage" bind:value={b.lactation_stage} />
        <NumberInput label="Age" min="0" bind:value={b.age} />
      </FormGroup>
    {/each}
    <Button kind="ghost" on:click={addBovine}>➕ Add Bovine</Button>

    <h2 style="margin-top: 2rem;">Feeds</h2>
    {#each feeds as f}
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

    {#if success}
      <InlineNotification
        kind="success"
        title="Success"
        subtitle="Optimization successful! Redirecting to dashboard..."
        timeout="3000"
      />
    {/if}

    {#if error}
      <InlineNotification
        kind="error"
        title="Error"
        subtitle="There was a problem submitting the optimization data."
        timeout="5000"
      />
    {/if}
  </Form>

  {#if selectedBovines.length > 0}
    <section class="results">
      <h2>Selected Bovines</h2>
      <ul>
        {#each selectedBovines as b}
          <li>
            <strong>ID:</strong> {b.id},
            <strong>Breed:</strong> {b.breed},
            <strong>Milk Yield:</strong> {b.milk_yield},
            <strong>Health:</strong> {b.health}
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
</style>
