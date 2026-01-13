<script>
  import { Form, FormGroup, TextInput } from 'carbon-components-svelte';
  import SubmitButton from '$components/Registration/SubmitButton/SubmitButton.svelte';
  import { createEventDispatcher } from 'svelte';

  export let loading = false;
  export let email = '';

  const dispatch = createEventDispatcher();

  function submit(event) {
    event.preventDefault();
    dispatch('submit', { email });
  }
</script>

<div class="form-wrapper">
  <h2>Forgot Password</h2>
  <p>Enter your email to receive password reset instructions.</p>

  <Form on:submit={submit}>
    <FormGroup legendText="Email Address">
      <TextInput
        labelText="Email"
        bind:value={email}
        type="email"
        required
        disabled={loading}
        class="email-input"
      />
      <div class="button-group">
        <SubmitButton text="Send Reset Link" {loading} />
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
    text-align: center;
  }

  .form-wrapper h2 {
    margin-bottom: 0.5rem;
    font-weight: 600;
    color: #1d1d1d;
  }

  .form-wrapper p {
    margin-bottom: 1.5rem;
    color: #555;
    font-size: 0.95rem;
  }

  .email-input {
    margin-bottom: 1.2rem;
  }

  .email-input input {
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
  }

  .email-input input:focus {
    border-color: #0f62fe;
    box-shadow: 0 0 0 3px rgba(14, 118, 254, 0.2);
  }

  .button-group {
    display: flex;
    justify-content: flex-end;
    margin-top: 1.5rem;
  }

  .button-group button {
    min-width: 150px;
  }

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
