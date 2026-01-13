<script>
  import 'carbon-components-svelte/css/g10.css';
  import { Form, FormGroup, TextInput, Button } from 'carbon-components-svelte';
  import { createEventDispatcher } from 'svelte';

  export let email = '';
  export let loading = false;

  const dispatch = createEventDispatcher();

  function submit(event) {
    event.preventDefault();
    dispatch('submit', { email });
  }

  function back() {
    dispatch('back');
  }
</script>

<Form on:submit={submit}>
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

      <Button
        type="button"
        kind="tertiary"
        size="small"
        on:click={back}
        disabled={loading}
      >
        Back to Login
      </Button>
    </div>
  </FormGroup>
</Form>

<style>
  .button-group {
    margin-top: 1rem;
    display: flex;
    justify-content: flex-end;
    gap: 0.5rem;
  }
</style>
