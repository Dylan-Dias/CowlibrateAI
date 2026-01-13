<script>
  import { InlineNotification } from 'carbon-components-svelte';

  export let error = '';
  export let success = false;
</script>

{#if success}
  <InlineNotification title="Success" subtitle="Your password has been updated." kind="success" />
{/if}

{#if error}
  <InlineNotification title="Error" subtitle={error} kind="error" />
{/if}
