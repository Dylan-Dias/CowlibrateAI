<script>
  import {
    Header,
    HeaderNav,
    HeaderNavItem
  } from "carbon-components-svelte";
  import { goto } from "$app/navigation";


    function navigateTo(path) {
    goto(path);
  }
</script>

<Header company="Dairy Dashboard" platformName="Milk Yield">
  <HeaderNav>
    <HeaderNavItem on:click={() => navigateTo("/analytics")}>
      Bovine Analytics
    </HeaderNavItem>
      


  </HeaderNav>
</Header>