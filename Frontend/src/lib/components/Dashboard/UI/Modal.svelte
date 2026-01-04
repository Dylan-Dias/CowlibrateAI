<script>
  import { Modal } from "carbon-components-svelte";

  export let open = false;
</script>

<Modal
  bind:open
  modalHeading="Cowlibrate Onboarding"
  hasScrollingContent
  passiveModal
  >
  <p>
    Hello, Welcome to Cowlibrate's onboarding page. 
    Here you will your herd's data to be stored in our Database. 
    This is a one time process, so you will only see this page once. 
    But, if you make mistakes there is a Database View page to edit and update your herd's information 
    
  </p>
</Modal>
