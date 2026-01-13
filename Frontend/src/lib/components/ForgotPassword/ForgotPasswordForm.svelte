<script>
  import { Form, FormGroup, PasswordInput } from 'carbon-components-svelte';
  import SubmitButton from '$components/Registration/SubmitButton/SubmitButton.svelte';
  import { createEventDispatcher } from 'svelte';

  export let token;
  export let loading = false;

  let newPassword = '';
  let confirmPassword = '';

  const dispatch = createEventDispatcher();

  function submit(event) {
    event.preventDefault();
    dispatch('submit', { newPassword, confirmPassword });
  }
</script>

<Form on:submit={submit}>
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
      <SubmitButton text="Update Password" {loading} />
    </div>
  </FormGroup>
</Form>

<style>
.button-group {
  display: flex;
  justify-content: flex-end;
  margin-top: 1rem;
}
</style>
