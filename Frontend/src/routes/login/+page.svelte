<script>
  import { goto } from '$app/navigation';
  import LoginForm from '$components/Login/LoginForm.svelte';
  import LoginNotifications from '$components/Login/LoginNotifications.svelte';
  import { login } from '$lib/API/AuthenticationAPI/LoginAPI';


  let username = '';
  let password = '';
  let loginError = '';
  let loginSuccess = false;

  async function handleLogin(event) {
    event.preventDefault();
    loginError = '';
    loginSuccess = false;

    try {
      const data = await login(username, password);
      loginSuccess = true;

      if (data.role === "goat") goto("/dashboard/GoatAnalytics");
      else if (data.role === "cow") goto("/analytics");
      else goto("/dashboard");
    } catch (err) {
      loginError = err.message;
      console.error(err);
    }
  }

  function handleForgotPassword() {
    goto('/forgot-password');
  } 
</script>



<main>
  <LoginNotifications {loginSuccess} {loginError} />
  <LoginForm
    bind:username
    bind:password
    onSubmit={handleLogin}
    onForgotPassword={handleForgotPassword}
  />
</main>

<style>
main {
  width: 100%;
  max-width: 650px; /* makes it a bit larger */
  margin: 150 auto; /* centers horizontally */
  padding: 5rem 4.5rem;
  background: var(--cds-layer);
  border-radius: 0px;
  box-shadow: 0 10px 10px 10px  rgba(0, 0, 0, 0.1);
  font-family: 'Segoe UI', Tahoma, sans-serif;

  /* Center vertically */
  display: center;
  flex-direction: column;
  justify-content: center;
}

  :global(.bx--form-group) {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }

  :global(.bx--inline-notification) {
    margin-bottom: 1.5rem;
  }

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


  :global(.bx--btn) {
    min-width: auto;
    padding: 0.5rem 1rem;
    font-size: 0.85rem;
  }
</style>
