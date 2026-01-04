<script>
  import { Modal } from "carbon-components-svelte";

  export let open = false;
</script>

<Modal
  bind:open
  modalHeading="Welcome!"
hasScrollingContent
  passiveModal
  >
  <p>
    Thanks for registering! Before you begin, please review this information.
  </p>
</Modal>
