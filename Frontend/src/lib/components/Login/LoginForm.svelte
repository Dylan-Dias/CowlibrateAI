<script>
  import { Form, FormGroup, TextInput, PasswordInput, Button } from "carbon-components-svelte";
  import { safeFetch } from '../../API/AuthenticationAPI/LoginAPI.js';

  export let username = '';
  export let password = '';
  export let onSubmit;
  export let onForgotPassword;
  
  async function submitLogin() {
    try {
      const res = await safeFetch("https://cowlibrate.onrender.com/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",  // important for cookies/sessions
        body: JSON.stringify({ username, password }),
      });

      const data = await res.json();
      console.log("Login response:", data);
    } catch (err) {
      console.error("Login failed:", err);
    }
  }
</script>

<Form on:submit={onSubmit}>
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
      <Button kind="tertiary" type="button" size="sm" on:click={onForgotPassword}>
        Forgot Password?
      </Button>
    </div>
  </FormGroup>
</Form>

<style>

:global(.bx--form-group) {
  display: flex;
  flex-direction: column;
}

:global(.bx--form-item) {
  margin-bottom: 1.25rem;
}

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
</style>
