<script>
  import 'carbon-components-svelte/css/g10.css';
  import { Form, FormGroup, TextInput, Button, InlineNotification } from 'carbon-components-svelte';
  import { goto } from '$app/navigation';

  let email = '';
  let message = '';
  let error = '';
  let loading = false;

  async function handleReset(event) {
    event.preventDefault();
    error = '';
    message = '';

    if (!email.trim()) {
      error = 'Please enter your email address.';
      return;
    }

    loading = true;

    try {
      const res = await fetch('http://127.0.0.1:8080/forgot-password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email })
      });

      const data = await res.json();

      if (res.ok) {
        message = 'If this email is registered, you will receive password reset instructions.';
        email = '';
      } else {
        error = data.error || 'Failed to send reset instructions.';
      }
    } catch (err) {
      console.error(err);
      error = 'Network error. Please try again later.';
    } finally {
      loading = false;
    }
  }

  function backToLogin() {
    goto('/login');
  }
</script>

<main>
  <h2>Reset Your Password</h2>

  {#if message}
    <InlineNotification title="Success" subtitle={message} kind="success" />
  {/if}

  {#if error}
    <InlineNotification title="Error" subtitle={error} kind="error" />
  {/if}

  <Form on:submit={handleReset}>
    <FormGroup legendText="Enter your email to receive a reset link">
      <TextInput
        labelText="Email Address"
        placeholder="you@example.com"
        type="email"
        bind:value={email}
        required
        disabled={loading}
      />

      <div class="button-group">
        <Button type="submit" kind="primary" size="small" disabled={loading}>
          {#if loading}Sending...{:else}Send Reset Link{/if}
        </Button>
        <Button type="button" kind="tertiary" size="small" on:click={backToLogin} disabled={loading}>
          Back to Login
        </Button>
      </div>
    </FormGroup>
  </Form>
</main>
<style>
  main {
    max-width: 600px;
    margin: 100px auto;
    padding: 2rem;
    background: var(--cds-layer);
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
  }

  .button-group {
    margin-top: 1rem;
    display: flex;
    justify-content: flex-end;
    gap: 0.50rem; 
  }

  
</style>