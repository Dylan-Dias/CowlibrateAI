<script>
  import 'carbon-components-svelte/css/g10.css';
  import {
    Form,
    FormGroup,
    TextInput,
    PasswordInput,
    Button,
    InlineNotification
  } from 'carbon-components-svelte';

  import { goto } from '$app/navigation';

  let username = '';
  let password = '';
  let loginError = '';
  let loginSuccess = false;

  async function handleLoginSubmit(event) {
    event.preventDefault();
    await login();
  }

  async function login() {
    loginError = '';
    loginSuccess = false;

    try {
      const res = await fetch('http://localhost:8080/api/login', {  // adjust origin if needed
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      });

      // Try to parse JSON response safely
      let data;
      try {
        data = await res.json();
      } catch {
        loginError = 'Unexpected server response.';
        return;
      }

      if (res.ok && data.token) {
        localStorage.setItem('token', data.token);
        loginSuccess = true;
        username = '';
        password = '';

        // Redirect based on role (make sure backend sends role)
        if (data.role === 'goat') {
          goto('/dashboard/goat');
        } else if (data.role === 'cow') {
          goto('/dashboard/cow');
        } else {
          goto('/');  // fallback
        }
      } else {
        loginError = data.message || 'Login failed. Please check your credentials.';
      }
    } catch (err) {
      loginError = 'Network error or server not reachable.';
    }
  }
</script>

<main>
  <h2>Login</h2>

  {#if loginSuccess}
    <InlineNotification title="Login Successful" subtitle="You are now logged in." kind="success" />
  {/if}

  {#if loginError}
    <InlineNotification title="Login Failed" subtitle={loginError} kind="error" />
  {/if}

  <Form on:submit={handleLoginSubmit}>
    <FormGroup legendText="Access your account">
      <TextInput
        labelText="Username"
        placeholder="Enter your username"
        bind:value={username}
        required
      />

      <PasswordInput
        labelText="Password"
        placeholder="Your password"
        bind:value={password}
        required
      />

      <Button type="submit" kind="primary">Login</Button>
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
