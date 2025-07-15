<script>
  import 'carbon-components-svelte/css/g10.css';
  import {
    Form,
    FormGroup,
    TextInput,
    Button,
    InlineNotification
  } from 'carbon-components-svelte';

  let email = '';
  let message = '';
  let error = '';

  async function handleReset(event) {
    event.preventDefault();
    error = '';
    message = '';

    if (!email) {
      error = 'Please enter your email address.';
      return;
    }

    try {
      const res = await fetch('/api/reset-password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email })
      });

      const data = await res.json();

      if (res.ok) {
        message = 'If this email is registered, you will receive password reset instructions.';
        email = '';
      } else {
        error = data.message || 'Failed to send reset instructions.';
      }
    } catch (err) {
      error = 'Network error. Please try again later.';
    }
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
    <FormGroup legendText="Enter your email to receive reset link">
      <TextInput
        labelText="Email Address"
        placeholder="you@example.com"
        type="email"
        bind:value={email}
        required
      />

      <Button type="submit" kind="primary">Send Reset Link</Button>
    </FormGroup>
  </Form>
</main>

<style>
  main {
    max-width: 480px;
    margin: 3rem auto;
    padding: 2rem;
    background: var(--cds-layer);
    border-radius: 12px;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.06);
    font-family: 'Segoe UI', Tahoma, sans-serif;
  }

  h2 {
    text-align: center;
    color: var(--cds-text-primary);
    margin-bottom: 2rem;
  }

  :global(.bx--form-group) {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }

  :global(.bx--btn) {
    margin-top: 1rem;
  }

  :global(.bx--inline-notification) {
    margin-bottom: 1.5rem;
  }
</style>
