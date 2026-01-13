<script>
  import { goto } from '$app/navigation';
  import 'carbon-components-svelte/css/g10.css';
  import PasswordResetForm from '$components/PasswordReset/PasswordResetForm/PasswordResetForm.svelte';
  import PasswordResetNotification from '$components/PasswordReset/PasswordResetNotification/PasswordResetNotification.svelte';
  import { requestPasswordReset } from '$lib/services/auth';

  let email = '';
  let message = '';
  let error = '';
  let loading = false;

  async function handleReset(event) {
    error = '';
    message = '';

    if (!event.detail.email.trim()) {
      error = 'Please enter your email address.';
      return;
    }

    loading = true;

    try {
      await requestPasswordReset(event.detail.email);
      message =
        'If this email is registered, you will receive password reset instructions.';
      email = '';
    } catch (err) {
      error = err.message;
    } finally {
      loading = false;
    }
  }
</script>

<PasswordResetNotification {message} {error} />

<PasswordResetForm
  bind:email
  {loading}
  on:submit={handleReset}
  on:back={() => goto('/login')}
/>
