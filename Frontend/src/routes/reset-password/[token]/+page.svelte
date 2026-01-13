<script>
  import { page } from '$app/stores';
  import { goto } from '$app/navigation';

  import ForgotPasswordForm from '$components/ForgotPassword/ForgotPasswordForm.svelte';
  import ForgotPasswordNotification from '$components/ForgotPassword/ForgotPasswordNotification.svelte';
  import { resetPassword } from '$lib/services/auth';

  let token;
  $: token = $page.params.token;

  let error = '';
  let success = false;
  let loading = false;

  async function handleReset(event) {
    error = '';
    success = false;
    loading = true;

    const { newPassword, confirmPassword } = event.detail;

    if (newPassword !== confirmPassword) {
      error = 'Passwords do not match';
      loading = false;
      return;
    }

    try {
      await resetPassword(token, newPassword, confirmPassword);
      success = true;

      setTimeout(() => goto('/login'), 2000);
    } catch (err) {
      error = err.message;
    } finally {
      loading = false;
    }
  }
</script>

<main>
  <h2>Reset Your Password</h2>

  <!-- Use the correct imported component names -->
  <ForgotPasswordNotification {error} {success} />
  <ForgotPasswordForm {token} {loading} on:submit={handleReset} />
</main>
