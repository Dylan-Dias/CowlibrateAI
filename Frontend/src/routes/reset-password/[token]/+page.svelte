<script>
  import { page } from '$app/stores';
  import ResetPasswordForm from '$lib/components/ResetPasswordForm.svelte';

  // Get token from URL
  let token;
  $: token = $page.params.token;
</script>

<ResetPasswordForm {token}></ResetPasswordForm>
