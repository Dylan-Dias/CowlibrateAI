<script>
  import { InlineNotification } from "carbon-components-svelte";
  export let loginSuccess = false;
  export let loginError = '';
</script>

{#if loginSuccess}
  <InlineNotification title="Login Successful" subtitle="You are now logged in." kind="success" />
{/if}

{#if loginError}
  <InlineNotification title="Login Failed" subtitle={loginError} kind="error" />
{/if}

<style>
  :global(.bx--inline-notification) {
    margin-bottom: 1.5rem;
  }
</style>
