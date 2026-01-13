<script>
  import { InlineNotification } from 'carbon-components-svelte';

  export let error = '';
  export let success = '';
  export let info = '';
</script>

{#if error}
  <InlineNotification
    title="Error"
    subtitle={error}
    kind="error"
    lowContrast
  />
{/if}

{#if success}
  <InlineNotification
    title="Success"
    subtitle={success}
    kind="success"
    lowContrast
  />
{/if}

{#if info}
  <InlineNotification
    title="Info"
    subtitle={info}
    kind="info"
    lowContrast
  />
{/if}
