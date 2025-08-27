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

  async function handleLogin(event) {
    event.preventDefault(); // stop page refresh
    loginError = '';
    loginSuccess = false;

    try {
      const res = await fetch("http://localhost:8080/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
      });

      const data = await res.json();

      if (!res.ok) {
        loginError = data.message || "Login failed";
        return;
      }

      localStorage.setItem("token", data.token);
      loginSuccess = true;

      if (data.success) {
        // ✅ Route based on role
        if (data.role === "goat") {
          goto("/dashboard/GoatAnalytics");
        } else if (data.role === "cow") {
          goto("/dashboard/CowAnalytics");
        } else {
          goto("/dashboard"); // fallback
        }
      } else {
        loginError = data.message || "Invalid login";
      }
    } catch (err) {
      loginError = "Something went wrong";
      console.error(err);
    }
  }

  function handleForgotPassword() {
    goto('/dashboard/ResetPassword');
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

  <Form on:submit={handleLogin}>
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

      <div class="button-group">
        <Button type="submit" kind="primary" size="sm">Login</Button>
        <Button kind="tertiary" type="button" size="sm" on:click={handleForgotPassword}>
          Forgot Password?
        </Button>
      </div>
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

  :global(.bx--inline-notification) {
    margin-bottom: 1.5rem;
  }

  /* Fix PasswordInput eyeball alignment */
  :global(.bx--password-input .bx--text-input__field-wrapper) {
    display: flex;
    align-items: center;
  }

  :global(.bx--password-input .bx--text-input) {
    flex: 1;
  }

  :global(.bx--password-input__visibility__toggle) {
    margin-left: 0.5rem;
  }

  /* Buttons side by side + smaller */
  .button-group {
    display: flex;
    justify-content: flex-end;
    gap: 0.5rem;
    margin-top: 1rem;
  }

  :global(.bx--btn) {
    min-width: auto;
    padding: 0.5rem 1rem;
    font-size: 0.85rem;
  }
</style>
