<script>
  import { InlineNotification } from 'carbon-components-svelte';

  export let message = '';
  export let error = '';
</script>

{#if message}
  <InlineNotification
    title="Success"
    subtitle={message}
    kind="success"
  />
{/if}

{#if error}
  <InlineNotification
    title="Error"
    subtitle={error}
    kind="error"
  />
{/if}
