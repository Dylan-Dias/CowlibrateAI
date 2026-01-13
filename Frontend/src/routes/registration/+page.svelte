<script>
  import 'carbon-components-svelte/css/g10.css';
  import '../styles/Registration.css';
  import { goto } from '$app/navigation';

  import { register } from '$lib/services/auth';
  import { RegistrationForm } from '$lib/components/Registration/Form/RegistrationForm.svelte';
  import { Notifications } from '$lib/components/Registration/Notifications/Notifications.svelte';
  import SubmitButton from '$components/Registration/SubmitButton/SubmitButton.svelte';

  let username = '';
  let email = '';
  let password = '';
  let role = 'cow';

  let error = '';
  let success = '';
  let loading = false;

  async function handleSubmit(event) {
    error = '';
    success = '';
    loading = true;

    try {
      const data = await register(
        event.detail.username,
        event.detail.email,
        event.detail.password,
        event.detail.role.toLowerCase()
      );

      success = 'Registration successful! Redirecting...';

      setTimeout(() => {
        if (data.user?.role === 'goat') {
          goto('/dashboard/GoatAnalytics');
        } else if (data.user?.role === 'cow') {
          goto('/cow');
        } else {
          goto('/dashboard');
        }
      }, 1500);
    } catch (err) {
      error = err.message;
    } finally {
      loading = false;
    }
  }
</script>

<main>
  <h1>Registration</h1>

  <RegistrationNotifications {error} {success} />

  <RegistrationForm
    bind:username
    bind:email
    bind:password
    bind:role
    {loading}
    on:submit={handleSubmit}
  />
</main>
