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

<div class="form-wrapper">
  <h2>Reset Your Password</h2>

  <Form on:submit={submit}>
    <FormGroup legendText="Enter your new password">
      <PasswordInput
        labelText="New Password"
        bind:value={newPassword}
        required
        disabled={loading}
        class="password-input"
      />
      <PasswordInput
        labelText="Confirm Password"
        bind:value={confirmPassword}
        required
        disabled={loading}
        class="password-input"
      />
      <div class="button-group">
        <SubmitButton text="Update Password" {loading} />
      </div>
    </FormGroup>
  </Form>
</div>

<style>
  .form-wrapper {
    max-width: 420px;
    margin: 3rem auto;
    padding: 2rem 2.5rem;
    background: #ffffff;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    font-family: 'IBM Plex Sans', sans-serif;
  }

  .form-wrapper h2 {
    text-align: center;
    margin-bottom: 1.5rem;
    font-weight: 600;
    color: #1d1d1d;
  }

  .password-input {
    margin-bottom: 1.2rem;
  }

  .password-input input {
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
  }

  .password-input input:focus {
    border-color: #0f62fe;
    box-shadow: 0 0 0 3px rgba(14, 118, 254, 0.2);
  }

  .button-group {
    display: flex;
    justify-content: flex-end;
    margin-top: 1.5rem;
  }

  /* Optional: make the SubmitButton a bit wider for aesthetic balance */
  .button-group button {
    min-width: 150px;
  }

  /* Responsive for smaller screens */
  @media (max-width: 480px) {
    .form-wrapper {
      padding: 1.5rem 1.8rem;
      margin: 2rem auto;
    }

    .button-group {
      justify-content: center;
    }
  }
</style>
