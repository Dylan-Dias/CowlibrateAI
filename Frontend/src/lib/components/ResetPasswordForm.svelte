<script>
  import {
    Form,
    FormGroup,
    PasswordInput,
    Button,
    InlineNotification
  } from 'carbon-components-svelte';

  export let token;
  let newPassword = '';
  let confirmPassword = '';
  let error = '';
  let success = false;
  let loading = false;

  async function handleSubmit(event) {
    event.preventDefault();
    error = '';
    success = false;

    if (newPassword !== confirmPassword) {
      error = 'Passwords do not match';
      return;
    }

    loading = true;
    try {
     const res = await fetch(`https://cowlibrate.onrender.com/reset-password${token}`, {
  method: "POST",
  headers: {
    "Content-Type": "application/json; charset=utf-8",
  },
  body: JSON.stringify({
    password: newPassword,
    confirm_password: confirmPassword
  })
});


      const data = await res.json();
        console.log(data);
      if (res.ok) {
        success = true;
        newPassword = '';
        confirmPassword = '';
      } else {
        error = data.error || 'Failed to reset password.';
      }
    } catch (err) {
      error = 'Network error. Please try again.';
    } finally {
      loading = false;
    }
  }
</script>

<main>
  <h2>Reset Your Password</h2>

  {#if success}
    <InlineNotification title="Success" subtitle="Your password has been updated." kind="success" />
  {/if}

  {#if error}
    <InlineNotification title="Error" subtitle={error} kind="error" />
  {/if}

  <Form on:submit={handleSubmit}>
    <FormGroup legendText="Enter your new password">
      <PasswordInput
        labelText="New Password"
        bind:value={newPassword}
        required
        disabled={loading}
      />

      <PasswordInput
        labelText="Confirm Password"
        bind:value={confirmPassword}
        required
        disabled={loading}
      />

      <div class="button-group">
        <Button type="submit" kind="primary" disabled={loading}>
          {#if loading}Updating...{:else}Update Password{/if}
        </Button>
      </div>
    </FormGroup>
  </Form>
</main>

<style>
  main {
    max-width: 480px;
    margin: 5rem auto;
    padding: 2.5rem;
    background: var(--cds-layer, #fff);
    border-radius: 12px;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.06);
    font-family: 'Segoe UI', Tahoma, sans-serif;
  }

  h2 {
    text-align: center;
    color: var(--cds-text-primary, #161616);
    font-size: 1.6rem;
    margin-bottom: 2rem;
  }

  :global(.bx--form-group) {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }

  .button-group {
    display: flex;
    justify-content: flex-end;
    margin-top: 1rem;
  }

  :global(.bx--inline-notification) {
    margin-bottom: 1.5rem;
  }

  @media (max-width: 600px) {
    main {
      margin: 2rem;
      padding: 1.5rem;
    }
  }
</style>
